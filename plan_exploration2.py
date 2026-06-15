import sys
with open("simulation.py", "r") as f:
    content = f.read()

for i, line in enumerate(content.split('\n')):
    if "elif current_state == 48:" in line or "elif current_state == 49:" in line:
        print(f"Line {i}: {line}")
