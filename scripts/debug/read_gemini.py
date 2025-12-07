
import inspect
from spoon_ai.llm.providers.gemini_provider import GeminiProvider

source = inspect.getsource(GeminiProvider)
lines = source.splitlines()
for i, line in enumerate(lines):
    if "ProviderMetadata" in line:
        # Print surrounding lines
        start = max(0, i - 5)
        end = min(len(lines), i + 15)
        print(f"Around line {i+1}:")
        for j in range(start, end):
            print(f"{j+1}: {lines[j]}")
        print("-" * 20)
