import re

with open("simulation.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "states =" in line:
        print(f"Line {i+1}: {line.strip()}")
    if "weights =" in line:
        print(f"Line {i+1}: {line.strip()}")
    if "elif state ==" in line and "30:" in line:
        print(f"Line {i+1}: {line.strip()}")
    if "blocking_states =" in line:
        print(f"Line {i+1}: {line.strip()}")
    if "colors =" in line:
        print(f"Line {i+1}: {line.strip()}")
