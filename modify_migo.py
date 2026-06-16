import re

with open('simulation.py', 'r') as f:
    content = f.read()

# 1. Update states list
content = re.sub(
    r'(states = \[.*?)(\])',
    r'\1, 55, 56\2',
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
    r'\1, 55: "m", 56: "c"\2',
    content,
    count=1
)

# 4. Update blocking_states
content = re.sub(
    r'(blocking_states = \{.*?)(\})',
    r'\1, 55, 56\2',
    content,
    count=1
)

# 5. Add Logic
logic_str = """
            # --- STATE 55: MI-GO ---
            elif current_state == 55:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                        new_grid[cy][cx] = 55
                        moved = True
                        break
                if not moved:
                    new_grid[y][x] = 55

                # Mi-Go harvest basic lifeforms into Brain Cylinders
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if new_grid[cy][cx] in [0, 1, 2, 3, 4] and random.random() < 0.10:
                        new_grid[cy][cx] = 56
                continue

            # --- STATE 56: BRAIN CYLINDER ---
            elif current_state == 56:
                new_grid[y][x] = 56 # Immobile
                # Brain Cylinders occasionally communicate to spawn a Mi-Go
                if random.random() < 0.05:
                    neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                    random.shuffle(neighbors)
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 55
                            break
                continue
"""
content = re.sub(
    r'(# --- STATE 29: RADIOTROPH ---)',
    logic_str.lstrip('\n') + r'\1',
    content,
    count=1
)

# 6. HTML Titles
content = re.sub(
    r'(<h2>.*?)(\s*&amp;\s*Dark Young)?(</h2>)',
    r'\1, Shub-Niggurath & Dark Young, Mi-Go & Brain Cylinder\3',
    content,
    count=1
)

# 7. HTML p text
content = re.sub(
    r'(<p>Red: Rock.*?)(</p>)',
    r'\1 | Light Pink: Mi-Go | Slate Gray: Brain Cylinder\2',
    content,
    count=1
)

# 8. HTML colorMap
color_map_str = """
            54: '#d3d3d3', // Ashen Dust
            55: '#ffb6c1', // Mi-Go
            56: '#708090'  // Brain Cylinder
"""
content = re.sub(
    r"54:\s*'#d3d3d3'\s*//\s*Ashen Dust",
    color_map_str.strip(),
    content,
    count=1
)

with open('simulation.py', 'w') as f:
    f.write(content)
