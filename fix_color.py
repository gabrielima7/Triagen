import re

with open('simulation.py', 'r') as f:
    content = f.read()

content = content.replace("60: '#2e8b57'  // Elder Thing  // Hound of Tindalos", "60: '#2e8b57'  // Elder Thing")
content = content.replace("59: '#191970',", "59: '#191970',  // Hound of Tindalos")

with open('simulation.py', 'w') as f:
    f.write(content)
