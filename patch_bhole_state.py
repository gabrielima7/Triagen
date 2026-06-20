import re

with open("simulation.py", "r") as f:
    text = f.read()

# 1. Update states list
text = re.sub(
    r'(states = \[.*?)(62)\]',
    r'\1\2, 63]',
    text,
    flags=re.DOTALL
)

# 2. Update comments
text = re.sub(
    r'(Hound of Tindalos \(0.005%\))',
    r'\1, Bhole (0.005%)',
    text
)

# 3. Update weights
text = re.sub(
    r'(weights = \[.*?)(0.005)\]',
    r'\1\2, 0.005]',
    text,
    flags=re.DOTALL
)

# 4. Update chars
text = re.sub(
    r'(62: "g")\}',
    r'\1, 63: "B"}',
    text
)

# 5. Update blocking states
text = re.sub(
    r'(blocking_states = \{.*?)(62)\}',
    r'\1\2, 63}',
    text,
    flags=re.DOTALL
)

with open("simulation.py", "w") as f:
    f.write(text)

print("Updated state lists")
