"""
Nutrition-Based Local Food Advisor App
Main Entry Point
"""

import asyncio

from config import AppConfig
from agents.advisor_agent import NutritionAdvisorAgent
from spoon_ai.chat import ChatBot


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

