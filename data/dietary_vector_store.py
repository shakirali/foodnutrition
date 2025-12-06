"""Vector store for dietary requirements data using ChromaDB."""
import chromadb
import json
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer


class DietaryRequirementsVectorStore:
    """Vector store for dietary requirements (minerals, vitamins, nutrition)."""
    
    def __init__(
        self,
        persist_directory: Path,
        embedding_model: str = "all-MiniLM-L6-v2",
        mineral_path: Optional[Path] = None,
        vitamin_path: Optional[Path] = None,
        nutrition_path: Optional[Path] = None
    ):
        """
        Initialize vector store for dietary requirements.
        
        Args:
            persist_directory: Where to store the vector database
            embedding_model: Sentence transformer model name (local, no API needed)
            mineral_path: Path to mineral_requirements.json (optional, for loading full data)
            vitamin_path: Path to vitamin_recommendations.json (optional, for loading full data)
            nutrition_path: Path to nutrition_recommendations.json (optional, for loading full data)
        """
        self.persist_directory = persist_directory
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Store JSON paths for loading full data when needed
        self.mineral_path = mineral_path
        self.vitamin_path = vitamin_path
        self.nutrition_path = nutrition_path
        self._data_cache = None  # Cache for loaded data
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(persist_directory),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="dietary_requirements",
            metadata={"description": "Dietary requirements: minerals, vitamins, and nutrition recommendations"}
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
        """Search for similar dietary requirements information."""
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
    
    def _load_data_cache(self):
        """Lazy load dietary data from JSON files."""
        if self._data_cache is not None:
            return
        
        self._data_cache = {
            'minerals': {},
            'vitamins': {},
            'nutrition': {}
        }
        
        # Load minerals
        if self.mineral_path and self.mineral_path.exists():
            try:
                with open(self.mineral_path, 'r', encoding='utf-8') as f:
                    self._data_cache['minerals'] = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load mineral data: {e}")
        
        # Load vitamins
        if self.vitamin_path and self.vitamin_path.exists():
            try:
                with open(self.vitamin_path, 'r', encoding='utf-8') as f:
                    self._data_cache['vitamins'] = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load vitamin data: {e}")
        
        # Load nutrition
        if self.nutrition_path and self.nutrition_path.exists():
            try:
                with open(self.nutrition_path, 'r', encoding='utf-8') as f:
                    self._data_cache['nutrition'] = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load nutrition data: {e}")
    
    def get_requirements_by_key(self, age_group: str, gender: str) -> Optional[Dict]:
        """Retrieve full dietary requirements data by age group and gender."""
        self._load_data_cache()
        
        doc_id = f"dietary_{age_group}_{gender}"
        
        # Try to get from cache
        minerals = self._data_cache.get('minerals', {}).get(age_group, {}).get(gender, {})
        vitamins = self._data_cache.get('vitamins', {}).get(age_group, {}).get(gender, {})
        nutrition = self._data_cache.get('nutrition', {}).get(age_group, {}).get(gender, {})
        
        if not (minerals or vitamins or nutrition):
            return None
        
        return {
            'age_group': age_group,
            'gender': gender,
            'minerals': minerals,
            'vitamins': vitamins,
            'nutrition': nutrition
        }
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()

