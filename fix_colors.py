import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Fix duplicates in javascript dictionary
content = re.sub(
    r"            50: '#00ced1', // Deep One\n            51: '#2e8b57', // Dagon\n            50: '#00ced1', // Deep One\n            51: '#2e8b57', // Dagon",
    "            50: '#00ced1', // Deep One\n            51: '#2e8b57', // Dagon",
    content
)

with open('simulation.py', 'w') as f:
    f.write(content)
