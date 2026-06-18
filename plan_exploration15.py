import re

with open('simulation.py', 'r') as f:
    content = f.read()

legend = re.search(r'Legend:(.*?)</div>', content, re.DOTALL).group(1)
print(legend)
