"""Quick test script to verify RAG setup."""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from data.process_usda_data import load_usda_json, process_all_foods
        print("✓ Data processing module imported")
        
        from data.vector_store import NutritionVectorStore
        print("✓ Vector store module imported")
        
        from agents.tools.nutrition_lookup_tool import NutritionLookupTool
        print("✓ Nutrition lookup tool imported")
        
        from agents.advisor_agent import NutritionAdvisorAgent
        print("✓ Advisor agent imported")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_data_processing():
    """Test data processing."""
    print("\nTesting data processing...")
    try:
        from data.process_usda_data import load_usda_json, process_all_foods
        from pathlib import Path
        
        json_path = Path('data/FoodData_Central_foundation_food_json_2025-04-24.json')
        if not json_path.exists():
            print(f"⚠ JSON file not found at {json_path}")
            return False
        
        foods = load_usda_json(json_path)
        print(f"✓ Loaded {len(foods)} foods")
        
        documents = process_all_foods(json_path)
        print(f"✓ Processed {len(documents)} documents")
        
        if documents:
            print(f"✓ Sample document structure: {list(documents[0].keys())}")
            print(f"✓ Sample document text length: {len(documents[0]['text'])} chars")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dependencies():
    """Test if required dependencies are installed."""
    print("\nTesting dependencies...")
    missing = []
    
    try:
        import chromadb
        print("✓ chromadb installed")
    except ImportError:
        print("✗ chromadb not installed")
        missing.append("chromadb")
    
    try:
        import sentence_transformers
        print("✓ sentence-transformers installed")
    except ImportError:
        print("✗ sentence-transformers not installed")
        missing.append("sentence-transformers")
    
    try:
        import pandas
        print("✓ pandas installed")
    except ImportError:
        print("✗ pandas not installed")
        missing.append("pandas")
    
    try:
        import numpy
        print("✓ numpy installed")
    except ImportError:
        print("✗ numpy not installed")
        missing.append("numpy")
    
    if missing:
        print(f"\n⚠ Missing dependencies: {', '.join(missing)}")
        print("Install them with: pip install " + " ".join(missing))
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("RAG Implementation Test")
    print("=" * 60)
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_data_processing()
    all_passed &= test_dependencies()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! Ready to run setup_rag.py")
    else:
        print("⚠ Some tests failed. Please install missing dependencies first.")
    print("=" * 60)

