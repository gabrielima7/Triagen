import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Introduce Formless Spawn (79)

# 1. Update states list
content = re.sub(r'77, 78\]', r'77, 78, 79]', content)

# 2. Update weights comment
content = re.sub(r'Chthonian \(0\.005%\)', r'Chthonian (0.005%), Formless Spawn (0.005%)', content)

# 3. Update weights list
content = re.sub(r'(0\.005, 0\.005, 0\.005, 0\.005, 0\.005\])', r'0.005, 0.005, 0.005, 0.005, 0.005, 0.005]', content)

# 4. Update chars
content = re.sub(r'77: "t", 78: "c"\}', r'77: "t", 78: "c", 79: "f"}', content)

# 5. Update blocking_states
content = re.sub(r'74, 75, 76, 77, 78\}', r'74, 75, 76, 77, 78, 79}', content)

# 6. Add Formless Spawn Logic
formless_logic = """
            # --- STATE 79: FORMLESS SPAWN ---
            elif current_state == 79:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False

                # Formless Spawn feed on Investigators (39), Cultists (40), and Ghouls (73)
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [39, 40, 73]:
                        new_grid[cy][cx] = 79
                        moved = True
                        break

                if not moved:
                    # They replicate rapidly into nearby void (oozing behavior) if they find Tsathoggua (76) nearby
                    has_tsathoggua = any(grid[ny % height][nx % width] == 76 for ny, nx in neighbors)
                    if has_tsathoggua and random.random() < 0.2: # 20% chance to replicate if near their creator
                         for ny, nx in neighbors:
                            cy, cx = ny % height, nx % width
                            if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                                new_grid[cy][cx] = 79
                                new_grid[y][x] = 79 # Don't leave void, replicate
                                moved = True
                                break

                if not moved:
                    # Wander
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 79
                            moved = True
                            break

                if not moved:
                    new_grid[y][x] = 79 # Stay put

"""
content = re.sub(r'(\s+)else:\n(\s+)# Evolve quantum non-local teleportation', r'\g<1>' + formless_logic.lstrip('\n') + r'\n\g<1>else:\n\g<2># Evolve quantum non-local teleportation', content)

# 7. Update HTML colors
content = re.sub(r"78: '#a0522d' // Chthonian\n\s+\}", r"78: '#a0522d', // Chthonian\n            79: '#000000' // Formless Spawn\n        }", content)

# 8. Update HTML title
content = re.sub(r'Tindalos Hound, Chthonian</h2>', r'Tindalos Hound, Chthonian, Formless Spawn</h2>', content)

# 9. Update Legend
content = re.sub(r'Sienna: Chthonian</p>', r'Sienna: Chthonian | Black: Formless Spawn</p>', content)

with open('simulation.py', 'w') as f:
    f.write(content)

print("Patched simulation.py")
