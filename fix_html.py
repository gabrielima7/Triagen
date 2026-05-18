with open("simulation.py", "r") as f:
    content = f.read()

content = content.replace(
"""                8: '#00ffff', // Pulsar
                9: '#ff00ff'  // Wormhole
            };""",
"""                8: '#00ffff', // Pulsar
                9: '#ff00ff', // Wormhole
                10: '#ff7f00' // Godzilla
            };""")

with open("simulation.py", "w") as f:
    f.write(content)
