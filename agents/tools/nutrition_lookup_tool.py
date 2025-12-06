"""Nutrition lookup tool for querying USDA FoodData Central database."""
from spoon_ai.tools.base import BaseTool
from data.vector_store import NutritionVectorStore
from pathlib import Path
from typing import Optional
from pydantic import PrivateAttr


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
    
    # Use PrivateAttr for internal implementation details
    _vector_store: Optional[NutritionVectorStore] = PrivateAttr(default=None)
    
    def __init__(self, vector_store: Optional[NutritionVectorStore] = None, **kwargs):
        super().__init__(**kwargs)
        if vector_store is None:
            # Initialize vector store if not provided
            data_dir = Path(__file__).parent.parent.parent / "data"
            vector_store_path = data_dir / "vector_db"
            json_path = data_dir / "FoodData_Central_foundation_food_json_2025-04-24.json"
            self._vector_store = NutritionVectorStore(vector_store_path, json_path=json_path)
        else:
            self._vector_store = vector_store
    
    @property
    def vector_store(self) -> NutritionVectorStore:
        """Get the vector store instance."""
        if self._vector_store is None:
            # Lazy initialization if somehow not set
            data_dir = Path(__file__).parent.parent.parent / "data"
            vector_store_path = data_dir / "vector_db"
            json_path = data_dir / "FoodData_Central_foundation_food_json_2025-04-24.json"
            self._vector_store = NutritionVectorStore(vector_store_path, json_path=json_path)
        return self._vector_store
    
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
                fdc_id = metadata.get('fdc_id')
                
                # Load full data using FDC ID
                full_data = self.vector_store.get_food_by_id(fdc_id) if fdc_id else {}
                
                # Extract key nutrients
                nutrients = full_data.get('foodNutrients', []) if full_data else []
                
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

