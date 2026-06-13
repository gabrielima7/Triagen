import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Update h2 tag
content = content.replace(
    'Yog-Sothoth, Hastur & Yellow Sign</h2>',
    'Yog-Sothoth, Hastur & Yellow Sign, Shub-Niggurath & Dark Young</h2>'
)

# Update p tag
content = content.replace(
    'Yellow: Yellow Sign</p>',
    'Yellow: Yellow Sign | Teal: Shub-Niggurath | Sienna: Dark Young</p>'
)

# Update javascript dictionary
content = re.sub(
    r"47: '#ffff00'  // Yellow Sign",
    "47: '#ffff00', // Yellow Sign\n            48: '#008080', // Shub-Niggurath\n            49: '#a0522d'  // Dark Young",
    content
)

with open('simulation.py', 'w') as f:
    f.write(content)
