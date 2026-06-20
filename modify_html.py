import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Update p tag
content = content.replace(
    'Sienna: Dark Young | Fuchsia: The Color Out of Space',
    'Sienna: Dark Young | DarkTurquoise: Deep One | SeaGreen: Dagon | Fuchsia: The Color Out of Space'
)

# Update javascript dictionary
content = re.sub(
    r"49: '#a0522d', // Dark Young",
    "49: '#a0522d',\n            50: '#00ced1', // Deep One\n            51: '#2e8b57', // Dagon",
    content
)

with open('simulation.py', 'w') as f:
    f.write(content)
