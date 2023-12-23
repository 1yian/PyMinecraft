# Minecraft in OpenGL

This is our final project repository for CS378H: Computer Graphics with Prof. Etienne Vouga. We recreated the iconic look and feel of Minecraft using modern OpenGL and Pyglet. This project gave us insight into procedural terrain generation using Perlin noise and 3D graphics programming.


## Features
- Custom Graphics Engine: Built using Pyglet and OpenGL, the engine renders Minecraft-like blocks in a 3D space.
- Texture Management: Custom textures for blocks, including grass, dirt, cobblestone, and more.
- Procedural Terrain Generation: Perlin noise for randomized terrain generation.
- Shader Implementation: Utilizes vertex and fragment shaders for rendering the blocks.
- Interactive Camera: A comprehensive camera system that allows you to navigate through the 3D world.

## Installation

This project uses Pyglet, a cross-platform windowing and multimedia library for Python. We also use perlin_noise and NumPy for computation. Install them using pip:
```
pip install pyglet pyglm numpy perlin_noise
```

## Usage

Start the game by running:
```
python game.py
```

## Gameplay
- `W A S D` to move your camera
- `M1` to break a block, 'M2' to place one
- `R` to toggle fast traveling
- `ESC` to pause the game
- `SHIFT` to move down
- `SPACE` to move up

## Project Content
The content is as follows: 
- The `game.py` files creates the window for the world as well as handles inputs and puts everything together
- the `shaders` folder contains the shaders for our project (it's how we display stuff onto the GPU)
- the `textures.py` file procedurally generates textures for the block faces to use
- the `camera.py` file updates the camera's orientation and the Model-View-Projection Matrix that makes the scene 3 dimensional
- the `chunk.py` file contains everything needed to load chunks into the world
- the `matrix_pyglm.py` file makes it easy to convert glm matrices into python matrices so that it's convenient to pass into shaders
- the `world.py` file generates chunks and draws them onto the window



