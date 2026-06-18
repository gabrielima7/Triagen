import re

with open('simulation.py', 'r') as f:
    content = f.read()

states = re.search(r'states\s*=\s*\[(.*?)\]', content).group(1)
print(states)
