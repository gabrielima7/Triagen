import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Introduce Shoggoth Lord (81)

# 1. Update states list
content = re.sub(r'79, 80\]', r'79, 80, 81]', content)

# 2. Update weights comment
content = re.sub(r'Star-Spawn of Cthulhu \(0\.005%\)', r'Star-Spawn of Cthulhu (0.005%), Shoggoth Lord (0.005%)', content)

# 3. Update weights list
content = re.sub(r'(0\.005, 0\.005, 0\.005, 0\.005, 0\.005, 0\.005, 0\.005\])', r'0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005]', content)

# 4. Update chars
content = re.sub(r'79: "f", 80: "C"\}', r'79: "f", 80: "C", 81: "l"}', content)

# 5. Update blocking_states
content = re.sub(r'76, 77, 78, 79, 80\}', r'76, 77, 78, 79, 80, 81}', content)

# 6. Add Shoggoth Lord Logic
shoggothlord_logic = """
            # --- STATE 81: SHOGGOTH LORD ---
            elif current_state == 81:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False

                # Shoggoth Lords feed on regular Shoggoths (41), Elder Things (60), and Deep Ones (50)
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [41, 50, 60]:
                        new_grid[cy][cx] = 81
                        moved = True
                        break

                if not moved:
                    # They possess intellect and can mimic humanoid forms;
                    # If an Investigator (39) is nearby, they have a 5% chance to transform into one to hide
                    has_investigator = any(grid[ny % height][nx % width] == 39 for ny, nx in neighbors)
                    if has_investigator and random.random() < 0.05:
                        new_grid[y][x] = 39 # Mimic an investigator!
                        moved = True

                if not moved:
                    # Wander
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 81
                            moved = True
                            break

                if not moved:
                    new_grid[y][x] = 81 # Stay put

"""
content = re.sub(r'(\s+)else:\n(\s+)# Evolve quantum non-local teleportation', r'\g<1>' + shoggothlord_logic.lstrip('\n') + r'\n\g<1>else:\n\g<2># Evolve quantum non-local teleportation', content)

# 7. Update HTML colors
content = re.sub(r"80: '#2e8b57' // Star-Spawn of Cthulhu\n\s+\}", r"80: '#2e8b57', // Star-Spawn of Cthulhu\n            81: '#556b2f' // Shoggoth Lord\n        }", content)

# 8. Update HTML title
content = re.sub(r'Formless Spawn, Star-Spawn of Cthulhu</h2>', r'Formless Spawn, Star-Spawn of Cthulhu, Shoggoth Lord</h2>', content)

# 9. Update Legend
content = re.sub(r'SeaGreen: Star-Spawn of Cthulhu</p>', r'SeaGreen: Star-Spawn of Cthulhu | DarkOliveGreen: Shoggoth Lord</p>', content)

with open('simulation.py', 'w') as f:
    f.write(content)

print("Patched simulation.py")
