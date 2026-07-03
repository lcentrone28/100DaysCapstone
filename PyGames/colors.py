import random

colors = []

for c in range(100):
    style = random.choice(["red", "pink", "magenta", "fuchsia", "purple", "violet", "blue", "cyan", "teal", "lime", "green",
                           "yellow", "orange"])
    if style == "red":
        colors.append((random.randint(240, 255), random.randint(30, 60), random.randint(0, 20)))
    elif style == "pink":
        colors.append((random.randint(240, 255), random.randint(20, 80), random.randint(140, 180)))
    elif style == "magenta":
        colors.append((random.randint(240, 255), random.randint(0, 20), random.randint(240, 255)))
    elif style == "fuchsia":
        colors.append((random.randint(180, 220), random.randint(0, 20), random.randint(180, 255)))
    elif style == "purple":
        colors.append((random.randint(120, 160), random.randint(0, 20), random.randint(240, 255)))
    elif style == "violet":
        colors.append((random.randint(140, 180), random.randint(30, 70), random.randint(240, 255)))
    elif style == "blue":
        colors.append((random.randint(0, 20), random.randint(100, 160), random.randint(240, 255)))
    elif style == "cyan":
        colors.append((random.randint(0, 20), random.randint(240, 255), random.randint(240, 255)))
    elif style == "teal":
        colors.append((random.randint(0, 20), random.randint(180, 220), random.randint(160, 200)))
    elif style == "lime":
        colors.append((random.randint(130, 170), random.randint(240, 255), random.randint(0, 20)))
    elif style == "green":
        colors.append((random.randint(0, 20), random.randint(240, 255), random.randint(0, 20)))
    elif style == "yellow":
        colors.append((random.randint(240, 255), random.randint(240, 255), random.randint(0, 20)))
    elif style == "orange":
        colors.append((random.randint(240, 255), random.randint(100, 150), random.randint(0, 20)))

reds = []

for c in range(100):
    style = random.choice(["red", "pink", "magenta"])

    if style == "red":
        reds.append((random.randint(240, 255), random.randint(30, 60), random.randint(0, 20)))
    elif style == "pink":
        reds.append((random.randint(240, 255), random.randint(20, 80), random.randint(140, 180)))
    elif style == "magenta":
        reds.append((random.randint(240, 255), random.randint(0, 20), random.randint(240, 255)))

greens = []

for c in range(100):
    style = random.choice(["teal", "lime", "green"])

    if style == "teal":
        greens.append((random.randint(0, 20), random.randint(180, 220), random.randint(160, 200)))
    elif style == "lime":
        greens.append((random.randint(130, 170), random.randint(240, 255), random.randint(0, 20)))
    elif style == "green":
        greens.append((random.randint(0, 20), random.randint(240, 255), random.randint(0, 20)))

def text_color(button_color):
    r, g, b = button_color

    brightness = (r * 0.3) + (g * 0.6) + (b * 0.1)

    if brightness > 125:
        return "black"
    else:
        return "white"