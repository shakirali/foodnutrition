# RAG Implementation Guide for USDA Nutrition Data

This guide explains how to implement a RAG (Retrieval-Augmented Generation) system for querying the USDA FoodData Central dataset locally.

## Architecture Overview

```
User Query → Nutrition Lookup Tool → Vector DB Search → Retrieve Top-K → Format Response
```

## Step 1: Install Required Dependencies

Add these to `requirements.txt`:

```txt
# RAG and Vector Database
chromadb>=0.4.0  # Lightweight vector database (or use FAISS, Qdrant, etc.)
sentence-transformers>=2.2.0  # For generating embeddings locally
# OR use OpenAI embeddings:
# openai>=1.0.0

# Data processing
pandas>=2.0.0
numpy>=1.24.0
```

**Alternative Options:**
- **FAISS** (Facebook AI Similarity Search): Fast, but requires more setup
- **Qdrant**: Production-ready, can run locally or cloud
- **Weaviate**: More features, heavier
- **ChromaDB**: Lightweight, easy to use (recommended for local)

## Step 2: Data Structure

The USDA JSON file (`FoodData_Central_foundation_food_json_2025-04-24.json`) has the following structure:

```json
{
  "FoundationFoods": [
    {
      "fdcId": 321358,
      "description": "Hummus, commercial",
      "foodClass": "FinalFood",
      "foodCategory": {
        "description": "Legumes and Legume Products"
      },
      "foodNutrients": [
        {
          "type": "FoodNutrient",
          "id": 2219707,
          "nutrient": {
            "id": 1120,
            "number": "334",
            "name": "Cryptoxanthin, beta",
            "rank": 7460,
            "unitName": "µg"
          },
          "amount": 3.0,
          "dataPoints": 1,
          "foodNutrientDerivation": {...}
        }
      ],
      "foodAttributes": [...],
      "foodPortions": [...],
      "nutrientConversionFactors": [...]
    }
  ]
}
```

**Key Fields:**
- `fdcId`: Unique food identifier
- `description`: Food name/description
- `foodClass`: Type of food (e.g., "FinalFood")
- `foodCategory`: Category information
- `foodNutrients`: Array of nutrient information with nested structure

## Step 3: Data Processing Pipeline

### 3.1 Parse and Structure Data

```python
# src/data/process_usda_data.py
import json
from pathlib import Path
from typing import List, Dict

def load_usda_json(json_path: Path) -> List[Dict]:
    """Load USDA JSON data."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('FoundationFoods', [])

def create_document(food_item: Dict) -> Dict:
    """Convert food item to a searchable document."""
    # Extract key information
    fdc_id = food_item.get('fdcId', '')
    description = food_item.get('description', '')
    food_class = food_item.get('foodClass', '')
    food_category = food_item.get('foodCategory', {})
    category_desc = food_category.get('description', '') if isinstance(food_category, dict) else ''
    
    # Build nutrient summary - prioritize important nutrients
    nutrients = food_item.get('foodNutrients', [])
    nutrient_text = []
    
    # Common important nutrients to prioritize
    important_nutrients = [
        'Energy', 'Protein', 'Total lipid (fat)', 'Carbohydrate, by difference',
        'Fiber, total dietary', 'Calcium', 'Iron', 'Vitamin C', 'Vitamin A',
        'Sodium', 'Sugars, total including NLEA'
    ]
    
    # First, add important nutrients
    for nutrient in nutrients:
        nutrient_name = nutrient.get('nutrient', {}).get('name', '')
        if nutrient_name in important_nutrients:
            amount = nutrient.get('amount', 0)
            unit = nutrient.get('nutrient', {}).get('unitName', '')
            if amount is not None and amount != 0:
                nutrient_text.append(f"{nutrient_name}: {amount} {unit}")
    
    # Then add other nutrients (limit to avoid too long text)
    for nutrient in nutrients:
        nutrient_name = nutrient.get('nutrient', {}).get('name', '')
        if nutrient_name not in important_nutrients and len(nutrient_text) < 15:
            amount = nutrient.get('amount', 0)
            unit = nutrient.get('nutrient', {}).get('unitName', '')
            if amount is not None and amount != 0:
                nutrient_text.append(f"{nutrient_name}: {amount} {unit}")
    
    # Create searchable text
    searchable_text = f"""
    Food: {description}
    Category: {category_desc}
    Food Class: {food_class}
    FDC ID: {fdc_id}
    Nutrients: {', '.join(nutrient_text)}
    """
    
    return {
        'id': str(fdc_id),
        'text': searchable_text.strip(),
        'metadata': {
            'fdc_id': fdc_id,
            'description': description,
            'food_class': food_class,
            'category': category_desc,
            'full_data': food_item  # Store full data for retrieval
        }
    }

def process_all_foods(json_path: Path) -> List[Dict]:
    """Process all food items into documents."""
    foods = load_usda_json(json_path)
    documents = []
    
    print(f"Processing {len(foods)} food items...")
    for food in foods:
        doc = create_document(food)
        documents.append(doc)
    
    return documents
```

## Step 4: Vector Database Setup

### 4.1 Initialize ChromaDB

```python
# src/rag/vector_store.py
import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer

class NutritionVectorStore:
    def __init__(self, persist_directory: Path, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize vector store for nutrition data.
        
        Args:
            persist_directory: Where to store the vector database
            embedding_model: Sentence transformer model name (local, no API needed)
        """
        self.persist_directory = persist_directory
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(persist_directory),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="usda_nutrition",
            metadata={"description": "USDA FoodData Central nutrition information"}
        )
        
        # Load embedding model (runs locally, no API needed)
        print(f"Loading embedding model: {embedding_model}...")
        self.embedding_model = SentenceTransformer(embedding_model)
        print(f"✓ Loaded embedding model: {embedding_model}")
    
    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store."""
        texts = [doc['text'] for doc in documents]
        ids = [doc['id'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        
        # Add to ChromaDB
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            ids=ids,
            metadatas=metadatas
        )
        print(f"✓ Added {len(documents)} documents to vector store")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for similar nutrition information."""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results and results['distances'] else None
                })
        
        return formatted_results
    
    def get_food_by_id(self, fdc_id: str) -> Optional[Dict]:
        """Retrieve full food data by FDC ID."""
        results = self.collection.get(ids=[str(fdc_id)])
        if results['ids']:
            return results['metadatas'][0].get('full_data')
        return None
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()
```

## Step 5: Create Nutrition Lookup Tool

### 5.1 Implement BaseTool

```python
# src/tools/nutrition_lookup_tool.py
from spoon_ai.tools.base import BaseTool
from src.rag.vector_store import NutritionVectorStore
from pathlib import Path
from typing import Optional

class NutritionLookupTool(BaseTool):
    """Tool for looking up nutritional information from USDA FoodData Central."""
    
    name: str = "nutrition_lookup"
    description: str = (
        "Look up nutritional information for foods from the USDA FoodData Central database. "
        "Use this tool when users ask about food nutrition, calories, vitamins, minerals, "
        "or want to compare foods nutritionally. Can search by food name, nutrient name, "
        "or nutritional properties (e.g., 'high protein foods', 'foods rich in iron')."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "food_query": {
                "type": "string",
                "description": "The food item or nutrient to search for (e.g., 'apple', 'chicken breast', 'high protein foods', 'foods rich in iron', 'low calorie vegetables')"
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return (default: 5, max: 20)",
                "default": 5,
                "minimum": 1,
                "maximum": 20
            }
        },
        "required": ["food_query"]
    }
    
    def __init__(self, vector_store: Optional[NutritionVectorStore] = None):
        super().__init__()
        if vector_store is None:
            # Initialize vector store if not provided
            data_dir = Path(__file__).parent.parent.parent / "data"
            vector_store_path = data_dir / "vector_db"
            self.vector_store = NutritionVectorStore(vector_store_path)
        else:
            self.vector_store = vector_store
    
    async def execute(self, food_query: str, max_results: int = 5) -> str:
        """Execute the nutrition lookup."""
        try:
            # Validate max_results
            max_results = min(max(1, max_results), 20)
            
            # Search vector store
            results = self.vector_store.search(food_query, n_results=max_results)
            
            if not results:
                return f"No nutritional information found for '{food_query}'. Try a different search term."
            
            # Format response
            response_parts = [f"Found {len(results)} result(s) for '{food_query}':\n"]
            
            for i, result in enumerate(results, 1):
                metadata = result['metadata']
                full_data = metadata.get('full_data', {})
                
                # Extract key nutrients
                nutrients = full_data.get('foodNutrients', [])
                
                # Prioritize important nutrients for display
                important_nutrients = {
                    'Energy': 'Calories',
                    'Protein': 'Protein',
                    'Total lipid (fat)': 'Fat',
                    'Carbohydrate, by difference': 'Carbs',
                    'Fiber, total dietary': 'Fiber',
                    'Calcium, Ca': 'Calcium',
                    'Iron, Fe': 'Iron',
                    'Vitamin C, total ascorbic acid': 'Vitamin C',
                    'Sodium, Na': 'Sodium',
                    'Sugars, total including NLEA': 'Sugars'
                }
                
                key_nutrients = []
                nutrient_map = {}
                
                # Build nutrient map
                for nutrient in nutrients:
                    name = nutrient.get('nutrient', {}).get('name', '')
                    amount = nutrient.get('amount')
                    unit = nutrient.get('nutrient', {}).get('unitName', '')
                    if amount is not None and amount != 0 and name:
                        nutrient_map[name] = (amount, unit)
                
                # Add important nutrients first
                for usda_name, display_name in important_nutrients.items():
                    if usda_name in nutrient_map:
                        amount, unit = nutrient_map[usda_name]
                        key_nutrients.append(f"{display_name}: {amount} {unit}")
                
                # Add a few more nutrients if space
                for name, (amount, unit) in list(nutrient_map.items())[:5]:
                    if name not in important_nutrients:
                        key_nutrients.append(f"{name}: {amount} {unit}")
                
                category = metadata.get('category', 'Unknown category')
                
                response_parts.append(
                    f"\n{i}. {metadata.get('description', 'Unknown')}\n"
                    f"   Category: {category}\n"
                    f"   Key Nutrients: {', '.join(key_nutrients[:8])}\n"
                )
            
            return "\n".join(response_parts)
            
        except Exception as e:
            return f"Error looking up nutrition information: {str(e)}"
```

## Step 6: Setup Script

```python
# scripts/setup_rag.py
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.vector_store import NutritionVectorStore
from src.data.process_usda_data import process_all_foods

def setup_rag():
    """Setup RAG system with USDA data."""
    data_dir = Path(__file__).parent.parent / "data"
    json_path = data_dir / "FoodData_Central_foundation_food_json_2025-04-24.json"
    
    if not json_path.exists():
        print(f"Error: USDA JSON file not found at {json_path}")
        print("Please ensure the file is in the data/ directory.")
        return
    
    print("Processing USDA data...")
    documents = process_all_foods(json_path)
    print(f"✓ Processed {len(documents)} food items")
    
    print("Initializing vector store...")
    vector_store_path = data_dir / "vector_db"
    vector_store = NutritionVectorStore(vector_store_path)
    
    # Check if collection already has data
    existing_count = vector_store.get_collection_count()
    if existing_count > 0:
        print(f"⚠ Collection already has {existing_count} documents.")
        response = input("Do you want to re-index? This will replace existing data. (y/N): ")
        if response.lower() != 'y':
            print("Skipping re-indexing.")
            return
        # Clear existing collection
        vector_store.client.delete_collection("usda_nutrition")
        vector_store.collection = vector_store.client.get_or_create_collection(
            name="usda_nutrition",
            metadata={"description": "USDA FoodData Central nutrition information"}
        )
    
    print("Adding documents to vector store...")
    vector_store.add_documents(documents)
    
    final_count = vector_store.get_collection_count()
    print(f"✓ RAG setup complete! Indexed {final_count} food items.")

if __name__ == "__main__":
    setup_rag()
```

## Step 7: Integrate with Advisor Agent

```python
# agents/advisor_agent.py (updated)
from pydantic import Field
from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.tools import ToolManager
from src.tools.nutrition_lookup_tool import NutritionLookupTool

class NutritionAdvisorAgent(ToolCallAgent):
    # ... existing code ...
    
    # Add the nutrition lookup tool
    available_tools: ToolManager = Field(
        default_factory=lambda: ToolManager([
            NutritionLookupTool()
        ])
    )
```

## Step 8: Usage Workflow

1. **Install Dependencies**:
   ```bash
   pip install chromadb sentence-transformers pandas numpy
   ```

2. **Process and Index Data** (one-time setup):
   ```bash
   python scripts/setup_rag.py
   ```
   
   This will:
   - Load the JSON file from `data/FoodData_Central_foundation_food_json_2025-04-24.json`
   - Process all 340 food items
   - Generate embeddings
   - Store in ChromaDB at `data/vector_db/`

3. **Run Application**:
   ```bash
   python main.py
   ```

4. **Test the Tool**:
   - Ask: "What are the nutrients in an apple?"
   - Ask: "Find high protein foods"
   - Ask: "What foods are rich in iron?"

## Alternative: Using OpenAI Embeddings

If you prefer using OpenAI embeddings (requires API key):

```python
# src/rag/vector_store_openai.py
from openai import OpenAI
import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict

class NutritionVectorStoreOpenAI:
    def __init__(self, persist_directory: Path, api_key: str, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = model
        
        self.persist_directory = persist_directory
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        chroma_client = chromadb.PersistentClient(
            path=str(persist_directory),
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.collection = chroma_client.get_or_create_collection(
            name="usda_nutrition",
            metadata={"description": "USDA FoodData Central nutrition information"}
        )
    
    def add_documents(self, documents: List[Dict]):
        """Add documents using OpenAI embeddings."""
        texts = [doc['text'] for doc in documents]
        ids = [doc['id'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        
        # Generate embeddings using OpenAI
        print("Generating embeddings with OpenAI...")
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=texts
        )
        embeddings = [item.embedding for item in response.data]
        
        # Add to ChromaDB
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            ids=ids,
            metadatas=metadatas
        )
        print(f"✓ Added {len(documents)} documents to vector store")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search using OpenAI embeddings."""
        # Generate query embedding
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=[query]
        )
        query_embedding = response.data[0].embedding
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results (same as local version)
        formatted_results = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results and results['distances'] else None
                })
        
        return formatted_results
```

## Performance Considerations

1. **Embedding Model Choice**:
   - `all-MiniLM-L6-v2`: Fast, 384 dimensions, good for most use cases (recommended)
   - `all-mpnet-base-v2`: Slower, 768 dimensions, better accuracy
   - `multi-qa-MiniLM-L6-cos-v1`: Optimized for Q&A

2. **Index Size**: With 340 foods, ChromaDB handles this easily. For larger datasets (>10k items), consider FAISS or Qdrant.

3. **Caching**: ChromaDB persists to disk, so embeddings are cached after first run.

4. **Query Performance**: Typical queries return results in <100ms.

## Testing

```python
# tests/test_nutrition_lookup.py
import pytest
from src.tools.nutrition_lookup_tool import NutritionLookupTool

@pytest.mark.asyncio
async def test_nutrition_lookup():
    tool = NutritionLookupTool()
    result = await tool.execute("apple", max_results=3)
    assert "apple" in result.lower() or "fruit" in result.lower()
    assert "nutrient" in result.lower() or "calorie" in result.lower()

@pytest.mark.asyncio
async def test_nutrition_lookup_protein():
    tool = NutritionLookupTool()
    result = await tool.execute("high protein", max_results=5)
    assert "protein" in result.lower()
```

## Project Structure After Implementation

```
foodnutrition/
├── agents/
│   └── advisor_agent.py
├── config/
│   └── config.py
├── data/
│   ├── FoodData_Central_foundation_food_json_2025-04-24.json
│   └── vector_db/                    # ChromaDB storage (created after setup)
│       └── ...
├── scripts/
│   └── setup_rag.py
├── src/
│   ├── data/
│   │   └── process_usda_data.py
│   ├── rag/
│   │   └── vector_store.py
│   └── tools/
│       └── nutrition_lookup_tool.py
├── main.py
└── requirements.txt
```

## Next Steps

1. Implement nutrient density calculation
2. Add filtering by dietary restrictions (vegan, halal, etc.)
3. Implement food comparison functionality
4. Add nutrient gap analysis (compare user intake vs recommendations)
5. Implement recommendation engine based on deficiencies
