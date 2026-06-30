import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Let's introduce Tindalos (77)

# 1. Update states list
content = re.sub(r'75, 76\]', r'75, 76, 77]', content)

# 2. Update weights comment
content = re.sub(r'Tsathoggua \(0\.005%\)', r'Tsathoggua (0.005%), Tindalos Hound (0.005%)', content)

# 3. Update weights list
content = re.sub(r'(0\.005, 0\.005, 0\.005\])', r'0.005, 0.005, 0.005, 0.005]', content)

# 4. Update chars
content = re.sub(r'75: "W", 76: "&"\}', r'75: "W", 76: "&", 77: "t"}', content)

# 5. Update blocking_states
content = re.sub(r'72, 73, 74, 75, 76\}', r'72, 73, 74, 75, 76, 77}', content)

# 6. Add Tindalos Hound Logic
tindalos_logic = """
            # --- STATE 77: TINDALOS HOUND ---
            elif current_state == 77:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False

                # Tindalos Hounds emerge from angles and corners to hunt
                # They prey on anyone who meddles with time/space: Paradox (24), Investigator (39)
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [24, 39]:
                        new_grid[cy][cx] = 77
                        moved = True
                        break

                if not moved:
                    # Very high chance to teleport to any tile that represents "corners"
                    if random.random() < 0.15:
                        void_tiles = [(ty, tx) for ty in range(height) for tx in range(width) if grid[ty][tx] == 6 and new_grid[ty][tx] == 6]
                        if void_tiles:
                            ty, tx = random.choice(void_tiles)
                            new_grid[ty][tx] = 77
                            moved = True

                if not moved:
                    # Wander
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 77
                            moved = True
                            break

                if not moved:
                    new_grid[y][x] = 77 # Stay put

"""
content = re.sub(r'(\s+)else:\n(\s+)# Evolve quantum non-local teleportation', r'\g<1>' + tindalos_logic.lstrip('\n') + r'\n\g<1>else:\n\g<2># Evolve quantum non-local teleportation', content)

# 7. Update HTML colors
content = re.sub(r"76: '#6b8e23' // Tsathoggua\n\s+\}", r"76: '#6b8e23', // Tsathoggua\n            77: '#4b0082' // Tindalos Hound\n        }", content)

# 8. Update HTML title
content = re.sub(r'Ithaqua, Tsathoggua</h2>', r'Ithaqua, Tsathoggua, Tindalos Hound</h2>', content)

# 9. Update Legend
content = re.sub(r'OliveDrab: Tsathoggua</p>', r'OliveDrab: Tsathoggua | Indigo: Tindalos Hound</p>', content)

with open('simulation.py', 'w') as f:
    f.write(content)

print("Patched simulation.py")
