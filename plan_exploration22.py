import re

with open('simulation.py', 'r') as f:
    content = f.read()

match = re.search(r'<h2>(.*?)</h2>', content)
if match:
    print(match.group(1))
