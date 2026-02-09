import os
import re
from collections import defaultdict

def analyze_css(start_path):
    # Regex to find class selectors: .classname {
    class_pattern = re.compile(r'\.([a-zA-Z0-9_-]+)\s*\{')
    
    class_definitions = defaultdict(list)
    
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith(".css"):
                file_path = os.path.join(root, file)
                
                # Exclusion logic
                if "themes" in file_path or "accessibility" in file_path:
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Remove comments to avoid false positives
                        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
                        
                        matches = class_pattern.findall(content)
                        for class_name in matches:
                            class_definitions[class_name].append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # specific interesting conflicts (e.g. against bootstrap)
    # We can't easily check against bootstrap CDN, but we can check internal dupes
    
    conflicts = {k: v for k, v in class_definitions.items() if len(set(v)) > 1}
    
    if not conflicts:
        print("No duplicate class definitions found across files.")
    else:
        print(f"Found {len(conflicts)} potential class conflicts (defined in >1 file):")
        # Sort by number of occurrences
        for class_name, paths in sorted(conflicts.items(), key=lambda item: len(set(item[1])), reverse=True)[:20]:
            print(f"\n.{class_name}:")
            unique_paths = list(set(paths))
            for p in unique_paths:
                rel_path = os.path.relpath(p, start_path)
                print(f"  - {rel_path}")

if __name__ == "__main__":
    import sys
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    analyze_css(base_path)
