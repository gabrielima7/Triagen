import sys
# Write down the changes requested by the next agent
# We will create state 52 (Cthulhi / Star-Spawn of Cthulhu)
# State 52: Star-Spawn of Cthulhu
# Characteristics:
# - Spawns very rarely
# - Wander randomly
# - If they find Cthulhu or Sleeping Cthulhu, they orbit it.
# Let's think of something more chaotic. The prompt says "I have absolute freedom". Let's introduce the concept of "The Color Out of Space", State 52.
# "The Color Out of Space" (State 52)
# Spawns at 0.005%.
# Visualized as `#ff00ff` (Magenta/Fuchsia).
# Wanders randomly. As it wanders, it leaves behind "Blighted Soil" (State 53).
# Blighted Soil (State 53): Spawns at 0%. Visualized as `#555555`.
# Any entity that walks into Blighted Soil has a 50% chance of turning into "Ashen Dust" (State 54).
# Ashen Dust (State 54): Spawns at 0%. Visualized as `#aaaaaa`. Slowly fades into Void (State 6) with 5% chance per turn.

# I need to update:
# 1. states list and weights
# 2. chars mapping
# 3. blocking_states
# 4. update_grid logic
# 5. HTML generation
