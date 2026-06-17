# Yithian logic (State 57)
# 2% chance per turn to mind swap with a target.
# Mind swap:
#   target_y, target_x = random.choice(yithian_targets)
#   new_grid[y][x] = current_state_of_target (which is grid[target_y][target_x])
#   global_modifications[(target_y, target_x)] = 57 # Target becomes Yithian
# Otherwise, random walk.

# Flying Polyp logic (State 58)
# Random walk.
# If grid[ny][nx] == 57: new_grid[cy][cx] = 6, new_grid[ny][nx] = 58 # destroy Yithian (void left behind? Or destroy Yithian into void and move there?)
# wait, "If they encounter a Yithian (57), they instantly destroy it, leaving a Void (6)."
# "If they encounter basic lifeforms (0-4) or Cultists (40), they also destroy them into Void (6)."
# This means: Flying Polyp moves to the space, leaving Void behind itself? Or it just turns them into Void?
# "If they encounter a Yithian (57), they instantly destroy it, leaving a Void (6)."
# That probably means the space where the Yithian was becomes Void.
# Actually, if they "encounter" them, they probably just wander into their space and turn them into Void, while the Polyp moves or stays?
# Let's say: when moving, if target is 57, 0, 1, 2, 3, 4, 40 -> the target becomes Void (6) and Polyp moves there? Or Polyp moves there and leaves Void behind?
# Or just "destroys them leaving a Void" means the Polyp doesn't move there, it just attacks and leaves Void?
# Actually, if they wander aggressively, it's typical to move into the space and turn them to Void... wait, if the Polyp moves to the space, it occupies the space, so the space becomes 58. Where does the Void go?
# Ah, maybe they destroy it and move there, and leave Void behind? That's just normal movement (leaving 6 behind).
# Maybe it means: they destroy them, meaning the target cell becomes Void, but the Polyp stays?
# Let's implement it as: if target is 57/0-4/40, target becomes 6, Polyp stays.
# Let's look at similar entities. Shoggoth? Deep One? Ahab?
