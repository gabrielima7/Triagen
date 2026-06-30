import re

with open("simulation.py", "r") as f:
    content = f.read()

# find states
states_match = re.search(r"states\s*=\s*\[(.*?)\]", content)
print("states len:", len(states_match.group(1).split(",")) if states_match else "None")

# find weights
weights_match = re.search(r"weights\s*=\s*\[(.*?)\]", content)
print("weights len:", len(weights_match.group(1).split(",")) if weights_match else "None")

# find chars
chars_match = re.search(r"chars\s*=\s*\{(.*?)\}", content, re.DOTALL)
print("chars found:", bool(chars_match))
