import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Introduce Star-Spawn of Cthulhu (80)

# 1. Update states list
content = re.sub(r'78, 79\]', r'78, 79, 80]', content)

# 2. Update weights comment
content = re.sub(r'Formless Spawn \(0\.005%\)', r'Formless Spawn (0.005%), Star-Spawn of Cthulhu (0.005%)', content)

# 3. Update weights list
content = re.sub(r'(0\.005, 0\.005, 0\.005, 0\.005, 0\.005, 0\.005\])', r'0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005]', content)

# 4. Update chars
content = re.sub(r'78: "c", 79: "f"\}', r'78: "c", 79: "f", 80: "C"}', content)

# 5. Update blocking_states
content = re.sub(r'75, 76, 77, 78, 79\}', r'75, 76, 77, 78, 79, 80}', content)

# 6. Add Star-Spawn Logic
starspawn_logic = """
            # --- STATE 80: STAR-SPAWN OF CTHULHU ---
            elif current_state == 80:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False

                # Star-Spawn feed on Deep Ones (50), Investigators (39), and Cultists (40)
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [39, 40, 50]:
                        new_grid[cy][cx] = 80
                        moved = True
                        break

                if not moved:
                    # They tend to congregate around Cthulhu (37) or Sleeping Cthulhu (38)
                    has_cthulhu = any(grid[ny % height][nx % width] in [37, 38] for ny, nx in neighbors)
                    if has_cthulhu:
                        new_grid[y][x] = 80 # Stay near Cthulhu
                        moved = True

                if not moved:
                    # Wander
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 80
                            moved = True
                            break

                if not moved:
                    new_grid[y][x] = 80 # Stay put

"""
content = re.sub(r'(\s+)else:\n(\s+)# Evolve quantum non-local teleportation', r'\g<1>' + starspawn_logic.lstrip('\n') + r'\n\g<1>else:\n\g<2># Evolve quantum non-local teleportation', content)

# 7. Update HTML colors
content = re.sub(r"79: '#000000' // Formless Spawn\n\s+\}", r"79: '#000000', // Formless Spawn\n            80: '#2e8b57' // Star-Spawn of Cthulhu\n        }", content)

# 8. Update HTML title
content = re.sub(r'Chthonian, Formless Spawn</h2>', r'Chthonian, Formless Spawn, Star-Spawn of Cthulhu</h2>', content)

# 9. Update Legend
content = re.sub(r'Black: Formless Spawn</p>', r'Black: Formless Spawn | SeaGreen: Star-Spawn of Cthulhu</p>', content)

with open('simulation.py', 'w') as f:
    f.write(content)

print("Patched simulation.py")
