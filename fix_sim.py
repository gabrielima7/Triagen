with open("simulation.py", "r") as f:
    content = f.read()

# Fix the duplicate logic block that may have been injected

logic_to_fix = """            elif current_state == 10: # Godzilla
                # Godzilla slowly walks and destroys
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                dy, dx = random.choice(directions)
                ny, nx = (y + dy) % height, (x + dx) % width
                if (ny, nx) not in pending_changes and grid[ny][nx] != 10:
                    pending_changes[(ny, nx)] = 10
                    pending_changes[(y, x)] = 6 # Leaves void behind
                else:
                     new_grid[y][x] = 10
                continue
"""
content = content.replace(logic_to_fix + logic_to_fix, logic_to_fix)

with open("simulation.py", "w") as f:
    f.write(content)
