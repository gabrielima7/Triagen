import json
import random
import os

GRID_WIDTH = 100
GRID_HEIGHT = 100
STATE_FILE = "state.json"

def create_grid(width, height, randomize=False):
    """Creates a 2D grid, optionally filled with random states."""
    grid = []
    if randomize:
        states = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        # Weighted choice: RPSLK (80% total, 16% each), Black Hole (1%), Void (16.45%), Supernova (0.1%), Pulsar (0.5%), Wormhole (0.3%), Godzilla (1.1%), Jaeger (0.5%), Mothra (0.5%), Glitch (0.05%), Anti-Virus (0.05%), MechaGodzilla (0.05%), Omega (0.05%), Nexus (0.05%)
        weights = [16.0, 16.0, 16.0, 16.0, 16.0, 1.0, 16.45, 0.1, 0.5, 0.3, 1.1, 0.5, 0.5, 0.05, 0.05, 0.05, 0.05, 0.05]
        for _ in range(height):
            row = random.choices(states, weights=weights, k=width)
            grid.append(row)
    else:
        for _ in range(height):
            grid.append([0 for _ in range(width)])
    return grid

def load_state():
    """Loads the grid state from state.json if it exists, otherwise creates a new random grid."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                print("Loaded existing state from", STATE_FILE)
                grid = data.get("grid", create_grid(GRID_WIDTH, GRID_HEIGHT, randomize=True))

                # Check if we need to resize the grid
                if len(grid) != GRID_HEIGHT or (len(grid) > 0 and len(grid[0]) != GRID_WIDTH):
                    print(f"Resizing grid from {len(grid[0]) if len(grid) > 0 else 0}x{len(grid)} to {GRID_WIDTH}x{GRID_HEIGHT}.")
                    new_grid = create_grid(GRID_WIDTH, GRID_HEIGHT, randomize=True)
                    # Copy old grid data over to new grid
                    min_height = min(len(grid), GRID_HEIGHT)
                    min_width = min(len(grid[0]) if len(grid) > 0 else 0, GRID_WIDTH)
                    for y in range(min_height):
                        for x in range(min_width):
                            new_grid[y][x] = grid[y][x]
                    grid = new_grid

                # Check if it's a legacy grid (missing states 3 or 4) and seed them
                has_three = any(3 in row for row in grid)
                has_four = any(4 in row for row in grid)
                if not (has_three and has_four):
                    print("Legacy grid detected. Seeding State 3 (Spock) and State 4 (Lizard).")
                    for y in range(len(grid)):
                        for x in range(len(grid[y])):
                            rand_val = random.random()
                            if rand_val < 0.05: # 5% chance to become Spock
                                grid[y][x] = 3
                            elif rand_val < 0.10: # 5% chance to become Lizard
                                grid[y][x] = 4
                return grid
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading state: {e}. Creating a new random grid.")
            return create_grid(GRID_WIDTH, GRID_HEIGHT, randomize=True)
    else:
        print("No existing state found. Creating a new random grid.")
        return create_grid(GRID_WIDTH, GRID_HEIGHT, randomize=True)

def save_state(grid):
    """Saves the grid state to state.json."""
    data = {
        "grid": grid,
        "width": len(grid[0]) if grid else 0,
        "height": len(grid)
    }
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Saved state to", STATE_FILE)

def print_grid(grid):
    """Prints the grid to the console."""
    chars = {0: "R", 1: "P", 2: "S", 3: "K", 4: "L", 5: "B", 6: "V", 7: "*", 8: "@", 9: "W", 10: "G", 11: "J", 12: "M", 13: "X", 14: "A", 15: "Z", 16: "O", 17: "N"}
    for row in grid:
        print(" ".join(chars.get(cell, "?") for cell in row))
    print()

def count_predator_neighbors(grid, x, y, state):
    """Counts the number of predator neighbors for a given cell in RPS-Spock-Lizard."""
    predators_of = {
        0: [1, 3],
        1: [2, 4],
        2: [0, 3],
        3: [1, 4],
        4: [0, 2]
    }

    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    count = 0
    if state in predators_of:
        predator_states = predators_of[state]
    else:
        predator_states = []
    predator_counts = {p: 0 for p in predator_states}

    # Check the 8 surrounding cells
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue # Skip the cell itself

            # Wrap around edges (toroidal array)
            neighbor_y = (y + i) % height
            neighbor_x = (x + j) % width

            neighbor_state = grid[neighbor_y][neighbor_x]
            if neighbor_state in predator_states:
                count += 1
                predator_counts[neighbor_state] += 1

    return count, predator_counts

def update_grid(grid):
    """Applies Rock-Paper-Scissors-Spock-Lizard Cellular Automaton rules to generate the next state."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    new_grid = create_grid(width, height)

    # 1. PRE-COMPUTATION (O(N) search for special states to avoid O(N^2) complexity inside the loop)
    wormholes = []
    voids = []
    godzillas = []
    jaegers = []
    mothras = []
    glitches = []
    mechagodzillas = []
    omegas = []
    for y in range(height):
        for x in range(width):
            state = grid[y][x]
            if state == 9:
                wormholes.append((y, x))
            elif state == 6:
                voids.append((y, x))
            elif state == 10:
                godzillas.append((y, x))
            elif state == 11:
                jaegers.append((y, x))
            elif state == 12:
                mothras.append((y, x))
            elif state == 13:
                glitches.append((y, x))
            elif state == 15:
                mechagodzillas.append((y, x))
            elif state == 16:
                omegas.append((y, x))

    # Ensure at least one Godzilla, Jaeger, and Mothra are on the board
    if not godzillas:
        # Spawn Godzilla in a random position, preferably a Void cell if one exists
        if voids:
            ry, rx = random.choice(voids)
            voids.remove((ry, rx))
        else:
            ry, rx = random.randint(0, height - 1), random.randint(0, width - 1)
        godzillas.append((ry, rx))
        # Place the newly spawned Godzilla in the new grid
        new_grid[ry][rx] = 10

    if not jaegers:
        # Spawn Jaeger in a random position, preferably a Void cell if one exists
        if voids:
            ry, rx = random.choice(voids)
            voids.remove((ry, rx))
        else:
            ry, rx = random.randint(0, height - 1), random.randint(0, width - 1)
        jaegers.append((ry, rx))
        # Place the newly spawned Jaeger in the new grid
        new_grid[ry][rx] = 11

    if not mothras:
        # Spawn Mothra in a random position, preferably a Void cell if one exists
        if voids:
            ry, rx = random.choice(voids)
            voids.remove((ry, rx))
        else:
            ry, rx = random.randint(0, height - 1), random.randint(0, width - 1)
        mothras.append((ry, rx))
        # Place the newly spawned Mothra in the new grid
        new_grid[ry][rx] = 12

    # 2. RESOLVE GODZILLA MOVEMENT (preventing overlap and blocking, O(G) where G is number of Godzillas)
    godzilla_moves = {}   # maps (src_y, src_x) -> (dest_y, dest_x)
    godzilla_targets = set()
    for gy, gx in godzillas:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        moved = False
        for dy, dx in directions:
            ny, nx = (gy + dy) % height, (gx + dx) % width
            # Valid target if it does not contain a Godzilla in the current grid and is not targeted by another, and is not a Nexus
            if grid[ny][nx] != 10 and grid[ny][nx] != 17 and (ny, nx) not in godzilla_targets:
                godzilla_moves[(gy, gx)] = (ny, nx)
                godzilla_targets.add((ny, nx))
                moved = True
                break
        if not moved:
            godzilla_moves[(gy, gx)] = (gy, gx)
            godzilla_targets.add((gy, gx))

    # 2.5 RESOLVE JAEGER MOVEMENT (seeking nearest Godzilla)
    jaeger_targets = set()
    for jy, jx in jaegers:
        if godzillas:
            # Find nearest Godzilla
            nearest_g = None
            min_dist = float('inf')
            for gy, gx in godzillas:
                dist = abs(gy - jy) + abs(gx - jx)
                if dist < min_dist:
                    min_dist = dist
                    nearest_g = (gy, gx)

            if nearest_g:
                gy, gx = nearest_g
                # Move one step towards Godzilla
                dy, dx = 0, 0
                if gy > jy: dy = 1
                elif gy < jy: dy = -1
                elif gx > jx: dx = 1
                elif gx < jx: dx = -1

                ny, nx = (jy + dy) % height, (jx + dx) % width
                if grid[ny][nx] != 11 and grid[ny][nx] != 17 and (ny, nx) not in jaeger_targets:
                    jaeger_targets.add((ny, nx))
                else:
                    jaeger_targets.add((jy, jx))
            else:
                jaeger_targets.add((jy, jx))
        else:
            jaeger_targets.add((jy, jx))

    # 2.6 RESOLVE MOTHRA MOVEMENT (random movement like Godzilla)
    mothra_targets = set()
    for my, mx in mothras:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        moved = False
        for dy, dx in directions:
            ny, nx = (my + dy) % height, (mx + dx) % width
            # Valid target if it does not contain a Mothra in the current grid and is not targeted by another, and is not a Nexus
            if grid[ny][nx] != 12 and grid[ny][nx] != 17 and (ny, nx) not in mothra_targets:
                mothra_targets.add((ny, nx))
                moved = True
                break
        if not moved:

            mothra_targets.add((my, mx))

    # 2.7 RESOLVE MECHAGODZILLA MOVEMENT (seeking nearest Mothra, or move randomly)
    mechagodzilla_targets = set()
    for mgy, mgx in mechagodzillas:
        if mothras:
            # Find nearest Mothra
            nearest_m = None
            min_dist = float('inf')
            for my, mx in mothras:
                dist = abs(my - mgy) + abs(mx - mgx)
                if dist < min_dist:
                    min_dist = dist
                    nearest_m = (my, mx)

            if nearest_m:
                my, mx = nearest_m
                # Move one step towards Mothra
                dy, dx = 0, 0
                if my > mgy: dy = 1
                elif my < mgy: dy = -1
                elif mx > mgx: dx = 1
                elif mx < mgx: dx = -1

                ny, nx = (mgy + dy) % height, (mgx + dx) % width
                if grid[ny][nx] != 15 and grid[ny][nx] != 17 and (ny, nx) not in mechagodzilla_targets:
                    mechagodzilla_targets.add((ny, nx))
                else:
                    mechagodzilla_targets.add((mgy, mgx))
            else:
                mechagodzilla_targets.add((mgy, mgx))
        else:
            # Move randomly
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            moved = False
            for dy, dx in directions:
                ny, nx = (mgy + dy) % height, (mgx + dx) % width
                if grid[ny][nx] != 15 and grid[ny][nx] != 17 and (ny, nx) not in mechagodzilla_targets:
                    mechagodzilla_targets.add((ny, nx))
                    moved = True
                    break
            if not moved:
                mechagodzilla_targets.add((mgy, mgx))

    # 2.8 RESOLVE OMEGA MOVEMENT (random movement)
    omega_targets = set()
    for oy, ox in omegas:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        moved = False
        for dy, dx in directions:
            ny, nx = (oy + dy) % height, (ox + dx) % width
            # Valid target if it does not contain an Omega in the current grid and is not targeted by another, and is not a Nexus
            if grid[ny][nx] != 16 and grid[ny][nx] != 17 and (ny, nx) not in omega_targets:
                omega_targets.add((ny, nx))
                moved = True
                break
        if not moved:
            omega_targets.add((oy, ox))

    # 3. COLLECT WORMHOLE HORIZONS (Normal states adjacent to any Wormhole)
    wormhole_horizons = []
    for wy, wx in wormholes:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue
                ny, nx = (wy + i) % height, (wx + j) % width
                neighbor_state = grid[ny][nx]
                if neighbor_state in [0, 1, 2, 3, 4]:
                    wormhole_horizons.append(neighbor_state)

    # 4. PRE-DETERMINE WORMHOLE QUANTUM TELEPORTATION TARGETS (to prevent cell overwrites)
    available_voids = [v for v in voids if v not in godzilla_targets and v not in mothra_targets and v not in jaeger_targets and v not in mechagodzilla_targets and v not in omega_targets]
    teleportation_targets = {}
    for wy, wx in wormholes:
        if available_voids:
            target_y, target_x = random.choice(available_voids)
            available_voids.remove((target_y, target_x))
            teleported_state = random.choice(wormhole_horizons) if wormhole_horizons else random.choice([0, 1, 2, 3, 4])
            teleportation_targets[(target_y, target_x)] = teleported_state

    # 5. MAIN CELLULAR AUTOMATON UPDATE PASS
    for y in range(height):
        for x in range(width):
            # Check for Omega collisions with any other Kaiju
            if (y, x) in omega_targets and ((y, x) in godzilla_targets or (y, x) in jaeger_targets or (y, x) in mothra_targets or (y, x) in mechagodzilla_targets):
                # Mutual destruction leaving a Wormhole
                new_grid[y][x] = 9
                continue

            # Check if this cell is a target of an Omega move
            if (y, x) in omega_targets:
                new_grid[y][x] = 16
                continue

            # Check for Jaeger-Godzilla collisions
            if (y, x) in godzilla_targets and (y, x) in jaeger_targets:
                # Mutual destruction into a Supernova
                new_grid[y][x] = 7
                continue

            # Check if this cell is a target of a Godzilla move (Godzilla crushes anything here)
            if (y, x) in godzilla_targets:
                new_grid[y][x] = 10
                continue

            # Check for MechaGodzilla-Godzilla/Jaeger collisions
            if (y, x) in mechagodzilla_targets and ((y, x) in godzilla_targets or (y, x) in jaeger_targets):
                # Mutual destruction into a Supernova
                new_grid[y][x] = 7
                continue

            # Check if this cell is a target of a MechaGodzilla move
            if (y, x) in mechagodzilla_targets:
                new_grid[y][x] = 15
                continue

            # Check if this cell is a target of a Mothra move
            if (y, x) in mothra_targets:
                new_grid[y][x] = 12
                continue

            # Check if Jaegers moving near Glitches become MechaGodzillas (corruption mechanic)
            if (y, x) in jaeger_targets:
                glitch_neighbors = sum(
                    1 for i in range(-1, 2) for j in range(-1, 2)
                    if not (i == 0 and j == 0) and grid[(y + i) % height][(x + j) % width] == 13
                )
                if glitch_neighbors > 0 and random.random() < 0.05:
                    new_grid[y][x] = 15 # Corrupted into MechaGodzilla
                else:
                    new_grid[y][x] = 11
                continue


            # Check if this cell previously had a Godzilla or Jaeger (it has moved away leaving a Void)
            if grid[y][x] == 10 or grid[y][x] == 11:
                new_grid[y][x] = 6
                continue

            # Check if this cell previously had a MechaGodzilla (it leaves behind a Glitch)
            if grid[y][x] == 15:
                new_grid[y][x] = 13
                continue

            # Check if this cell previously had a Mothra (it has moved away leaving Life)
            if grid[y][x] == 12:
                new_grid[y][x] = random.choice([0, 1, 2, 3, 4])
                continue

            # Check if this cell previously had an Omega (it leaves behind a Black Hole)
            if grid[y][x] == 16:
                new_grid[y][x] = 5
                continue

            # Check if this cell receives a quantum teleported state
            if (y, x) in teleportation_targets:
                new_grid[y][x] = teleportation_targets[(y, x)]
                continue

            current_state = grid[y][x]

            # --- STATE 17: NEXUS ---
            if current_state == 17:
                if random.random() < 0.001: # 0.1% chance to decay
                    new_grid[y][x] = 6
                else:
                    new_grid[y][x] = 17
                continue

            # --- STATE 14: ANTI-VIRUS ---
            if current_state == 14:
                glitch_neighbors = sum(
                    1 for i in range(-1, 2) for j in range(-1, 2)
                    if not (i == 0 and j == 0) and grid[(y + i) % height][(x + j) % width] == 13
                )
                if glitch_neighbors == 0:
                    if random.random() < 0.05:
                        new_grid[y][x] = 6 # Decays into Void (5% chance)
                    else:
                        new_grid[y][x] = 14 # Stays Anti-Virus
                else:
                    new_grid[y][x] = 14 # Stays Anti-Virus to fight Glitches
                continue

            # --- STATE 13: GLITCH ---
            anti_virus_neighbors = sum(
                1 for i in range(-1, 2) for j in range(-1, 2)
                if not (i == 0 and j == 0) and grid[(y + i) % height][(x + j) % width] == 14
            )
            glitch_neighbors = sum(
                1 for i in range(-1, 2) for j in range(-1, 2)
                if not (i == 0 and j == 0) and grid[(y + i) % height][(x + j) % width] == 13
            )

            if current_state == 13:
                has_nexus_neighbor = any(
                    grid[(y + i) % height][(x + j) % width] == 17
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not (i == 0 and j == 0)
                )
                if has_nexus_neighbor:
                    new_grid[y][x] = 6 # Nexus purifies Glitch
                elif anti_virus_neighbors > 0:
                    new_grid[y][x] = 14 # Anti-Virus cures Glitch
                elif glitch_neighbors >= 4:
                    new_grid[y][x] = 6 # Collapses into Void
                else:
                    new_grid[y][x] = 13 # Stays Glitch
                continue

            if glitch_neighbors > 0:
                if random.random() < (0.10 * glitch_neighbors):
                    new_grid[y][x] = 13
                    continue

            # --- STATE 5: BLACK HOLE ---
            if current_state == 5:
                has_nexus_neighbor = any(
                    grid[(y + i) % height][(x + j) % width] == 17
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not (i == 0 and j == 0)
                )
                # Black Hole vs Wormhole: adjacent Wormholes destroy Black Holes completely
                has_wormhole_neighbor = any(
                    grid[(y + i) % height][(x + j) % width] == 9
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not (i == 0 and j == 0)
                )
                if has_nexus_neighbor:
                    new_grid[y][x] = 6 # Nexus neutralizes Black Hole
                elif has_wormhole_neighbor:
                    new_grid[y][x] = 6
                else:
                    rand_val = random.random()
                    if rand_val < 0.01:
                        new_grid[y][x] = 7 # Supernova (1% chance)
                    elif rand_val < 0.02:
                        new_grid[y][x] = 9 # Wormhole (1% chance)
                    else:
                        new_grid[y][x] = 6 # Decays into Void (98% chance)
                continue

            # --- STATE 6: VOID ---
            elif current_state == 6:
                has_nexus_neighbor = any(
                    grid[(y + i) % height][(x + j) % width] == 17
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not (i == 0 and j == 0)
                )
                has_pulsar_neighbor = any(
                    grid[(y + i) % height][(x + j) % width] == 8
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not (i == 0 and j == 0)
                )

                has_wormhole_neighbor = any(
                    grid[(y + i) % height][(x + j) % width] == 9
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not (i == 0 and j == 0)
                )

                if has_nexus_neighbor and random.random() < 0.05:
                    new_grid[y][x] = 17 # Void crystallizes into Nexus
                elif has_pulsar_neighbor:
                    new_grid[y][x] = random.choice([0, 1, 2, 3, 4])
                elif has_wormhole_neighbor:
                    r = random.random()
                    if r < 0.10:
                        new_grid[y][x] = random.choice([0, 1, 2, 3, 4])
                    elif r < 0.11:
                        new_grid[y][x] = 5
                    else:
                        new_grid[y][x] = 6
                else:
                    rand_val = random.random()
                    if rand_val < 0.001:
                        new_grid[y][x] = 9
                    elif rand_val < 0.05:
                        new_grid[y][x] = random.choice([0, 1, 2, 3, 4])
                    elif rand_val < 0.0505:
                        new_grid[y][x] = 13
                    elif rand_val < 0.051:
                        new_grid[y][x] = 14
                    else:
                        new_grid[y][x] = 6
                continue

            # --- STATE 7: SUPERNOVA ---
            elif current_state == 7:
                if random.random() < 0.05:
                    new_grid[y][x] = 16 # Supernova becomes Omega
                else:
                    new_grid[y][x] = 8 # Supernova becomes Pulsar
                continue

            # --- STATE 8: PULSAR ---
            elif current_state == 8:
                r = random.random()
                if r < 0.01:
                    new_grid[y][x] = 12 # Pulsar becomes Mothra
                elif r < 0.06:
                    new_grid[y][x] = 9 # Pulsar becomes Wormhole
                elif r < 0.11:
                    new_grid[y][x] = 6 # Pulsar becomes Void
                else:
                    new_grid[y][x] = 8
                continue

            # --- STATE 9: WORMHOLE ---
            elif current_state == 9:
                r = random.random()
                if r < 0.05:
                    new_grid[y][x] = 5 # Collapses into Black Hole (closes cycle)
                elif r < 0.15:
                    new_grid[y][x] = 6 # Wormhole collapses into Void
                else:
                    new_grid[y][x] = 9
                continue

            # --- NORMAL STATES 0-4: RPSLK ---
            has_nexus_neighbor = any(
                grid[(y + i) % height][(x + j) % width] == 17
                for i in range(-1, 2)
                for j in range(-1, 2)
                if not (i == 0 and j == 0)
            )
            # Check environmental hazards first
            # 1. Supernova neighbor: completely destroys normal states
            has_state_7_neighbor = any(
                grid[(y + i) % height][(x + j) % width] == 7
                for i in range(-1, 2)
                for j in range(-1, 2)
                if not (i == 0 and j == 0)
            )
            if has_state_7_neighbor and not has_nexus_neighbor:
                new_grid[y][x] = 6
                continue

            # 2. Black Hole neighbor: consumes normal states
            has_state_5_neighbor = any(
                grid[(y + i) % height][(x + j) % width] == 5
                for i in range(-1, 2)
                for j in range(-1, 2)
                if not (i == 0 and j == 0)
            )
            if has_state_5_neighbor and not has_nexus_neighbor:
                new_grid[y][x] = 5
                continue

            # 3. Wormhole neighbor: sucked in with a 20% chance
            has_state_9_neighbor = any(
                grid[(y + i) % height][(x + j) % width] == 9
                for i in range(-1, 2)
                for j in range(-1, 2)
                if not (i == 0 and j == 0)
            )
            if has_state_9_neighbor and random.random() < 0.20:
                new_grid[y][x] = 6
                continue

            total_predators, predator_counts = count_predator_neighbors(grid, x, y, current_state)
            if total_predators >= 3:
                max_count = max(predator_counts.values())
                most_common = [p for p, c in predator_counts.items() if c == max_count]
                new_grid[y][x] = random.choice(most_common)
            else:
                # Evolve quantum non-local teleportation via Wormhole horizons if neighbor to one
                if has_state_9_neighbor and wormhole_horizons and random.random() < 0.10:
                    new_grid[y][x] = random.choice(wormhole_horizons)
                else:
                    new_grid[y][x] = current_state

    return new_grid

def generate_html(grid):
    """Generates an HTML file to visualize the grid using a canvas."""
    width = len(grid[0]) if grid else 0
    height = len(grid)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="1">
    <title>AI Collective: RPS-Spock-Lizard-Wormhole Simulation with Omega</title>
    <style>
        body {{ background-color: #111; color: #eee; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; flex-direction: column; }}
        canvas {{ background-color: #333; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7); border-radius: 4px; }}
        h2 {{ margin-bottom: 5px; color: #ff00ff; text-shadow: 0 0 10px rgba(255, 0, 255, 0.4); }}
        p {{ margin-top: 15px; font-size: 11px; color: #999; }}
    </style>
</head>
<body>
    <h2>Rock-Paper-Scissors-Spock-Lizard with Wormhole Singularity, Godzilla, Jaeger, Mothra, Glitch, MechaGodzilla, Omega & Nexus</h2>
    <canvas id="simCanvas" width="{width * 5}" height="{height * 5}"></canvas>
    <p>Red: Rock | Green: Paper | Blue: Scissors | Purple: Spock | Yellow: Lizard | Black: Black Hole | Gray: Void | White: Supernova | Cyan: Pulsar | Magenta: Wormhole | Orange: Godzilla | Silver: Jaeger | Gold: Mothra | Neon Green: Glitch | Deep Sky Blue: Anti-Virus | Crimson Red: MechaGodzilla | Blue Violet: Omega | Light Cyan: Nexus</p>

    <script>
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');
        const cellSize = 5;

        const colors = {{
            0: '#e74c3c', // Rock
            1: '#2ecc71', // Paper
            2: '#3498db', // Scissors
            3: '#9b59b6', // Spock
            4: '#f1c40f', // Lizard
            5: '#000000', // Black Hole
            6: '#7f8c8d', // Void
            7: '#ffffff', // Supernova
            8: '#00ffff', // Pulsar
            9: '#ff00ff', // Wormhole
            10: '#ff7f00', // Godzilla
            11: '#bdc3c7', // Jaeger
            12: '#ffd700', // Mothra
            13: '#39ff14', // Glitch
            14: '#00bfff', // Anti-Virus
            15: '#e6005c', // MechaGodzilla
            16: '#8a2be2', // Omega
            17: '#e0ffff' // Nexus
        }};

        const grid = {json.dumps(grid)};

        for (let y = 0; y < grid.length; y++) {{
            for (let x = 0; x < grid[y].length; x++) {{
                const state = grid[y][x];
                ctx.fillStyle = colors[state] || '#333';
                ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
            }}
        }}
    </script>
</body>
</html>
"""

    with open("index.html", "w") as f:
        f.write(html_content)
    print("Generated visualizer at index.html")

def main():
    print("--- AI Collective: Continuous Execution Shift ---")
    grid = load_state()

    print("Current State:")
    print_grid(grid)

    print("Computing next generation...")
    next_grid = update_grid(grid)

    print("Next State:")
    print_grid(next_grid)

    save_state(next_grid)
    generate_html(next_grid)
    print("Shift complete. Handing over state to next agent.")

if __name__ == "__main__":
    main()
