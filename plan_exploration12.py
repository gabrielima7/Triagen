# Yithian logic (State 57)
# For the mind swap logic, if we swap with target, do we swap grid positions?
# "The target is instantly swapped with a Yithian (57) and the original Yithian becomes the target's original state"
# Meaning new_grid[y][x] = target_state
# and global_modifications[(target_y, target_x)] = 57
# This implies the Yithian itself "becomes" the target's original state, and the target's position becomes the Yithian.
# This means the Yithian is effectively teleported to the target, and the target is teleported to the Yithian's original position.
# We will check if len(yithian_targets) > 0 and random.random() < 0.02.
# If so, pick a target. We can set new_grid[y][x] = grid[ty][tx], and global_modifications[(ty, tx)] = 57.
# If not swapping, wander randomly (similar to Mi-Go or Dagon).

# Flying Polyp logic (State 58)
# Wander aggressively: meaning it moves into the space of its victim?
# "If they encounter a Yithian (57), they instantly destroy it, leaving a Void (6)."
# "If they encounter basic lifeforms (0-4) or Cultists (40), they also destroy them into Void (6)."
# Let's say it looks for a target among neighbors. If found, it moves into that space and leaves a Void?
# Or maybe it just attacks adjacent targets, turning them to Void.
# Actually, the phrasing "they instantly destroy it, leaving a Void (6)" could mean that they turn it to Void instead of moving into it.
# Let's just have them attack adjacent targets and turn them into Void.
# And they wander randomly.
# "They have a 1% chance per turn to spawn a new Flying Polyp in an adjacent Void."
