with open("simulation.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def update_grid" in line:
        print(f"update_grid at {i}")
    if "elif current_state == 62:" in line:
        print(f"Gug at {i}")
    if "else:" in line and i > 500:
        # maybe finding the end of the update_grid loop
        pass
