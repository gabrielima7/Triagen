import re

with open("simulation.py", "r") as f:
    text = f.read()

assert "63: \"B\"" in text, "Missing char mapping"
assert "63: '#B22222' // Bhole" in text, "Missing color mapping"
print("Data mappings OK")
