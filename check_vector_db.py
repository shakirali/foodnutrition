"""
Utility script to check if the vector database has data.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from data.vector_store import NutritionVectorStore


def check_vector_db():
    """Check if vector database has data."""
    
    print("=" * 70)
    print("Checking Vector Database")
    print("=" * 70)
    print()
    
    # Initialize the vector store
    data_dir = Path(__file__).parent / "data"
    vector_store_path = data_dir / "vector_db"
    
    try:
        vector_store = NutritionVectorStore(vector_store_path)
        print("✓ Vector store initialized successfully")
        print()
        
        # Method 1: Check collection count
        print("Method 1: Collection Count")
        print("-" * 70)
        count = vector_store.get_collection_count()
        print(f"Collection count: {count}")
        if count > 0:
            print(f"✓ Database has {count} food items")
        else:
            print("⚠ Collection count shows 0")
        print()
        
        # Method 2: Try to peek at collection
        print("Method 2: Collection Peek")
        print("-" * 70)
        try:
            sample = vector_store.collection.peek(limit=5)
            if sample and len(sample.get('ids', [])) > 0:
                print(f"✓ Found {len(sample['ids'])} sample items in collection")
                print(f"  Sample IDs: {sample['ids'][:3]}...")
                print(f"  Sample descriptions: {[desc[:50] + '...' if len(desc) > 50 else desc for desc in sample.get('documents', [])[:3]]}")
            else:
                print("⚠ Peek returned no data")
        except Exception as e:
            print(f"⚠ Could not peek at collection: {e}")
        print()
        
        # Method 3: Try a test search
        print("Method 3: Test Search")
        print("-" * 70)
        test_queries = ["apple", "chicken", "bread"]
        for query in test_queries:
            try:
                results = vector_store.search(query, n_results=1)
                if results:
                    print(f"✓ Search for '{query}': Found {len(results)} result(s)")
                    print(f"  First result: {results[0]['metadata'].get('description', 'N/A')[:60]}...")
                else:
                    print(f"⚠ Search for '{query}': No results")
            except Exception as e:
                print(f"✗ Search for '{query}': Error - {e}")
        print()
        
        # Method 4: List all collections
        print("Method 4: List Collections")
        print("-" * 70)
        try:
            collections = vector_store.client.list_collections()
            print(f"✓ Found {len(collections)} collection(s):")
            for coll in collections:
                coll_count = coll.count()
                print(f"  - {coll.name}: {coll_count} items")
        except Exception as e:
            print(f"⚠ Could not list collections: {e}")
        print()
        
        # Summary
        print("=" * 70)
        print("Summary")
        print("=" * 70)
        
        has_data = False
        if count > 0:
            has_data = True
            print(f"✓ Vector database HAS DATA: {count} food items")
        else:
            # Check if search works
            test_results = vector_store.search("test", n_results=1)
            if test_results:
                has_data = True
                print("✓ Vector database HAS DATA (confirmed by search, despite count=0)")
            else:
                print("✗ Vector database appears to be EMPTY")
                print("\nTo populate the database, run:")
                print("  python scripts/setup_rag.py")
        
        return has_data
        
    except ImportError as e:
        print(f"✗ Missing dependencies: {e}")
        print("\nPlease install required dependencies:")
        print("  pip install chromadb sentence-transformers")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    check_vector_db()

