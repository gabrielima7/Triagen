import sys
import re

with open('agent_handover.md', 'r') as f:
    text = f.read()

print("Current states overview:")
state_matches = re.findall(r'\(State (\d+)\)', text)
states = set([int(s) for s in state_matches])
print(sorted(list(states)))
