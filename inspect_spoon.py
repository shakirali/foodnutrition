
from spoon_ai.agents.toolcall import ToolCallAgent
from pydantic import BaseModel

print("--- ToolCallAgent Fields ---")
for name, field in ToolCallAgent.model_fields.items():
    print(f"{name}: {field.annotation} (default: {field.default})")

print("\n--- ToolCallAgent Validators ---")
# This might be harder to see on pydantic v2
try:
    print(ToolCallAgent.__pydantic_decorators__)
except:
    pass
