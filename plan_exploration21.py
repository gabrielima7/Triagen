import re

with open('simulation.py', 'r') as f:
    content = f.read()

chars = re.search(r'chars\s*=\s*\{(.*?)\}', content).group(1)
if "60:" not in chars:
    print("Character for 60 is missing.")
else:
    print("Character 60 exists")
