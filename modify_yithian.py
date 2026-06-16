import re

with open('simulation.py', 'r') as f:
    content = f.read()

# 1. Update states list
content = re.sub(
    r'(states = \[.*?)(\])',
    r'\1, 57, 58\2',
    content,
    count=1
)

# 2. Update weights list
content = re.sub(
    r'(weights = \[.*?)(\])',
    r'\1, 0.005, 0.0\2',
    content,
    count=1
)

# 3. Update chars dict
content = re.sub(
    r'(chars = \{.*?)(\})',
    r'\1, 57: "y", 58: "f"\2',
    content,
    count=1
)

# 4. Update blocking_states
content = re.sub(
    r'(blocking_states = \{.*?)(\})',
    r'\1, 57, 58\2',
    content,
    count=1
)

# 5. Add Logic
logic_str = """
            # --- STATE 57: GREAT RACE OF YITH ---
            elif current_state == 57:
                new_grid[y][x] = 6 # Default to leave void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                        new_grid[cy][cx] = 57
                        moved = True
                        break
                if not moved:
                    new_grid[y][x] = 57

                # Yithians mind-swap with basic lifeforms or spawn Flying Polyps
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if new_grid[cy][cx] in [0, 1, 2, 3, 4] and random.random() < 0.10:
                        new_grid[cy][cx] = 57 # Mind-swap
                    elif new_grid[cy][cx] == 6 and random.random() < 0.01:
                        new_grid[cy][cx] = 58 # Unearthed Flying Polyp
                continue

            # --- STATE 58: FLYING POLYP ---
            elif current_state == 58:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                        new_grid[cy][cx] = 58
                        moved = True
                        break
                if not moved:
                    new_grid[y][x] = 58

                # Polyps hunt Yithians
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if new_grid[cy][cx] == 57:
                        new_grid[cy][cx] = 6 # Consume Yithian
                        break
                continue
"""
content = re.sub(
    r'(# --- STATE 41: SHOGGOTH ---)',
    logic_str.lstrip('\n') + r'\1',
    content,
    count=1
)

# 6. HTML Titles
content = re.sub(
    r'(<h2>.*?)(\s*&\s*Brain Cylinder)?(</h2>)',
    r'\1, Yithian & Flying Polyp\3',
    content,
    count=1
)

# 7. HTML p text
content = re.sub(
    r'(<p>Red: Rock.*?)(</p>)',
    r'\1 | Goldenrod: Yithian | Dark Sea Green: Flying Polyp\2',
    content,
    count=1
)

# 8. HTML colorMap
color_map_str = """
            56: '#708090',  // Brain Cylinder
            57: '#daa520', // Yithian
            58: '#8fbc8f'  // Flying Polyp
"""
content = re.sub(
    r"56:\s*'#708090'\s*//\s*Brain Cylinder",
    color_map_str.strip(),
    content,
    count=1
)

with open('simulation.py', 'w') as f:
    f.write(content)
