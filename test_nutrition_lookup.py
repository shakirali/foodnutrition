"""
Test script for NutritionLookupTool
Tests the tool with different food queries to verify it returns nutritional values.
This test directly uses the vector store to avoid SpoonOS dependencies.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from data.vector_store import NutritionVectorStore


def format_nutrition_results(results, query):
    """Format search results similar to NutritionLookupTool."""
    if not results:
        return f"No nutritional information found for '{query}'. Try a different search term."
    
    # Format response
    response_parts = [f"Found {len(results)} result(s) for '{query}':\n"]
    
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


def test_nutrition_lookup():
    """Test nutrition lookup with different food queries."""
    
    print("=" * 70)
    print("Testing Nutrition Lookup (Vector Store)")
    print("=" * 70)
    print()
    
    # Initialize the vector store
    data_dir = Path(__file__).parent / "data"
    vector_store_path = data_dir / "vector_db"
    
    try:
        vector_store = NutritionVectorStore(vector_store_path)
        print("✓ Vector store initialized successfully")
        
        # Check if database has data
        # Note: count() may sometimes return 0 even if data exists (ChromaDB quirk)
        # We'll proceed with tests regardless - the search results will show if data exists
        count = vector_store.get_collection_count()
        if count > 0:
            print(f"✓ Vector database contains {count} food items")
        else:
            print("⚠ Collection count shows 0 (may be a ChromaDB display issue)")
            print("  Proceeding with tests - search results will confirm if data exists")
        
    except ImportError as e:
        print(f"✗ Missing dependencies: {e}")
        print("\nPlease install required dependencies:")
        print("  pip install chromadb sentence-transformers")
        print("\nOr install all project dependencies:")
        print("  pip install -r requirements.txt")
        return
    except Exception as e:
        print(f"✗ Failed to initialize vector store: {e}")
        print("\nMake sure you have:")
        print("1. Run 'python scripts/setup_rag.py' to set up the vector database")
        print("2. Installed all dependencies: pip install -r requirements.txt")
        import traceback
        traceback.print_exc()
        return
    
    print()
    
    # Test queries
    test_queries = [
        "Humus",   # User requested
        "eggs",    # User requested
        "Summed",  # User requested
        "hummus",  # Try alternative spelling
        "egg",     # Try singular
    ]
    
    for query in test_queries:
        print("-" * 70)
        print(f"Testing query: '{query}'")
        print("-" * 70)
        
        try:
            results = vector_store.search(query, n_results=5)
            formatted_result = format_nutrition_results(results, query)
            print(formatted_result)
        except Exception as e:
            print(f"✗ Error executing query '{query}': {e}")
            import traceback
            traceback.print_exc()
        
        print()
    
    print("=" * 70)
    print("Test completed!")
    print("=" * 70)


if __name__ == "__main__":
    test_nutrition_lookup()
