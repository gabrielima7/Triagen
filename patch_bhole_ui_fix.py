import re

with open("simulation.py", "r") as f:
    text = f.read()

# 3. Update colors mapping correctly (without escaping single quotes)
text = re.sub(
    r'(63: \\\'#B22222\\\' // Bhole)',
    r"63: '#B22222' // Bhole",
    text
)

with open("simulation.py", "w") as f:
    f.write(text)

print("Updated UI")
