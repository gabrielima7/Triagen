with open('simulation.py', 'r') as f:
    text = f.read()

text = text.replace(
    "            49: '#a0522d', // Dark Young\n",
    "            49: '#a0522d', // Dark Young\n            50: '#00ced1', // Deep One\n"
)

with open('simulation.py', 'w') as f:
    f.write(text)
