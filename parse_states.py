import json
with open("simulation.py", "r") as f:
    code = f.read()
print([i for i in range(32) if str(i) in code])
