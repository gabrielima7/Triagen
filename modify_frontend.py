import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Modify h2 title
content = re.sub(r'(<h2>.*?)(</h2>)', r'\1, Elder Thing\2', content)

# Modify p legend
content = re.sub(r'(<p>Red: Rock \|.*?)(</p>)', r'\1 | SeaGreen: Elder Thing\2', content)

# Add color dictionary mapping safely before the inline comment
color_addition = ",\n            60: '#2e8b57'  // Elder Thing"
content = re.sub(r'(59:\s*\'#191970\')(\s*//\s*Hound of Tindalos)', r'\1' + color_addition + r'\2', content)

with open('simulation.py', 'w') as f:
    f.write(content)
