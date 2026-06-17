import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Update states
content = re.sub(
    r'(states = \[.*?)(\])',
    r'\1, 57, 58\2',
    content, count=1
)

# Update weights
content = re.sub(
    r'(weights = \[.*?)(\])',
    r'\1, 0.005, 0.005\2',
    content, count=1
)

# Update comment
content = re.sub(
    r'(# Weighted choice: .*?)( Dagon \(0\.005\%\))',
    r'\1\2, Yithian (0.005%), Flying Polyp (0.005%)',
    content, count=1
)

# Update chars
content = re.sub(
    r'(chars = \{.*?)(56: "c"\}|\'c\'\})',
    r'\1 56: "c", 57: "y", 58: "F"}',
    content, count=1
)

# Update blocking_states
content = re.sub(
    r'(blocking_states = \{.*?)(\})',
    r'\1, 57, 58\2',
    content, count=1
)

# Update HTML colors
content = re.sub(
    r"(56: '#708090'  // Brain Cylinder)",
    r"56: '#708090',  // Brain Cylinder\n            57: '#D2B48C', // Yithian\n            58: '#483D8B'  // Flying Polyp",
    content, count=1
)

with open('simulation.py', 'w') as f:
    f.write(content)
