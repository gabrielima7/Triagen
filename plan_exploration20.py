import re

with open('simulation.py', 'r') as f:
    content = f.read()

legend = re.search(r'<p>Red: Rock \|.*?</p>', content)
if legend:
    print(legend.group(0))
