import re

with open('simulation.py', 'r') as f:
    content = f.read()

states_to_add = [60]
weights_to_add = [0.005]

states = re.search(r'states\s*=\s*\[(.*?)\]', content).group(1)
weights = re.search(r'weights\s*=\s*\[(.*?)\]', content).group(1)

new_states = states + ", 60"
new_weights = weights + ", 0.005"

print(f"new_states: {new_states}")
print(f"new_weights: {new_weights}")
