import re

with open('simulation.py', 'r') as f:
    content = f.read()

content = re.sub(
    r'(Light Pink: Mi-Go \| Slate Gray: Brain Cylinder)(</p>)',
    r'\1 | Tan: Yithian | Dark Slate Blue: Flying Polyp\2',
    content, count=1
)

with open('simulation.py', 'w') as f:
    f.write(content)
