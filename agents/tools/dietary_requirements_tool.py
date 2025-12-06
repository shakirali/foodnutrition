"""Dietary requirements lookup tool for querying minerals, vitamins, and nutrition recommendations."""
from spoon_ai.tools.base import BaseTool
from data.dietary_vector_store import DietaryRequirementsVectorStore
from data.process_dietary_data import get_age_group
from pathlib import Path
from typing import Optional
from pydantic import PrivateAttr
import re


class DietaryRequirementsTool(BaseTool):
    """Tool for looking up dietary requirements (minerals, vitamins, nutrition) by age and gender."""
    
    name: str = "dietary_requirements"
    description: str = (
        "Look up dietary requirements including minerals, vitamins, and nutrition recommendations "
        "based on age and gender. Use this tool when users ask about daily nutrient requirements, "
        "recommended intake, dietary guidelines, or what nutrients they need (e.g., 'What are the "
        "requirements for a 30-year-old male?', 'How much iron does a 25-year-old female need?', "
        "'What vitamins should a 15-year-old get?')."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query about dietary requirements. Can include age, gender, or specific nutrients (e.g., 'requirements for 30-year-old male', 'iron needs for female 25', 'vitamins for age 15')"
            },
            "age": {
                "type": "integer",
                "description": "Optional: User's age (will be used for precise matching if provided)",
                "minimum": 1,
                "maximum": 120
            },
            "gender": {
                "type": "string",
                "description": "Optional: User's gender ('male' or 'female')",
                "enum": ["male", "female"]
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return (default: 5, max: 10)",
                "default": 5,
                "minimum": 1,
                "maximum": 10
            }
        },
        "required": ["query"]
    }
    
    # Use PrivateAttr for internal implementation details
    _vector_store: Optional[DietaryRequirementsVectorStore] = PrivateAttr(default=None)
    
    def __init__(self, vector_store: Optional[DietaryRequirementsVectorStore] = None, **kwargs):
        super().__init__(**kwargs)
        if vector_store is None:
            # Initialize vector store if not provided
            data_dir = Path(__file__).parent.parent.parent / "data"
            vector_store_path = data_dir / "dietary_vector_db"
            mineral_path = data_dir / "mineral_requirements.json"
            vitamin_path = data_dir / "vitamin_recommendations.json"
            nutrition_path = data_dir / "nutrition_recommendations.json"
            self._vector_store = DietaryRequirementsVectorStore(
                vector_store_path,
                mineral_path=mineral_path,
                vitamin_path=vitamin_path,
                nutrition_path=nutrition_path
            )
        else:
            self._vector_store = vector_store
    
    @property
    def vector_store(self) -> DietaryRequirementsVectorStore:
        """Get the vector store instance."""
        if self._vector_store is None:
            # Lazy initialization if somehow not set
            data_dir = Path(__file__).parent.parent.parent / "data"
            vector_store_path = data_dir / "dietary_vector_db"
            mineral_path = data_dir / "mineral_requirements.json"
            vitamin_path = data_dir / "vitamin_recommendations.json"
            nutrition_path = data_dir / "nutrition_recommendations.json"
            self._vector_store = DietaryRequirementsVectorStore(
                vector_store_path,
                mineral_path=mineral_path,
                vitamin_path=vitamin_path,
                nutrition_path=nutrition_path
            )
        return self._vector_store
    
    def _extract_age_from_query(self, query: str) -> Optional[int]:
        """Extract age from query text."""
        # Look for patterns like "30-year-old", "age 30", "30 years old", etc.
        patterns = [
            r'(\d+)[-\s]year[-\s]old',
            r'age[-\s](\d+)',
            r'aged[-\s](\d+)',
            r'(\d+)[-\s]years[-\s]old',
            r'\b(\d+)\b'  # Any number (less precise, use as fallback)
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                try:
                    age = int(match.group(1))
                    if 1 <= age <= 120:  # Reasonable age range
                        return age
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _extract_gender_from_query(self, query: str) -> Optional[str]:
        """Extract gender from query text."""
        query_lower = query.lower()
        if 'male' in query_lower or 'man' in query_lower or 'boy' in query_lower:
            return "male"
        elif 'female' in query_lower or 'woman' in query_lower or 'girl' in query_lower:
            return "female"
        return None
    
    def _format_nutrient_value(self, value, key: str) -> str:
        """Format nutrient value for display."""
        if value is None:
            return "not specified"
        if isinstance(value, dict):
            # Handle special case like iron for females 19-64
            return ", ".join([f"{k}: {v}" for k, v in value.items()])
        if isinstance(value, str):
            # Handle range strings like "3.0-5.0"
            return value
        
        # Extract unit from key
        if '_' in key:
            unit = key.split('_')[-1]
            return f"{value} {unit}"
        return str(value)
    
    async def execute(
        self,
        query: str,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        max_results: int = 5
    ) -> str:
        """Execute the dietary requirements lookup."""
        try:
            # Validate max_results
            max_results = min(max(1, max_results), 10)
            
            # Extract age and gender from query if not provided
            if age is None:
                age = self._extract_age_from_query(query)
            if gender is None:
                gender = self._extract_gender_from_query(query)
            
            # Try exact match first if we have both age and gender
            exact_match = None
            if age and gender:
                age_group = get_age_group(age)
                exact_match = self.vector_store.get_requirements_by_key(age_group, gender)
            
            # Perform semantic search
            results = self.vector_store.search(query, n_results=max_results)
            
            # If we have exact match, prioritize it
            if exact_match:
                # Format exact match response
                response_parts = [
                    f"Dietary Requirements for {gender.capitalize()}, Age {age} (Age Group: {exact_match['age_group']})\n"
                ]
                
                # Format minerals
                if exact_match['minerals']:
                    response_parts.append("\nMINERALS:")
                    for key, value in exact_match['minerals'].items():
                        formatted_value = self._format_nutrient_value(value, key)
                        nutrient_name = key.replace('_', ' ').title()
                        response_parts.append(f"  - {nutrient_name}: {formatted_value}")
                
                # Format vitamins
                if exact_match['vitamins']:
                    response_parts.append("\nVITAMINS:")
                    for key, value in exact_match['vitamins'].items():
                        formatted_value = self._format_nutrient_value(value, key)
                        nutrient_name = key.replace('_', ' ').title()
                        response_parts.append(f"  - {nutrient_name}: {formatted_value}")
                
                # Format nutrition
                if exact_match['nutrition']:
                    response_parts.append("\nNUTRITION (Macronutrients):")
                    for key, value in exact_match['nutrition'].items():
                        formatted_value = self._format_nutrient_value(value, key)
                        nutrient_name = key.replace('_', ' ').title()
                        response_parts.append(f"  - {nutrient_name}: {formatted_value}")
                
                return "\n".join(response_parts)
            
            # Fallback to semantic search results
            if not results:
                return f"No dietary requirements found for '{query}'. Try specifying age and gender (e.g., 'requirements for 30-year-old male')."
            
            # Format semantic search results
            response_parts = [f"Found {len(results)} result(s) for '{query}':\n"]
            
            for i, result in enumerate(results, 1):
                metadata = result['metadata']
                age_group = metadata.get('age_group', 'Unknown')
                gender_result = metadata.get('gender', 'Unknown')
                
                # Try to get full data
                full_data = self.vector_store.get_requirements_by_key(age_group, gender_result)
                
                if full_data:
                    response_parts.append(f"\n{i}. {gender_result.capitalize()}, Age Group: {age_group}")
                    
                    # Add summary of key nutrients
                    if full_data['minerals']:
                        key_minerals = list(full_data['minerals'].keys())[:3]
                        response_parts.append(f"   Key Minerals: {', '.join([k.replace('_', ' ').title() for k in key_minerals])}")
                    
                    if full_data['vitamins']:
                        key_vitamins = list(full_data['vitamins'].keys())[:3]
                        response_parts.append(f"   Key Vitamins: {', '.join([k.replace('_', ' ').title() for k in key_vitamins])}")
                else:
                    response_parts.append(f"\n{i}. {gender_result.capitalize()}, Age Group: {age_group}")
            
            return "\n".join(response_parts)
            
        except Exception as e:
            return f"Error looking up dietary requirements: {str(e)}"

