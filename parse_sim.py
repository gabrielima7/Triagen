import re

with open('simulation.py', 'r') as f:
    content = f.read()

blocking = re.search(r'blocking_states\s*=\s*\{(.*?)\}', content).group(1)
print(blocking)
