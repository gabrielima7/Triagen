import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Append to states array
content = re.sub(r'(states\s*=\s*\[.*?)(])', r'\1, 60\2', content)

# Append to weights array
content = re.sub(r'(weights\s*=\s*\[.*?)(])', r'\1, 0.005\2', content)

# Append to chars dictionary
content = re.sub(r'(chars\s*=\s*\{.*?)(})', r'\1, 60: "E"\2', content)

# Append to blocking_states set
content = re.sub(r'(blocking_states\s*=\s*\{.*?)(})', r'\1, 60\2', content)

with open('simulation.py', 'w') as f:
    f.write(content)
