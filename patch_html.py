import re

with open("simulation.py", "r") as f:
    text = f.read()

# Replace legend title
text = text.replace(
    'Abhoth, Glaaki</h2>',
    'Abhoth, Glaaki, Spider of Leng</h2>'
)

# Replace legend description
text = text.replace(
    '| Crimson: Fed Star Vampire</p>',
    '| Crimson: Fed Star Vampire | Purple: Spider of Leng</p>'
)

# Add to JavaScript dictionary
js_color_match = re.search(r"(70: '#dc143c' // Fed Star Vampire)(\n\s+)(}})", text)
if js_color_match:
    text = text[:js_color_match.start(2)] + ",\n            71: '#800080' // Spider of Leng" + text[js_color_match.start(2):]

with open("simulation.py", "w") as f:
    f.write(text)
