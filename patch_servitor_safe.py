import re

with open("simulation.py", "r") as f:
    content = f.read()

# 1. Update states
content = re.sub(
    r'(states\s*=\s*\[[^\]]+82)\]',
    r'\1, 83]',
    content
)

# 2. Update weights and comment
content = re.sub(
    r'(Outer God \(0\.005%\))',
    r'\1, Servitor of the Outer Gods (0.005%)',
    content
)
content = re.sub(
    r'(weights\s*=\s*\[[^\]]+0\.005)\]',
    r'\1, 0.005]',
    content
)

# 3. Update chars
content = re.sub(
    r'(82: \'O\'\n\s*)\}',
    r"\1, 83: '♪'\n    }",
    content
)

# 4. Update blocking_states
content = re.sub(
    r'(blocking_states\s*=\s*\{[^}]+82)\}',
    r'\1, 83}',
    content
)

# 5. Update logic safely by finding the end of 82
search_str = """                if not moved:
                    new_grid[y][x] = 82 # Stay put"""

replace_str = """                if not moved:
                    new_grid[y][x] = 82 # Stay put

            elif current_state == 83:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False

                outer_gods = [42, 43, 45, 48, 82]
                near_god = any(grid[ny % height][nx % width] in outer_gods for ny, nx in neighbors)

                if near_god:
                    # Their maddening music lures mortals
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6 and random.random() < 0.1:
                            new_grid[cy][cx] = random.choice([39, 40])
                            break

                # Wander
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                        new_grid[cy][cx] = 83
                        moved = True
                        break

                if not moved:
                    new_grid[y][x] = 83"""

content = content.replace(search_str, replace_str)

# 6. Update HTML colors
content = re.sub(
    r"(82:\s*'#ff1493'\s*//\s*Outer God\n\s*)\}",
    r"\1, 83: '#7b68ee' // Servitor of the Outer Gods\n        }",
    content
)

# 7. Update HTML legend
legend_addition = r'<span class="legend-item"><span class="color-box" style="background-color: #7b68ee;"></span> 83: Servitor of the Outer Gods</span></p>'
content = re.sub(
    r'Outer God</span></p>',
    f'Outer God</span> {legend_addition}',
    content
)

with open("simulation.py", "w") as f:
    f.write(content)

print("Patch applied.")
