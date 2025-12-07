
import inspect
from spoon_ai.llm.interface import ProviderMetadata

try:
    print(inspect.signature(ProviderMetadata.__init__))
except Exception as e:
    print(f"Error inspecting signature: {e}")

# Also try to grep where it is used in spoon_ai
import spoon_ai.llm.manager
print("\nScanning spoon_ai for ProviderMetadata usage...")
