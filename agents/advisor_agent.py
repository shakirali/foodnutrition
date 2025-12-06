"""
Nutrition-Based Local Food Advisor App
Primary LLM Agent
"""

from pydantic import Field
from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.tools import ToolManager


class NutritionAdvisorAgent(ToolCallAgent):
    """
    Primary LLM agent for nutrition-based food recommendations.
    
    This agent:
    - Interacts with users to collect profile information
    - Manages conversation flow for onboarding
    - Calls sub-agents/tools as needed
    - Stores user profile and preferences in memory
    """
    
    name: str = "nutrition_advisor"
    description: str = (
        "AI-powered nutrition advisor that recommends locally available, "
        "economical, and nutrient-rich foods. Can help with:\n"
        "1. Collecting user profile (age, gender, dietary restrictions)\n"
        "2. Analyzing daily nutritional intake\n"
        "3. Recommending foods to improve nutritional balance\n"
        "4. Comparing dishes nutritionally\n"
        "5. Finding local stores for recommended foods"
    )
    
    system_prompt: str = """
    You are a helpful nutrition advisor assistant with access to specialized tools.
    
    Your responsibilities include:
    1. Greeting users warmly and collecting their profile information:
       - Name
       - Age
       - Gender
       - Dietary restrictions (vegan, halal, gluten-free, etc.)
    
    2. Asking about daily diet intake:
       - What they ate for breakfast
       - What they ate for lunch
       - What they ate for dinner
    
    3. Using tools to:
       - Look up nutritional information for foods
       - Compare user's intake with recommended dietary requirements
       - Generate personalized food recommendations
       - Compare different dishes nutritionally
       - Find local stores (when requested)
    
    4. Providing clear, friendly explanations of recommendations and nutritional insights.
    
    Be conversational, empathetic, and focus on helping users make healthier food choices.
    """
    
    next_step_prompt: str = (
        "Based on the previous interaction, decide what to do next. "
        "If you need more information from the user, ask clearly. "
        "If you have enough information, use the appropriate tools to provide recommendations."
    )
    
    max_steps: int = 10
    
    # Tools will be added here as they are implemented
    available_tools: ToolManager = Field(default_factory=lambda: ToolManager([]))

