
import inspect
from spoon_ai.llm.providers.gemini_provider import GeminiProvider

try:
    source = inspect.getsource(GeminiProvider)
    # Print first 100 lines to see init and generate
    print("\n".join(source.splitlines()[:100]))
except Exception as e:
    print(f"Could not get source: {e}")
