import re
with open('simulation.py', 'r') as f:
    content = f.read()

m = re.search(r'weights = \[(.*?)\]', content)
if m:
    weights = m.group(1).split(',')
    print(len(weights))
