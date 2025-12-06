"""Setup script for RAG system with USDA data and dietary requirements."""
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.vector_store import NutritionVectorStore
from data.process_usda_data import process_all_foods
from data.dietary_vector_store import DietaryRequirementsVectorStore
from data.process_dietary_data import process_all_dietary_data


def setup_usda_rag(data_dir: Path, reindex: bool = False) -> bool:
    """Setup RAG system with USDA food data."""
    print("\n" + "="*60)
    print("Setting up USDA Food Data RAG System")
    print("="*60)
    
    json_path = data_dir / "FoodData_Central_foundation_food_json_2025-04-24.json"
    
    if not json_path.exists():
        print(f"⚠ USDA JSON file not found at {json_path}")
        print("Skipping USDA data setup.")
        return False
    
    print("Processing USDA data...")
    documents = process_all_foods(json_path)
    print(f"✓ Processed {len(documents)} food items")
    
    print("Initializing vector store...")
    vector_store_path = data_dir / "vector_db"
    vector_store = NutritionVectorStore(vector_store_path, json_path=json_path)
    
    # Check if collection already has data
    existing_count = vector_store.get_collection_count()
    if existing_count > 0:
        if not reindex:
            print(f"⚠ Collection already has {existing_count} documents.")
            response = input("Do you want to re-index? This will replace existing data. (y/N): ")
            if response.lower() != 'y':
                print("Skipping USDA re-indexing.")
                return False
        # Clear existing collection
        vector_store.client.delete_collection("usda_nutrition")
        vector_store.collection = vector_store.client.get_or_create_collection(
            name="usda_nutrition",
            metadata={"description": "USDA FoodData Central nutrition information"}
        )
    
    print("Adding documents to vector store...")
    vector_store.add_documents(documents)
    
    final_count = vector_store.get_collection_count()
    print(f"✓ USDA RAG setup complete! Indexed {final_count} food items.")
    return True


def setup_dietary_rag(data_dir: Path, reindex: bool = False) -> bool:
    """Setup RAG system with dietary requirements data."""
    print("\n" + "="*60)
    print("Setting up Dietary Requirements RAG System")
    print("="*60)
    
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
        print(f"⚠ Missing required files: {', '.join(missing_files)}")
        print("Skipping dietary requirements setup.")
        return False
    
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
        if not reindex:
            print(f"⚠ Collection already has {existing_count} documents.")
            response = input("Do you want to re-index? This will replace existing data. (y/N): ")
            if response.lower() != 'y':
                print("Skipping dietary requirements re-indexing.")
                return False
        # Clear existing collection
        vector_store.client.delete_collection("dietary_requirements")
        vector_store.collection = vector_store.client.get_or_create_collection(
            name="dietary_requirements",
            metadata={"description": "Dietary requirements: minerals, vitamins, and nutrition recommendations"}
        )
    
    print("Adding documents to vector store...")
    vector_store.add_documents(documents)
    
    final_count = vector_store.get_collection_count()
    print(f"✓ Dietary Requirements RAG setup complete! Indexed {final_count} documents.")
    return True


def setup_rag():
    """Setup both RAG systems (USDA food data and dietary requirements)."""
    print("\n" + "="*60)
    print("RAG System Setup - Complete")
    print("="*60)
    print("This script will set up both vector databases:")
    print("  1. USDA Food Data (nutrition lookup)")
    print("  2. Dietary Requirements (minerals, vitamins, nutrition)")
    print("="*60)
    
    data_dir = Path(__file__).parent.parent / "data"
    
    # Setup USDA RAG
    usda_success = setup_usda_rag(data_dir)
    
    # Setup Dietary Requirements RAG
    dietary_success = setup_dietary_rag(data_dir)
    
    # Summary
    print("\n" + "="*60)
    print("Setup Summary")
    print("="*60)
    print(f"USDA Food Data: {'✓ Complete' if usda_success else '✗ Skipped'}")
    print(f"Dietary Requirements: {'✓ Complete' if dietary_success else '✗ Skipped'}")
    print("="*60)
    
    if usda_success or dietary_success:
        print("\n✓ RAG setup process completed!")
    else:
        print("\n⚠ No vector databases were set up. Please ensure required data files are present.")


if __name__ == "__main__":
    setup_rag()

