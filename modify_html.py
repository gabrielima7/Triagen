with open('simulation.py', 'r') as f:
    text = f.read()

text = text.replace(
    'Shub-Niggurath & Dark Young</h2>',
    'Shub-Niggurath & Dark Young, Deep One</h2>'
)
text = text.replace(
    '| Sienna: Dark Young</p>',
    '| Sienna: Dark Young | Dark Turquoise: Deep One</p>'
)

with open('simulation.py', 'w') as f:
    f.write(text)
