import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Update states list
content = re.sub(
    r'(states = \[[0-9, ]+)49\]',
    r'\g<1>49, 50]',
    content
)

# Update weights list
content = re.sub(
    r'(weights = \[[0-9., ]+)0\.005\]',
    r'\g<1>0.005, 0.005]',
    content
)

with open('simulation.py', 'w') as f:
    f.write(content)
