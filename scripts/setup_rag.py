"""Setup script for RAG system with USDA data."""
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.vector_store import NutritionVectorStore
from data.process_usda_data import process_all_foods


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
    vector_store = NutritionVectorStore(vector_store_path, json_path=json_path)
    
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

