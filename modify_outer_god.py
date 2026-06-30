import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Introduce Outer God (82)

# 1. Update states list
content = re.sub(r'80, 81\]', r'80, 81, 82]', content)

# 2. Update weights comment
content = re.sub(r'Shoggoth Lord \(0\.005%\)', r'Shoggoth Lord (0.005%), Outer God (0.005%)', content)

# 3. Update weights list
content = re.sub(r'(0\.005, 0\.005, 0\.005, 0\.005, 0\.005, 0\.005, 0\.005, 0\.005\])', r'0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005]', content)

# 4. Update chars (using 'o' as 'O' is taken by Omega (16) and '0' is Rock)
content = re.sub(r'80: "C", 81: "l"\}', r'80: "C", 81: "l", 82: "o"}', content)

# 5. Update blocking_states
content = re.sub(r'77, 78, 79, 80, 81\}', r'77, 78, 79, 80, 81, 82}', content)

# 6. Add Outer God Logic
outergod_logic = """
            # --- STATE 82: OUTER GOD ---
            elif current_state == 82:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False

                # Outer Gods consume almost all lesser entities
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [39, 40, 41, 50, 73, 79, 81]:
                        new_grid[cy][cx] = 82
                        moved = True
                        break

                if not moved:
                    # They corrupt the very soil around them
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6 and random.random() < 0.1:
                            new_grid[cy][cx] = 53 # Blighted Soil

                    # Space and time bend around them; chance to teleport
                    if random.random() < 0.05:
                        void_tiles = [(ty, tx) for ty in range(height) for tx in range(width) if grid[ty][tx] == 6 and new_grid[ty][tx] == 6]
                        if void_tiles:
                            ty, tx = random.choice(void_tiles)
                            new_grid[ty][tx] = 82
                            moved = True

                if not moved:
                    # Wander
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 82
                            moved = True
                            break

                if not moved:
                    new_grid[y][x] = 82 # Stay put

"""
content = re.sub(r'(\s+)else:\n(\s+)# Evolve quantum non-local teleportation', r'\g<1>' + outergod_logic.lstrip('\n') + r'\n\g<1>else:\n\g<2># Evolve quantum non-local teleportation', content)

# 7. Update HTML colors
content = re.sub(r"81: '#556b2f' // Shoggoth Lord\n\s+\}", r"81: '#556b2f', // Shoggoth Lord\n            82: '#ff1493' // Outer God\n        }", content)

# 8. Update HTML title
content = re.sub(r'Star-Spawn of Cthulhu, Shoggoth Lord</h2>', r'Star-Spawn of Cthulhu, Shoggoth Lord, Outer God</h2>', content)

# 9. Update Legend
content = re.sub(r'DarkOliveGreen: Shoggoth Lord</p>', r'DarkOliveGreen: Shoggoth Lord | DeepPink: Outer God</p>', content)

with open('simulation.py', 'w') as f:
    f.write(content)

print("Patched simulation.py")
