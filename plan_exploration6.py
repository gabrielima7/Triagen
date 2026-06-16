with open("simulation.py", "r") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "def update_grid" in line:
        print(f"update_grid at {i}")
    if "The Color Out of Space" in line:
        print(f"Color at {i}")
