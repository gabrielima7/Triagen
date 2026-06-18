import re

with open('simulation.py', 'r') as f:
    content = f.read()

for match in re.finditer(r'(<div.*?>.*?</div>)', content, re.DOTALL):
    if "Rock" in match.group(1):
        print(match.group(1)[:100])
        break
else:
    print("Not found")
