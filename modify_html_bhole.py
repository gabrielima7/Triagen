import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Update colors dictionary
content = re.sub(
    r"62: '#5c4033' // Gug",
    "62: '#5c4033', // Gug\n            63: '#9acd32'  // Bhole",
    content
)

# Update h2 tag
content = content.replace(
    'Hound of Tindalos, Elder Thing, Nightgaunt, Gug</h2>',
    'Hound of Tindalos, Elder Thing, Nightgaunt, Gug, Bhole</h2>'
)

# Update p tag
content = content.replace(
    'Midnight Blue: Hound of Tindalos | SeaGreen: Elder Thing | Indigo: Nightgaunt | Dark Brown: Gug</p>',
    'Midnight Blue: Hound of Tindalos | SeaGreen: Elder Thing | Indigo: Nightgaunt | Dark Brown: Gug | YellowGreen: Bhole</p>'
)

with open('simulation.py', 'w') as f:
    f.write(content)
