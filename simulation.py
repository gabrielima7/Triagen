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
        states = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        # Weighted choice: RPSLK (80% total, 16% each), Black Hole (1%), Void (16.43%), Supernova (0.1%), Pulsar (0.5%), Wormhole (0.3%), Godzilla (1.1%), Jaeger (0.5%), Mothra (0.5%), Glitch (0.05%), Anti-Virus (0.05%), MechaGodzilla (0.05%), Omega (0.05%), Nexus (0.05%), Reaper (0.05%), Phoenix (0.05%), Yggdrasil (0%), Nidhogg (0.01%), Pandora (0.01%), Chronos (0.01%), Paradox (0.01%), Singularity (0.0001%), Conway (0.0001%), Neutron Star Ortho (0.005%), Neutron Star Diag (0.005%), Radiotroph (0.005%)
        weights = [16.0, 16.0, 16.0, 16.0, 16.0, 1.0, 16.4249, 0.1, 0.5, 0.3, 1.1, 0.5, 0.5, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.0, 0.01, 0.01, 0.01, 0.01, 0.0001, 0.0001, 0.005, 0.005, 0.005]
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
    chars = {0: "R", 1: "P", 2: "S", 3: "K", 4: "L", 5: "B", 6: "V", 7: "*", 8: "@", 9: "W", 10: "G", 11: "J", 12: "M", 13: "X", 14: "A", 15: "Z", 16: "O", 17: "N", 18: "D", 20: "Y", 21: "H", 25: "I", 26: "C"}
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
    reapers = []
    phoenixes = []
    yggdrasils = []
    nidhoggs = []
    pandoras = []
    chronos = []
    paradoxes = []
    singularities = []
    conways = []
    neutron_stars_ortho = []
    neutron_stars_diag = []
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
            elif state == 18:
                reapers.append((y, x))
            elif state == 19:
                phoenixes.append((y, x))
            elif state == 20:
                yggdrasils.append((y, x))
            elif state == 21:
                nidhoggs.append((y, x))
            elif state == 22:
                pandoras.append((y, x))
            elif state == 23:
                chronos.append((y, x))
            elif state == 24:
                paradoxes.append((y, x))
            elif state == 25:
                singularities.append((y, x))
            elif state == 26:
                conways.append((y, x))
            elif state == 27:
                neutron_stars_ortho.append((y, x))
            elif state == 28:
                neutron_stars_diag.append((y, x))

    conway_seeds = set()
    if len(conways) < 15 and random.random() < 0.10:
        if voids:
            cy, cx = random.choice(voids)
            glider_offsets = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
            for dy, dx in glider_offsets:
                ny, nx = (cy + dy) % height, (cx + dx) % width
                conway_seeds.add((ny, nx))

    # BIG BANG CONDITION: If Singularity has consumed enough of the board, trigger universal reset
    if len(singularities) > 100:
        return create_grid(width, height, randomize=True)

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

    # If reapers exist but no phoenixes, spawn a phoenix to hunt it
    if reapers and not phoenixes:
        if voids:
            ry, rx = random.choice(voids)
            voids.remove((ry, rx))
        else:
            ry, rx = random.randint(0, height - 1), random.randint(0, width - 1)
        phoenixes.append((ry, rx))
        new_grid[ry][rx] = 19

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
            if grid[ny][nx] != 10 and grid[ny][nx] != 17 and grid[ny][nx] != 20 and (ny, nx) not in godzilla_targets:
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
                if grid[ny][nx] != 11 and grid[ny][nx] != 17 and grid[ny][nx] != 20 and (ny, nx) not in jaeger_targets:
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
            if grid[ny][nx] != 12 and grid[ny][nx] != 17 and grid[ny][nx] != 20 and (ny, nx) not in mothra_targets:
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
                if grid[ny][nx] != 15 and grid[ny][nx] != 17 and grid[ny][nx] != 20 and (ny, nx) not in mechagodzilla_targets:
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
                if grid[ny][nx] != 15 and grid[ny][nx] != 17 and grid[ny][nx] != 20 and (ny, nx) not in mechagodzilla_targets:
                    mechagodzilla_targets.add((ny, nx))
                    moved = True
                    break
            if not moved:
                mechagodzilla_targets.add((mgy, mgx))

    # 2.8 RESOLVE OMEGA MOVEMENT (random movement)
    # 2.9 RESOLVE REAPER MOVEMENT (random movement)
    reaper_targets = set()
    for ry, rx in reapers:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        moved = False
        for dy, dx in directions:
            ny, nx = (ry + dy) % height, (rx + dx) % width
            # Reapers can move anywhere except where another Reaper is targeting
            if grid[ny][nx] != 18 and grid[ny][nx] != 20 and (ny, nx) not in reaper_targets:
                reaper_targets.add((ny, nx))
                moved = True
                break
        if not moved:
            reaper_targets.add((ry, rx))
    omega_targets = set()
    for oy, ox in omegas:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        moved = False
        for dy, dx in directions:
            ny, nx = (oy + dy) % height, (ox + dx) % width
            # Valid target if it does not contain an Omega in the current grid and is not targeted by another, and is not a Nexus
            if grid[ny][nx] != 16 and grid[ny][nx] != 17 and grid[ny][nx] != 20 and (ny, nx) not in omega_targets:
                omega_targets.add((ny, nx))
                moved = True
                break
        if not moved:
            omega_targets.add((oy, ox))

    phoenix_targets = set()
    for py, px in phoenixes:
        if reapers:
            # Find nearest Reaper
            nearest_r = None
            min_dist = float('inf')
            for ry, rx in reapers:
                dist = abs(ry - py) + abs(rx - px)
                if dist < min_dist:
                    min_dist = dist
                    nearest_r = (ry, rx)

            if nearest_r:
                ry, rx = nearest_r
                # Move one step towards Reaper
                dy, dx = 0, 0
                if ry > py: dy = 1
                elif ry < py: dy = -1
                elif rx > px: dx = 1
                elif rx < px: dx = -1

                ny, nx = (py + dy) % height, (px + dx) % width
                if grid[ny][nx] != 19 and grid[ny][nx] != 20 and (ny, nx) not in phoenix_targets:
                    phoenix_targets.add((ny, nx))
                else:
                    phoenix_targets.add((py, px))
            else:
                phoenix_targets.add((py, px))
        else:
            # Reapers gone, move randomly
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            moved = False
            for dy, dx in directions:
                ny, nx = (py + dy) % height, (px + dx) % width
                if grid[ny][nx] != 19 and grid[ny][nx] != 20 and (ny, nx) not in phoenix_targets:
                    phoenix_targets.add((ny, nx))
                    moved = True
                    break
            if not moved:
                phoenix_targets.add((py, px))

    # 2.12 RESOLVE NIDHOGG MOVEMENT (seeking nearest Yggdrasil)
    nidhogg_targets = set()
    for ny_pos, nx_pos in nidhoggs:
        if yggdrasils:
            # Find nearest Yggdrasil
            nearest_y = None
            min_dist = float('inf')
            for yy, yx in yggdrasils:
                dist = abs(yy - ny_pos) + abs(yx - nx_pos)
                if dist < min_dist:
                    min_dist = dist
                    nearest_y = (yy, yx)

            if nearest_y:
                yy, yx = nearest_y
                # Move one step towards Yggdrasil
                dy, dx = 0, 0
                if yy > ny_pos: dy = 1
                elif yy < ny_pos: dy = -1
                elif yx > nx_pos: dx = 1
                elif yx < nx_pos: dx = -1

                ny_next, nx_next = (ny_pos + dy) % height, (nx_pos + dx) % width
                if grid[ny_next][nx_next] != 21 and grid[ny_next][nx_next] != 17 and (ny_next, nx_next) not in nidhogg_targets:
                    nidhogg_targets.add((ny_next, nx_next))
                else:
                    nidhogg_targets.add((ny_pos, nx_pos))
            else:
                nidhogg_targets.add((ny_pos, nx_pos))
        else:
            # Move randomly
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            moved = False
            for dy, dx in directions:
                ny_next, nx_next = (ny_pos + dy) % height, (nx_pos + dx) % width
                if grid[ny_next][nx_next] != 21 and grid[ny_next][nx_next] != 17 and (ny_next, nx_next) not in nidhogg_targets:
                    nidhogg_targets.add((ny_next, nx_next))
                    moved = True
                    break
            if not moved:
                nidhogg_targets.add((ny_pos, nx_pos))

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

    # 3.4 RESOLVE CHRONOS CLEANSE
    chronos_targets = set()
    chronos_cleansed = {}
    for cy, cx in chronos:
        # Move randomly
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        moved = False
        for dy, dx in directions:
            ny, nx = (cy + dy) % height, (cx + dx) % width
            if grid[ny][nx] not in [17, 20, 22] and (ny, nx) not in chronos_targets:
                chronos_targets.add((ny, nx))
                moved = True
                break
        if not moved:
            chronos_targets.add((cy, cx))

        # Cleanse 3x3 area around original position
        for i in range(-1, 2):
            for j in range(-1, 2):
                ey, ex = (cy + i) % height, (cx + j) % width
                if grid[ey][ex] in [7, 8, 9, 22]:
                    chronos_cleansed[(ey, ex)] = random.choice([0, 1, 2, 3, 4])

    # 3.4.5 RESOLVE PARADOX MOVEMENT AND TIME ANOMALIES
    paradox_targets = set()
    time_anomalies = {}
    for py, px in paradoxes:
        # Paradox seeks Chronos
        best_dist = float('inf')
        best_moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue
                ny, nx = (py + i) % height, (px + j) % width
                if grid[ny][nx] not in [17, 20] and (ny, nx) not in paradox_targets:
                    min_c_dist = float('inf')
                    for cy, cx in chronos:
                        dist = abs(ny - cy) + abs(nx - cx)
                        # Handle wrapping
                        dist = min(dist, abs(ny - (cy + height)) + abs(nx - cx), abs(ny - cy) + abs(nx - (cx + width)), abs(ny - (cy + height)) + abs(nx - (cx + width)))
                        if dist < min_c_dist:
                            min_c_dist = dist

                    if min_c_dist < best_dist:
                        best_dist = min_c_dist
                        best_moves = [(ny, nx)]
                    elif min_c_dist == best_dist:
                        best_moves.append((ny, nx))

        if best_moves and chronos:
            target_pos = random.choice(best_moves)
        else:
            # Move randomly if no Chronos
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            moved = False
            for dy, dx in directions:
                ny, nx = (py + dy) % height, (px + dx) % width
                if grid[ny][nx] not in [17, 20] and (ny, nx) not in paradox_targets:
                    target_pos = (ny, nx)
                    moved = True
                    break
            if not moved:
                target_pos = (py, px)

        paradox_targets.add(target_pos)

        # Check for collision with Chronos
        if target_pos in chronos_targets:
            # Collision creates Time Anomalies in a 3x3 area
            for i in range(-1, 2):
                for j in range(-1, 2):
                    ey, ex = (target_pos[0] + i) % height, (target_pos[1] + j) % width
                    if random.random() < 0.5:
                        time_anomalies[(ey, ex)] = 24 # Spawns more Paradoxes
                    else:
                        time_anomalies[(ey, ex)] = random.randint(0, 24)

    # 3.5 RESOLVE PANDORA'S BOX OPENING
    pandora_explosions = {}
    for py, px in pandoras:
        if ((py, px) in godzilla_targets or (py, px) in jaeger_targets or
            (py, px) in mothra_targets or (py, px) in mechagodzilla_targets or
            (py, px) in omega_targets or (py, px) in reaper_targets or
            (py, px) in phoenix_targets or (py, px) in nidhogg_targets or
            (py, px) in paradox_targets):

            # Pandora is touched! Unleash chaos in a 5x5 area
            for i in range(-2, 3):
                for j in range(-2, 3):
                    ey, ex = (py + i) % height, (px + j) % width
                    if i == 0 and j == 0:
                        pandora_explosions[(ey, ex)] = 9 # Pandora becomes a Wormhole
                    else:
                        # Full randomization of all states including Pandora and Paradox
                        pandora_explosions[(ey, ex)] = random.randint(0, 24)

    # 4. PRE-DETERMINE WORMHOLE QUANTUM TELEPORTATION TARGETS (to prevent cell overwrites)
    available_voids = [v for v in voids if v not in godzilla_targets and v not in mothra_targets and v not in jaeger_targets and v not in mechagodzilla_targets and v not in omega_targets and v not in reaper_targets and v not in phoenix_targets and v not in nidhogg_targets and v not in pandora_explosions and v not in chronos_targets and v not in paradox_targets and v not in time_anomalies]
    teleportation_targets = {}
    for wy, wx in wormholes:
        if available_voids:
            target_y, target_x = random.choice(available_voids)
            available_voids.remove((target_y, target_x))
            teleported_state = random.choice(wormhole_horizons) if wormhole_horizons else random.choice([0, 1, 2, 3, 4])
            teleportation_targets[(target_y, target_x)] = teleported_state

    beam_targets = set()
    blocking_states = {0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29}
    for ny, nx in neutron_stars_ortho:
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            cy, cx = (ny + dy) % height, (nx + dx) % width
            while grid[cy][cx] not in blocking_states and (cy, cx) != (ny, nx):
                beam_targets.add((cy, cx))
                cy, cx = (cy + dy) % height, (cx + dx) % width
            if grid[cy][cx] == 29:
                beam_targets.add((cy, cx))
    for ny, nx in neutron_stars_diag:
        for dy, dx in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            cy, cx = (ny + dy) % height, (nx + dx) % width
            while grid[cy][cx] not in blocking_states and (cy, cx) != (ny, nx):
                beam_targets.add((cy, cx))
                cy, cx = (cy + dy) % height, (cx + dx) % width
            if grid[cy][cx] == 29:
                beam_targets.add((cy, cx))

    # 5. MAIN CELLULAR AUTOMATON UPDATE PASS
    for y in range(height):
        for x in range(width):
            if (y, x) in chronos_cleansed:
                new_grid[y][x] = chronos_cleansed[(y, x)]
                continue

            if (y, x) in time_anomalies:
                new_grid[y][x] = time_anomalies[(y, x)]
                continue

            if (y, x) in paradox_targets:
                new_grid[y][x] = 24
                continue

            if (y, x) in chronos_targets:
                new_grid[y][x] = 23
                continue

            # Check if this cell previously had a Chronos (leaves a Void)
            if grid[y][x] == 23:
                new_grid[y][x] = 6
                continue

            # Check if this cell previously had a Paradox (leaves a Void)
            if grid[y][x] == 24:
                new_grid[y][x] = 6
                continue

            # Check if this cell is caught in a Pandora's Box explosion
            if (y, x) in pandora_explosions:
                new_grid[y][x] = pandora_explosions[(y, x)]
                continue

            if (y, x) in conway_seeds:
                new_grid[y][x] = 26
                continue

            # Check if this cell is a target of a Nidhogg move (Nidhogg destroys everything here)
            if (y, x) in nidhogg_targets:
                new_grid[y][x] = 21
                continue

            # Check for Phoenix-Reaper collisions
            if (y, x) in phoenix_targets and (y, x) in reaper_targets:
                # Mutual destruction into a Nexus
                new_grid[y][x] = 17
                continue

            # Check if this cell is a target of a Phoenix move
            if (y, x) in phoenix_targets:
                new_grid[y][x] = 19
                continue

            # Check if this cell is a target of a Reaper move (Reaper destroys everything, including Nexus)
            if (y, x) in reaper_targets:
                new_grid[y][x] = 18
                continue

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

            # Check if this cell previously had a Phoenix (it has moved away leaving a Pulsar or Void)
            if grid[y][x] == 19:
                if random.random() < 0.10:
                    new_grid[y][x] = 8
                else:
                    new_grid[y][x] = 6
                continue

            # Check if this cell previously had a Reaper (it leaves behind a Void)
            if grid[y][x] == 18:
                new_grid[y][x] = 6
                continue

            # Check if this cell previously had a Nidhogg (it leaves behind a Void)
            if grid[y][x] == 21:
                new_grid[y][x] = 6
                continue

            # Check if this cell previously had an Omega (it leaves behind a Black Hole)
            if grid[y][x] == 16:
                new_grid[y][x] = 5
                continue

            if (y, x) in beam_targets:
                if grid[y][x] == 29:
                    new_grid[y][x] = 29
                    # Reproduce in adjacent void
                    neighbors = []
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0: continue
                            ny, nx = (y + i) % height, (x + j) % width
                            if grid[ny][nx] == 6:
                                neighbors.append((ny, nx))
                    if neighbors:
                        ty, tx = random.choice(neighbors)
                        new_grid[ty][tx] = 29
                else:
                    new_grid[y][x] = 8 # Beams turn cells into Pulsars
                continue

            # Check if this cell receives a quantum teleported state
            if (y, x) in teleportation_targets:
                new_grid[y][x] = teleportation_targets[(y, x)]
                continue

            current_state = grid[y][x]

            # --- STATE 22: PANDORA ---
            if current_state == 22:
                # Pandora remains dormant unless touched
                new_grid[y][x] = 22
                continue

            # --- STATE 17: NEXUS ---
            if current_state == 17:
                nexus_neighbors = sum(
                    1 for i in range(-1, 2) for j in range(-1, 2)
                    if not (i == 0 and j == 0) and grid[(y + i) % height][(x + j) % width] == 17
                )
                if nexus_neighbors == 8 and random.random() < 0.01:
                    new_grid[y][x] = 20 # Crystallizes into Yggdrasil
                elif random.random() < 0.001: # 0.1% chance to decay
                    new_grid[y][x] = 6
                else:
                    new_grid[y][x] = 17
                continue

            # --- STATE 20: YGGDRASIL ---
            if current_state == 20:
                if len(yggdrasils) > 5 and random.random() < 0.05:
                    new_grid[y][x] = 7 # Decays to Supernova
                else:
                    new_grid[y][x] = 20
                    if random.random() < 0.05:
                        # Convert random adjacent Void or RPSLK cell to Nexus
                        neighbors = []
                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                if i == 0 and j == 0: continue
                                ny, nx = (y + i) % height, (x + j) % width
                                if grid[ny][nx] in [6, 0, 1, 2, 3, 4]:
                                    neighbors.append((ny, nx))
                        if neighbors:
                            ty, tx = random.choice(neighbors)
                            new_grid[ty][tx] = 17
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

            # --- STATES 27 & 28: NEUTRON STARS ---
            if current_state in [27, 28]:
                new_grid[y][x] = current_state
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

            # --- STATE 29: RADIOTROPH ---
            elif current_state == 29:
                if random.random() < 0.05:
                    new_grid[y][x] = 6 # Decays into Void (5% chance)
                else:
                    new_grid[y][x] = 29
                continue

            # --- STATE 25: SINGULARITY ---
            elif current_state == 25:
                new_grid[y][x] = 25
                # Consume all neighbors
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0: continue
                        ny, nx = (y + i) % height, (x + j) % width
                        new_grid[ny][nx] = 25
                continue

            # --- STATE 6: VOID ---
            elif current_state == 6:
                # count 26 neighbors
                conway_neighbors = sum(
                    1 for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not (i == 0 and j == 0) and grid[(y + i) % height][(x + j) % width] == 26
                )
                if conway_neighbors == 3:
                    new_grid[y][x] = 26
                    continue

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
                    elif rand_val < 0.0515:
                        new_grid[y][x] = 18
                    elif rand_val < 0.052:
                        new_grid[y][x] = 19
                    elif rand_val < 0.0521:
                        new_grid[y][x] = 22
                    elif rand_val < 0.05211:
                        new_grid[y][x] = 25
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

            # --- STATE 26: CONWAY ---
            elif current_state == 26:
                conway_neighbors = sum(
                    1 for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not (i == 0 and j == 0) and grid[(y + i) % height][(x + j) % width] == 26
                )
                if conway_neighbors in [2, 3]:
                    new_grid[y][x] = 26
                else:
                    new_grid[y][x] = 6 # Decays to Void
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
    <h2>Rock-Paper-Scissors-Spock-Lizard with Wormhole Singularity, Godzilla, Jaeger, Mothra, Glitch, MechaGodzilla, Omega, Nexus, Phoenix, Yggdrasil, Nidhogg, Pandora, Chronos & Paradox</h2>
    <canvas id="simCanvas" width="{width * 5}" height="{height * 5}"></canvas>
    <p>Red: Rock | Green: Paper | Blue: Scissors | Purple: Spock | Yellow: Lizard | Black: Black Hole | Gray: Void | White: Supernova | Cyan: Pulsar | Magenta: Wormhole | Orange: Godzilla | Silver: Jaeger | Gold: Mothra | Neon Green: Glitch | Deep Sky Blue: Anti-Virus | Crimson Red: MechaGodzilla | Blue Violet: Omega | Light Cyan: Nexus | Dark Gray: Reaper | Coral: Phoenix | Forest Green: Yggdrasil | Dark Red: Nidhogg | Deep Pink: Pandora | Royal Blue: Chronos | Dark Violet: Paradox | Pure White: Singularity | Lavender: Neutron Star Ortho | Thistle: Neutron Star Diag | Chartreuse: Radiotroph</p>

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
            17: '#e0ffff', // Nexus
            18: '#555555', // Reaper
            19: '#ff7f50', // Phoenix
            20: '#228b22', // Yggdrasil
            21: '#8b0000', // Nidhogg
            22: '#ff1493', // Pandora
            23: '#4169e1', // Chronos
            24: '#9400d3', // Paradox
            25: '#ffffff',  // Singularity
            26: '#00ff00',  // Conway
            27: '#e6e6fa', // Neutron Star Ortho
            28: '#d8bfd8', // Neutron Star Diag
            29: '#7fff00'  // Radiotroph
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
