"""Vector store for nutrition data using ChromaDB."""
import chromadb
import json
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer


class NutritionVectorStore:
    def __init__(self, persist_directory: Path, embedding_model: str = "all-MiniLM-L6-v2", json_path: Optional[Path] = None):
        """
        Initialize vector store for nutrition data.
        
        Args:
            persist_directory: Where to store the vector database
            embedding_model: Sentence transformer model name (local, no API needed)
            json_path: Path to original USDA JSON file for loading full_data (optional)
        """
        self.persist_directory = persist_directory
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Store JSON path for loading full_data when needed
        self.json_path = json_path
        self._food_data_cache = None  # Cache for loaded food data
        
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
    
    def _load_food_data_cache(self):
        """Lazy load food data from JSON file."""
        if self._food_data_cache is not None:
            return
        
        if self.json_path and self.json_path.exists():
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    foods = data.get('FoundationFoods', [])
                    # Create a lookup dictionary by FDC ID
                    self._food_data_cache = {str(food.get('fdcId')): food for food in foods}
            except Exception as e:
                print(f"Warning: Could not load food data cache: {e}")
                self._food_data_cache = {}
        else:
            self._food_data_cache = {}
    
    def get_food_by_id(self, fdc_id: str) -> Optional[Dict]:
        """Retrieve full food data by FDC ID."""
        # Try to load from cache (original JSON)
        self._load_food_data_cache()
        if self._food_data_cache and str(fdc_id) in self._food_data_cache:
            return self._food_data_cache[str(fdc_id)]
        
        # Fallback: try metadata (for backwards compatibility)
        results = self.collection.get(ids=[str(fdc_id)])
        if results['ids']:
            return results['metadatas'][0].get('full_data')
        return None
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()

