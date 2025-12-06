
import os
import inspect
import spoon_ai
from spoon_ai.llm.interface import ProviderMetadata

print(f"ProviderMetadata Location: {inspect.getfile(ProviderMetadata)}")

root_path = os.path.dirname(spoon_ai.__file__)
for root, dirs, files in os.walk(root_path):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if "ProviderMetadata(" in content:
                        print(f"Found in {path}")
                        # Print context
                        lines = content.splitlines()
                        for i, line in enumerate(lines):
                            if "ProviderMetadata(" in line:
                                print(f"{i+1}: {line.strip()}")
            except Exception as e:
                pass
