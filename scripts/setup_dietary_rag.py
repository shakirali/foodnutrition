"""Setup script for RAG system with dietary requirements data."""
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.dietary_vector_store import DietaryRequirementsVectorStore
from data.process_dietary_data import process_all_dietary_data


def setup_dietary_rag():
    """Setup RAG system with dietary requirements data."""
    data_dir = Path(__file__).parent.parent / "data"
    mineral_path = data_dir / "mineral_requirements.json"
    vitamin_path = data_dir / "vitamin_recommendations.json"
    nutrition_path = data_dir / "nutrition_recommendations.json"
    
    # Check if all files exist
    missing_files = []
    if not mineral_path.exists():
        missing_files.append("mineral_requirements.json")
    if not vitamin_path.exists():
        missing_files.append("vitamin_recommendations.json")
    if not nutrition_path.exists():
        missing_files.append("nutrition_recommendations.json")
    
    if missing_files:
        print(f"Error: Missing required files: {', '.join(missing_files)}")
        print(f"Please ensure all files are in the {data_dir} directory.")
        return
    
    print("Processing dietary requirements data...")
    documents = process_all_dietary_data(mineral_path, vitamin_path, nutrition_path)
    print(f"✓ Processed {len(documents)} documents")
    
    print("Initializing vector store...")
    vector_store_path = data_dir / "dietary_vector_db"
    vector_store = DietaryRequirementsVectorStore(
        vector_store_path,
        mineral_path=mineral_path,
        vitamin_path=vitamin_path,
        nutrition_path=nutrition_path
    )
    
    # Check if collection already has data
    existing_count = vector_store.get_collection_count()
    if existing_count > 0:
        print(f"⚠ Collection already has {existing_count} documents.")
        response = input("Do you want to re-index? This will replace existing data. (y/N): ")
        if response.lower() != 'y':
            print("Skipping re-indexing.")
            return
        # Clear existing collection
        vector_store.client.delete_collection("dietary_requirements")
        vector_store.collection = vector_store.client.get_or_create_collection(
            name="dietary_requirements",
            metadata={"description": "Dietary requirements: minerals, vitamins, and nutrition recommendations"}
        )
    
    print("Adding documents to vector store...")
    vector_store.add_documents(documents)
    
    final_count = vector_store.get_collection_count()
    print(f"✓ RAG setup complete! Indexed {final_count} dietary requirement documents.")


if __name__ == "__main__":
    setup_dietary_rag()

