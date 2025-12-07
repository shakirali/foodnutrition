
import inspect
from spoon_ai.agents.toolcall import ToolCallAgent

lines = inspect.getsource(ToolCallAgent).splitlines()
for i, line in enumerate(lines[:50]):
    print(f"{i+1}: {line}")
