import re

with open("simulation.py", "r") as f:
    text = f.read()

# 1. Update Legend title
text = re.sub(
    r'(Nightgaunt, Gug)</h2>',
    r'\1, Bhole</h2>',
    text
)

# 2. Update Legend description
text = re.sub(
    r'(Dark Brown: Gug)</p>',
    r'\1 | Firebrick: Bhole</p>',
    text
)

# 3. Update colors mapping
text = re.sub(
    r'(62: \'#5c4033\' // Gug)',
    r'\1,\n            63: \'#B22222\' // Bhole',
    text
)

with open("simulation.py", "w") as f:
    f.write(text)

print("Updated UI")
