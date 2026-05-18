with open("simulation.py", "r") as f:
    content = f.read()

# Godzilla may not be naturally seeded well because of the random choice
# Let's add Godzilla into Pulsar to Wormhole random seeding or
# just drop one on the grid if none exist to make sure it functions

logic_to_add = """
    # Make sure at least one Godzilla is on the board
    has_godzilla = any(10 in row for row in grid)
    if not has_godzilla:
        ry, rx = random.randint(0, len(grid)-1), random.randint(0, len(grid[0])-1)
        grid[ry][rx] = 10
"""

content = content.replace("def update_grid(grid):\n    \"\"\"Applies Rock-Paper-Scissors-Spock-Lizard Cellular Automaton rules to generate the next state.\"\"\"\n    height = len(grid)",
"def update_grid(grid):\n    \"\"\"Applies Rock-Paper-Scissors-Spock-Lizard Cellular Automaton rules to generate the next state.\"\"\"\n" + logic_to_add + "\n    height = len(grid)")

with open("simulation.py", "w") as f:
    f.write(content)
