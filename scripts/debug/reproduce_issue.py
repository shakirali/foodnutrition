
import traceback
import sys
import os

# Add current dir to path
sys.path.append(os.getcwd())

try:
    print("Importing...")
    from agents.advisor_agent import NutritionAdvisorAgent
    from spoon_ai.chat import ChatBot
    
    # minimal mock for AppConfig if needed, but we pass string to llm_provider
    
    print("Instantiating Agent...")
    agent = NutritionAdvisorAgent(
        llm=ChatBot(llm_provider="gemini")
    )
    print("Success!")
except Exception:
    traceback.print_exc()
