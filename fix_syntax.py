with open("simulation.py", "r") as f:
    content = f.read()

content = content.replace('73: \\"u\\", 74: \\"H\\"}', '73: "u", 74: "H"}')

with open("simulation.py", "w") as f:
    f.write(content)
