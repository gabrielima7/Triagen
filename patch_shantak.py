import re

with open("simulation.py", "r") as f:
    content = f.read()

# Add to states array
content = re.sub(r'(states = \[.*?72, 73)(\])', r'\1, 74\2', content)

# Add to chars
content = re.sub(r"(73: \"u\"})", r"73: \"u\", 74: \"H\"}", content)

# Add to weights array
content = re.sub(r"(Spider of Leng \(0\.005%\), Byakhee \(0\.005%\), Ghoul \(0\.005%\))", r"\1, Shantak (0.005%)", content)
content = re.sub(r"(weights = \[.*?0\.005, 0\.005, 0\.005)(\])", r"\1, 0.005\2", content)

# Add to Legend in HTML
content = re.sub(r'(<span class="legend-color" style="background-color: #8b4513;"></span> Ghoul)', r'\1\n        <span class="legend-color" style="background-color: #7b68ee;"></span> Shantak', content)

# Add to colors map
content = re.sub(r"(73: '#8b4513' // Ghoul)", r"\1,\n            74: '#7b68ee' // Shantak", content)

# Add Shantak logic
logic = """
            # --- STATE 74: SHANTAK ---
            elif current_state == 74:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False

                # Shantaks prey on Nightgaunts (61) and Ghouls (73)
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [61, 73]:
                        new_grid[cy][cx] = 74
                        moved = True
                        break

                if not moved:
                    # Rare chance to teleport
                    if random.random() < 0.05:
                        void_tiles = [(ty, tx) for ty in range(height) for tx in range(width) if grid[ty][tx] == 6 and new_grid[ty][tx] == 6]
                        if void_tiles:
                            ty, tx = random.choice(void_tiles)
                            new_grid[ty][tx] = 74
                            moved = True

                if not moved:
                    # Wander
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 74
                            moved = True
                            break

                if not moved:
                    new_grid[y][x] = 74 # Stay put
"""
content = re.sub(r'(            # --- STATE 73: GHOUL ---.*?                    new_grid\[y\]\[x\] = 73 # Stay put\n)', r'\1' + logic, content, flags=re.DOTALL)

with open("simulation.py", "w") as f:
    f.write(content)
