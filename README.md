# CarGame

This is a simple Pygame-based car game. Steer your car to avoid oncoming obstacles using the arrow keys.

## Requirements

- Python 3.12 or compatible
- Pygame

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running the game

Run the main game script:

```bash
python car_game.py
```

A game window will open. Use the arrow keys to move your car freely around the screen.
Collect the green money blocks to earn points and grab yellow equipment boxes
for extra gear. Hitting a red obstacle subtracts money. The current scores are
displayed in the top-right corner. The timer in the top-left corner shows how
long you have survived. The road has four lanes with sidewalks and simple
buildings on the sides.

Cars appear most often, followed by small money, large money and finally the
yellow equipment crates.

If you hit too many red cars and your money drops below zero, a short crash
animation plays and the game ends. Click the **Restart** button to try again.

## Customizing graphics

The `assets.py` file contains placeholders for sprite images. Leave the paths
empty to use the built‑in colored rectangles, or replace them with file paths to
PNG images to give the game custom graphics.

