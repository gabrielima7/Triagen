import re

with open("simulation.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "<h2>Rock-Paper" in line:
        print(f"Legend title at {i}")
    if "<p>Red:" in line:
        print(f"Legend text at {i}")
