import re

with open("agent_handover.md", "r") as f:
    text = f.read()

shifts = re.findall(r'### Shift (\d+): (.*?)\n', text)
print(shifts[-5:])
