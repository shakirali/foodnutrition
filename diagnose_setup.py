"""
Diagnostic script to check why vector database isn't populating correctly.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from data.process_usda_data import load_usda_json, process_all_foods
from data.vector_store import NutritionVectorStore


def diagnose_setup():
    """Diagnose the setup process step by step."""
    
    print("=" * 70)
    print("Diagnosing Vector Database Setup")
    print("=" * 70)
    print()
    
    # Step 1: Check JSON file
    print("Step 1: Checking JSON file")
    print("-" * 70)
    data_dir = Path(__file__).parent / "data"
    json_path = data_dir / "FoodData_Central_foundation_food_json_2025-04-24.json"
    
    if not json_path.exists():
        print(f"✗ JSON file not found at {json_path}")
        return
    print(f"✓ JSON file exists: {json_path}")
    
    # Step 2: Load JSON data
    print("\nStep 2: Loading JSON data")
    print("-" * 70)
    try:
        foods = load_usda_json(json_path)
        print(f"✓ Loaded {len(foods)} food items from JSON")
        if len(foods) == 0:
            print("⚠ Warning: No food items found in JSON!")
            return
    except Exception as e:
        print(f"✗ Error loading JSON: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Process documents
    print("\nStep 3: Processing documents")
    print("-" * 70)
    try:
        documents = process_all_foods(json_path)
        print(f"✓ Processed {len(documents)} documents")
        if len(documents) == 0:
            print("⚠ Warning: No documents created!")
            return
        
        # Check first document structure
        if documents:
            first_doc = documents[0]
            print(f"\nSample document structure:")
            print(f"  - ID: {first_doc.get('id')}")
            print(f"  - Text length: {len(first_doc.get('text', ''))} chars")
            print(f"  - Has metadata: {bool(first_doc.get('metadata'))}")
            if first_doc.get('metadata'):
                meta = first_doc['metadata']
                print(f"  - Description: {meta.get('description', 'N/A')[:50]}...")
                print(f"  - Has full_data: {bool(meta.get('full_data'))}")
    except Exception as e:
        print(f"✗ Error processing documents: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Initialize vector store
    print("\nStep 4: Initializing vector store")
    print("-" * 70)
    try:
        vector_store_path = data_dir / "vector_db"
        vector_store = NutritionVectorStore(vector_store_path)
        print(f"✓ Vector store initialized at {vector_store_path}")
        
        # Check initial count
        initial_count = vector_store.get_collection_count()
        print(f"  Initial collection count: {initial_count}")
    except Exception as e:
        print(f"✗ Error initializing vector store: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 5: Add documents
    print("\nStep 5: Adding documents to vector store")
    print("-" * 70)
    try:
        vector_store.add_documents(documents)
        print(f"✓ Documents added successfully")
    except Exception as e:
        print(f"✗ Error adding documents: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 6: Verify count after adding
    print("\nStep 6: Verifying collection count")
    print("-" * 70)
    try:
        final_count = vector_store.get_collection_count()
        print(f"Final collection count: {final_count}")
        
        if final_count == 0:
            print("⚠ Warning: Count is still 0 after adding documents!")
            print("\nTrying alternative verification methods...")
            
            # Try peek
            try:
                sample = vector_store.collection.peek(limit=5)
                if sample and len(sample.get('ids', [])) > 0:
                    print(f"✓ Peek found {len(sample['ids'])} items")
                    print(f"  Sample IDs: {sample['ids'][:3]}")
                else:
                    print("✗ Peek found no items")
            except Exception as e:
                print(f"✗ Peek failed: {e}")
            
            # Try search
            try:
                results = vector_store.search("test", n_results=1)
                if results:
                    print(f"✓ Search found {len(results)} results")
                else:
                    print("✗ Search found no results")
            except Exception as e:
                print(f"✗ Search failed: {e}")
        else:
            print(f"✓ Success! Collection has {final_count} items")
    except Exception as e:
        print(f"✗ Error verifying count: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 7: Test search
    print("\nStep 7: Testing search functionality")
    print("-" * 70)
    try:
        test_queries = ["apple", "chicken", "bread"]
        for query in test_queries:
            results = vector_store.search(query, n_results=1)
            if results:
                print(f"✓ Search '{query}': Found {len(results)} result(s)")
                print(f"  First result: {results[0]['metadata'].get('description', 'N/A')[:50]}...")
            else:
                print(f"✗ Search '{query}': No results")
    except Exception as e:
        print(f"✗ Error testing search: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("Diagnosis complete!")
    print("=" * 70)


if __name__ == "__main__":
    diagnose_setup()

