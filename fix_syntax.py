import re

with open("simulation.py", "r") as f:
    text = f.read()

text = text.replace("62: '#5c4033' // Gug,", "62: '#5c4033', // Gug")

with open("simulation.py", "w") as f:
    f.write(text)

print("Fixed syntax")
