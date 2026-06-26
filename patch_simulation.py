import re

with open("simulation.py", "r") as f:
    text = f.read()

# Add to states array
states_match = re.search(r'(states = \[.*?)(])', text)
if states_match:
    text = text[:states_match.end(1)] + ', 71' + text[states_match.end(1):]

# Add to weights array
weights_match = re.search(r'(weights = \[.*?)(])', text)
if weights_match:
    text = text[:weights_match.end(1)] + ', 0.005' + text[weights_match.end(1):]

# Update Legend Comment
text = text.replace(
    'Yithian (0.005%), Flying Polyp (0.005%), Hound of Tindalos (0.005%)',
    'Yithian (0.005%), Flying Polyp (0.005%), Hound of Tindalos (0.005%), Spider of Leng (0.005%)'
)

# Update chars dict
chars_match = re.search(r'(chars = \{.*?)(})', text)
if chars_match:
    text = text[:chars_match.end(1)] + ', 71: "8"' + text[chars_match.end(1):]

# Update blocking states
blocking_match = re.search(r'(blocking_states = \{.*?)(})', text)
if blocking_match:
    text = text[:blocking_match.end(1)] + ', 71' + text[blocking_match.end(1):]

# Update predators array... wait we don't need to, spiders aren't prey to RPS
# but what about others?

with open("simulation.py", "w") as f:
    f.write(text)
