with open('simulation.py', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def update_grid" in line:
        print(f"Line {i}: {line.strip()}")
    if "white_holes =" in line:
        print(f"Line {i}: {line.strip()}")
    if "elif state == 32:" in line:
        print(f"Line {i}: {line.strip()}")
    if "MAIN CELLULAR AUTOMATON UPDATE PASS" in line:
        print(f"Line {i}: {line.strip()}")
    if "elif current_state == 32:" in line:
        print(f"Line {i}: {line.strip()}")
