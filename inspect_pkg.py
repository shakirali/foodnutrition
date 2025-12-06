
import os
import spoon_ai

root_path = os.path.dirname(spoon_ai.__file__)
print(f"Searching in: {root_path}")

for root, dirs, files in os.walk(root_path):
    for f in files:
        if f.endswith(".py"):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, root_path)
            print(f"FILE: {rel_path}")
