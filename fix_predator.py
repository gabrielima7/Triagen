import re

with open('simulation.py', 'r') as f:
    content = f.read()

content = content.replace("predator_states = [, 60]", "predator_states = []")

with open('simulation.py', 'w') as f:
    f.write(content)
