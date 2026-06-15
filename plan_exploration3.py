import sys
with open("simulation.py", "r") as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if "elif current_state == 49:" in line:
        print(f"Line {i}: {line}")
    if "49: '#a0522d'" in line:
        print(f"Line {i}: {line}")
