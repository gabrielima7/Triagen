import re

with open('agent_handover.md', 'r') as f:
    text = f.read()

shifts = re.findall(r'### Shift \d+: .*?\n.*?(?=### Shift \d+|$)', text, re.DOTALL)
print("Total shifts:", len(shifts))
print("\nLast shift:")
print(shifts[-1])
