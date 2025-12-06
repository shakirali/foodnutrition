"""
Nutrition-Based Local Food Advisor App
Primary LLM Agent
"""

from pydantic import Field
from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.tools import ToolManager
from agents.tools.nutrition_lookup_tool import NutritionLookupTool
from agents.tools.web_search_tool import WebSearchTool


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
    You are a helpful nutrition advisor assistant.
    
    TOOL USAGE GUIDELINES (STRICT):
    1. Nutritional Inquiries:
       - FIRST, always check the local database (`nutrition_lookup`).
       - Use `web_search` ONLY if local data is missing (especially for branded items).
    
    2. Store/Location Inquiries:
       - Search for **GROCERY STORES** or **SUPERMARKETS** (Tesco, Sainsbury's, Waitrose, etc.).
       - AVOID restaurants unless requested.
       - MUST ask for location (City/Zip) if unknown.
    
    WORKFLOW (STRICT):
    When the user provides their profile and daily intake, you MUST follow this structure:
    
    1. **Nutritional Analysis (RDI Check)**:
       - Analyze their Breakfast, Lunch, and Dinner.
       - Compare their estimated intake against the **Recommended Daily Intake (RDI)** for their Age and Gender.
       - Explicitly state if they are meeting requirements (e.g., "For a 23-year-old male, your protein intake looks good, but you are likely low on Fiber and Vitamin C").
    
    2. **Identify Nutritional Gaps**:
       - Clearly list what is missing or excessive (e.g., "Gap: Low Iron", "Gap: High Saturated Fat").
    
    3. **Corrective Recommendation & Shopping List**:
       - For each gap, recommend **SPECIFIC PRODUCTS** to buy at grocery stores (Tesco, Sainsbury's, Waitrose, etc.).
       - **Format**: [Nutrient Needed] -> [Specific Product to Buy]
       - Example: "To increase Fiber: Buy 'Tesco Wholemeal Bread' or 'Sainsbury's Organic Oats'."
       - Example: "To reduce Saturated Fat: Switch to 'Alpro Unsweetened Almond Milk' available at Waitrose."
    
    Your responsibilities:
    1. Onboarding: Collect Name, Age, Gender, Diet, Location.
    2. Execution: Perform the RDI Analysis and generate the Shopping List described above.
    
    Be conversational but structured. Focus on actionable shopping advice.
    """
    
    next_step_prompt: str = (
        "Based on the previous interaction, decide what to do next. "
        "If you need more information from the user, ask clearly. "
        "If you have enough information, use the appropriate tools to provide recommendations."
    )
    
    max_steps: int = 10
    
    # Tools for nutrition lookup
    avaliable_tools: ToolManager = Field(
        default_factory=lambda: ToolManager([
            NutritionLookupTool(),
            WebSearchTool()
        ])
    )

