"""Process dietary requirements JSON data (minerals, vitamins, nutrition) into searchable documents."""
import json
from pathlib import Path
from typing import List, Dict


def get_age_group(age: int) -> str:
    """Map age to age group string."""
    age_ranges = [
        (1, 1, "1"),
        (2, 3, "2-3"),
        (4, 6, "4-6"),
        (7, 10, "7-10"),
        (11, 14, "11-14"),
        (15, 18, "15-18"),
        (19, 64, "19-64"),
        (65, 74, "65-74"),
        (75, float('inf'), "75+")
    ]
    
    for min_age, max_age, group in age_ranges:
        if min_age <= age <= max_age:
            return group
    
    return "75+"  # Fallback


def load_dietary_json(json_path: Path) -> Dict:
    """Load dietary requirements JSON data."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_nutrient_value(value, unit: str = "") -> str:
    """Format nutrient value for display."""
    if value is None:
        return "not specified"
    if isinstance(value, dict):
        # Handle special case like iron for females 19-64
        return ", ".join([f"{k}: {v}" for k, v in value.items()])
    if isinstance(value, str):
        # Handle range strings like "3.0-5.0"
        return value
    return f"{value} {unit}".strip()


def create_unified_document(
    age_group: str,
    gender: str,
    minerals: Dict,
    vitamins: Dict,
    nutrition: Dict
) -> Dict:
    """Create a unified document combining all three datasets for an age group and gender."""
    
    # Add minerals
    mineral_text = []
    for key, value in minerals.items():
        # Extract unit from key (e.g., "iron_mg" -> "mg")
        unit = key.split('_')[-1] if '_' in key else ""
        formatted_value = format_nutrient_value(value, unit)
        mineral_text.append(f"{key.replace('_', ' ')}: {formatted_value}")
    
    # Add vitamins
    vitamin_text = []
    for key, value in vitamins.items():
        unit = key.split('_')[-1] if '_' in key else ""
        formatted_value = format_nutrient_value(value, unit)
        vitamin_text.append(f"{key.replace('_', ' ')}: {formatted_value}")
    
    # Add nutrition/macronutrients
    nutrition_text = []
    for key, value in nutrition.items():
        unit = key.split('_')[-1] if '_' in key else ""
        formatted_value = format_nutrient_value(value, unit)
        nutrition_text.append(f"{key.replace('_', ' ')}: {formatted_value}")
    
    # Create comprehensive searchable text
    searchable_text = f"""
    Age group: {age_group}
    Gender: {gender}
    
    Minerals: {', '.join(mineral_text)}
    
    Vitamins: {', '.join(vitamin_text)}
    
    Nutrition (Macronutrients): {', '.join(nutrition_text)}
    """
    
    # Create unique document ID
    doc_id = f"dietary_{age_group}_{gender}"
    
    return {
        'id': doc_id,
        'text': searchable_text.strip(),
        'metadata': {
            'age_group': age_group,
            'gender': gender,
            'dataset_type': 'unified_dietary_requirements'
        },
        'full_data': {
            'age_group': age_group,
            'gender': gender,
            'minerals': minerals,
            'vitamins': vitamins,
            'nutrition': nutrition
        }
    }


def process_all_dietary_data(
    mineral_path: Path,
    vitamin_path: Path,
    nutrition_path: Path
) -> List[Dict]:
    """Process all three dietary requirements JSON files into unified documents."""
    
    # Load all three datasets
    print("Loading dietary requirements data...")
    minerals_data = load_dietary_json(mineral_path)
    vitamins_data = load_dietary_json(vitamin_path)
    nutrition_data = load_dietary_json(nutrition_path)
    
    documents = []
    
    # Get all age groups (should be the same across all three datasets)
    age_groups = set(minerals_data.keys()) | set(vitamins_data.keys()) | set(nutrition_data.keys())
    genders = ["male", "female"]
    
    print(f"Processing {len(age_groups)} age groups × {len(genders)} genders = {len(age_groups) * len(genders)} documents...")
    
    # Create unified documents for each age group and gender combination
    for age_group in sorted(age_groups):
        for gender in genders:
            # Get data for this age group and gender from each dataset
            minerals = minerals_data.get(age_group, {}).get(gender, {})
            vitamins = vitamins_data.get(age_group, {}).get(gender, {})
            nutrition = nutrition_data.get(age_group, {}).get(gender, {})
            
            # Skip if no data available
            if not (minerals or vitamins or nutrition):
                continue
            
            # Create unified document
            doc = create_unified_document(age_group, gender, minerals, vitamins, nutrition)
            documents.append(doc)
    
    return documents

