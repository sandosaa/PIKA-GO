# Pika Go! 

Pika Go! is an action-packed 2D platformer built with **Python** and **Pygame**. Navigate through levels, defeat enemies, and collect flowers to win!

##  Features

- **Smooth Platforming:** Responsive controls with gravity, jumping, and collision detection.
- **Dynamic Camera:** A custom camera system that keeps the player centered on the screen.
- **Combat System:** Shoot bullets to defeat various enemies like Bats and Worms[cite: 10, 13].
- **Health Management:** A visual health bar using heart sprites that reflect current player health.
- **Animated Sprites:** Fully animated characters and enemies for an immersive experience.
- **Level Loading:** Integration with Tiled Map Editor (.tmx files) for complex level designs.

##  Technical Details

- **Language:** Python
- **Library:** Pygame, PyTMX
- **Resolution:** 1280x720
- **Framerate:** 60 FPS

##  Getting Started

### Prerequisites
- Python 3.x
- Pygame-ce library
- PyTMX library

## Installation
#### Clone the repository:
```bash
git clone https://github.com/sandosaa/PIKA-GO.git
```
#### Navigate to the project folder:
```bash
cd pika-go
```
#### Install dependencies:
```bash
pip install -r requirement.txt
```
#### Run the game:
```bash
python src/main.py
```

#### Controls

    Arrow Keys: Move Left/Right and Jump (Up).  

    Spacebar: Shoot

#### Project Structure
```bash 
pika_go/
    ├── src/
    │   ├── main.py
    │   ├── groups.py
    │   ├── heartmanage.py
    │   ├── settime.py
    │   ├── settings.py
    │   ├── sprites.py
    │   ├── support.py
    ├── assets/
    │   ├── audio/
    │   ├── data/
    │   │   ├── graphics/
    │   │   ├── maps/
    │   │   ├── tilesets/
    │   ├── font/
    │   │   └── deltarune.ttf
    │   └── images/
    ├── requirement.txt
    └── README.md

```
#### How to Win

Collect at least 200 flowers and reach Pika to trigger the victory state! If you have fewer than 200, Pika will be sad, and you'll need to keep exploring.
### License

This project is open-source. Feel free to use and modify!
