import re

with open('simulation.py', 'r') as f:
    content = f.read()

colors = re.search(r'const colors = \{(.*?)\}', content, re.DOTALL).group(1)
print(colors)
