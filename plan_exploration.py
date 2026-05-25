import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Let's verify line numbers for states list
states_match = re.search(r'states = \[(.*?)\]', content)
if states_match:
    print(f"states found: {states_match.group(0)}")

weights_match = re.search(r'weights = \[(.*?)\]', content)
if weights_match:
    print(f"weights found: {weights_match.group(0)}")
