import re

with open('simulation.py', 'r') as f:
    content = f.read()

content = re.sub(
    r'(</p>)',
    r' | Fuchsia: The Color Out of Space | Dark Slate Gray: Blighted Soil | Light Gray: Ashen Dust\1',
    content,
    count=1
)

content = content.replace(
    "            51: '#2e8b57'  // Dagon\n        }};",
    "            51: '#2e8b57', // Dagon\n            52: '#ff00ff', // The Color Out of Space\n            53: '#2f4f4f', // Blighted Soil\n            54: '#d3d3d3'  // Ashen Dust\n        }};"
)

with open('simulation.py', 'w') as f:
    f.write(content)
