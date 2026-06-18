import re

with open('simulation.py', 'r') as f:
    content = f.read()

print("states =", re.search(r'states\s*=\s*\[(.*?)\]', content).group(1))
print("weights =", re.search(r'weights\s*=\s*\[(.*?)\]', content).group(1))
print("chars =", re.search(r'chars\s*=\s*\{(.*?)\}', content).group(1))
