import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Introduce Chthonian (78)

# 1. Update states list
content = re.sub(r'76, 77\]', r'76, 77, 78]', content)

# 2. Update weights comment
content = re.sub(r'Tindalos Hound \(0\.005%\)', r'Tindalos Hound (0.005%), Chthonian (0.005%)', content)

# 3. Update weights list
content = re.sub(r'(0\.005, 0\.005, 0\.005, 0\.005\])', r'0.005, 0.005, 0.005, 0.005, 0.005]', content)

# 4. Update chars
content = re.sub(r'76: "&", 77: "t"\}', r'76: "&", 77: "t", 78: "c"}', content)

# 5. Update blocking_states
content = re.sub(r'73, 74, 75, 76, 77\}', r'73, 74, 75, 76, 77, 78}', content)

# 6. Add Chthonian Logic
chthonian_logic = """
            # --- STATE 78: CHTHONIAN ---
            elif current_state == 78:
                new_grid[y][x] = 78 # Default to stay put
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False

                # Chthonians are massive worm-like burrowers that feed on subterranean things
                # They prey on Bholes (63), Ghouls (73), and Rock (0)
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [0, 63, 73]:
                        new_grid[cy][cx] = 78
                        new_grid[y][x] = 6 # Leave void
                        moved = True
                        break

                if not moved:
                    # Wander
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 78
                            new_grid[y][x] = 6
                            moved = True
                            break

"""
content = re.sub(r'(\s+)else:\n(\s+)# Evolve quantum non-local teleportation', r'\g<1>' + chthonian_logic.lstrip('\n') + r'\n\g<1>else:\n\g<2># Evolve quantum non-local teleportation', content)

# 7. Update HTML colors
content = re.sub(r"77: '#4b0082' // Tindalos Hound\n\s+\}", r"77: '#4b0082', // Tindalos Hound\n            78: '#a0522d' // Chthonian\n        }", content)

# 8. Update HTML title
content = re.sub(r'Tsathoggua, Tindalos Hound</h2>', r'Tsathoggua, Tindalos Hound, Chthonian</h2>', content)

# 9. Update Legend
content = re.sub(r'Indigo: Tindalos Hound</p>', r'Indigo: Tindalos Hound | Sienna: Chthonian</p>', content)

with open('simulation.py', 'w') as f:
    f.write(content)

print("Patched simulation.py")
