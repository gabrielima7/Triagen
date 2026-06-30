import re

with open('simulation.py', 'r') as f:
    content = f.read()

# 1. Update states list
content = re.sub(r'73, 74, 75\]', r'73, 74, 75, 76]', content)

# 2. Update weights comment
content = re.sub(r'Ithaqua \(0\.005%\)', r'Ithaqua (0.005%), Tsathoggua (0.005%)', content)

# 3. Update weights list
content = re.sub(r'(0\.005, 0\.005\])', r'0.005, 0.005, 0.005]', content)

# 4. Update chars
content = re.sub(r'74: "H", 75: "W"\}', r'74: "H", 75: "W", 76: "&"}', content)

# 5. Update blocking_states
content = re.sub(r'68, 69, 70, 71\}', r'68, 69, 70, 71, 72, 73, 74, 75, 76}', content)

# 6. Add Tsathoggua Logic
tsathoggua_logic = """
            # --- STATE 76: TSATHOGGUA ---
            elif current_state == 76:
                new_grid[y][x] = 76 # Default to stay put (lazy)
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False

                # Tsathoggua feeds on Cultists (40), Ghouls (73), Investigators (39)
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [39, 40, 73]:
                        new_grid[cy][cx] = 76
                        new_grid[y][x] = 6 # Leave void
                        moved = True
                        break

                if not moved:
                    # Very low chance to wander (lazy)
                    if random.random() < 0.05:
                        for ny, nx in neighbors:
                            cy, cx = ny % height, nx % width
                            if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                                new_grid[cy][cx] = 76
                                new_grid[y][x] = 6
                                moved = True
                                break

"""
content = re.sub(r'(\s+)else:\n(\s+)# Evolve quantum non-local teleportation', r'\g<1>' + tsathoggua_logic.lstrip('\n') + r'\n\g<1>else:\n\g<2># Evolve quantum non-local teleportation', content)

# 7. Update HTML colors
content = re.sub(r"75: '#b0e0e6' // Ithaqua\n\s+\}", r"75: '#b0e0e6', // Ithaqua\n            76: '#6b8e23' // Tsathoggua\n        }", content)

# 8. Update HTML title
content = re.sub(r'Byakhee, Ithaqua</h2>', r'Byakhee, Ithaqua, Tsathoggua</h2>', content)

# 9. Update Legend
content = re.sub(r'PowderBlue: Ithaqua</p>', r'PowderBlue: Ithaqua | OliveDrab: Tsathoggua</p>', content)

with open('simulation.py', 'w') as f:
    f.write(content)

print("Patched simulation.py")
