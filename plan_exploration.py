import re
with open("simulation.py", "r") as f:
    content = f.read()

print("Lines with weights:")
for i, line in enumerate(content.split('\n')):
    if "weights = " in line or "states =" in line:
        print(f"{i}: {line}")

print("\nLines with chars:")
for i, line in enumerate(content.split('\n')):
    if "chars =" in line:
        print(f"{i}: {line}")

print("\nLines with blocking_states:")
for i, line in enumerate(content.split('\n')):
    if "blocking_states" in line:
        print(f"{i}: {line}")
