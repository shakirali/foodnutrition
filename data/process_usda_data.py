"""Process USDA FoodData Central JSON data into searchable documents."""
import json
from pathlib import Path
from typing import List, Dict


def load_usda_json(json_path: Path) -> List[Dict]:
    """Load USDA JSON data."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('FoundationFoods', [])


def create_document(food_item: Dict) -> Dict:
    """Convert food item to a searchable document."""
    # Extract key information
    fdc_id = food_item.get('fdcId', '')
    description = food_item.get('description', '')
    food_class = food_item.get('foodClass', '')
    food_category = food_item.get('foodCategory', {})
    category_desc = food_category.get('description', '') if isinstance(food_category, dict) else ''
    
    # Build nutrient summary - prioritize important nutrients
    nutrients = food_item.get('foodNutrients', [])
    nutrient_text = []
    
    # Common important nutrients to prioritize
    important_nutrients = [
        'Energy', 'Protein', 'Total lipid (fat)', 'Carbohydrate, by difference',
        'Fiber, total dietary', 'Calcium', 'Iron', 'Vitamin C', 'Vitamin A',
        'Sodium', 'Sugars, total including NLEA'
    ]
    
    # First, add important nutrients
    for nutrient in nutrients:
        nutrient_name = nutrient.get('nutrient', {}).get('name', '')
        if nutrient_name in important_nutrients:
            amount = nutrient.get('amount', 0)
            unit = nutrient.get('nutrient', {}).get('unitName', '')
            if amount is not None and amount != 0:
                nutrient_text.append(f"{nutrient_name}: {amount} {unit}")
    
    # Then add other nutrients (limit to avoid too long text)
    for nutrient in nutrients:
        nutrient_name = nutrient.get('nutrient', {}).get('name', '')
        if nutrient_name not in important_nutrients and len(nutrient_text) < 15:
            amount = nutrient.get('amount', 0)
            unit = nutrient.get('nutrient', {}).get('unitName', '')
            if amount is not None and amount != 0:
                nutrient_text.append(f"{nutrient_name}: {amount} {unit}")
    
    # Create searchable text
    searchable_text = f"""
    Food: {description}
    Category: {category_desc}
    Food Class: {food_class}
    FDC ID: {fdc_id}
    Nutrients: {', '.join(nutrient_text)}
    """
    
    return {
        'id': str(fdc_id),
        'text': searchable_text.strip(),
        'metadata': {
            'fdc_id': fdc_id,
            'description': description,
            'food_class': food_class,
            'category': category_desc,
            # Note: full_data is not stored here due to ChromaDB metadata size limits
            # Full data is loaded on-demand from the original JSON file using fdc_id
        }
    }


def process_all_foods(json_path: Path) -> List[Dict]:
    """Process all food items into documents."""
    foods = load_usda_json(json_path)
    documents = []
    
    print(f"Processing {len(foods)} food items...")
    for food in foods:
        doc = create_document(food)
        documents.append(doc)
    
    return documents

