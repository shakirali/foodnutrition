"""
Nutrition-Based Local Food Advisor App
Primary LLM Agent - Main Entry Point
"""

import asyncio
import sys
from pathlib import Path
from pydantic import Field

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import AppConfig
from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.chat import ChatBot
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


async def run_conversation_loop(agent: NutritionAdvisorAgent):
    """
    Main conversation loop for user interaction.
    
    Args:
        agent: The primary agent instance
    """
    print("\n" + "="*60)
    print("Welcome to the Nutrition-Based Local Food Advisor!")
    print("="*60)
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    # Reset the agent state
    agent.clear()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nThank you for using the Nutrition Advisor. Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Process user input through agent
            print("\n🤖 Agent is processing your request...")
            response = await agent.run(user_input)
            print(f"\n📋 Nutrition Advisor: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nConversation interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again or type 'exit' to quit.\n")


async def main():
    """Main entry point for the Nutrition Advisor application."""
    print("Initializing Nutrition-Based Local Food Advisor App...")
    print(AppConfig.get_summary())
    
    try:
        # Validate configuration
        AppConfig.validate()
        
        # Create the primary agent with LLM configuration
        agent = NutritionAdvisorAgent(
            llm=ChatBot(
                llm_provider=AppConfig.DEFAULT_LLM_PROVIDER
            )
        )
        
        print("✓ Agent initialized successfully!")
        print("✓ Using default LLM provider:", AppConfig.DEFAULT_LLM_PROVIDER)
        
        # Start conversation loop
        await run_conversation_loop(agent)
        
    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease install the required dependencies:")
        print("  pip install spoon-ai-sdk")
    except Exception as e:
        print(f"Error initializing agent: {e}")


if __name__ == "__main__":
    asyncio.run(main())

