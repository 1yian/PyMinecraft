Name1: Yian Wong
eid1: yw23342
Name2: Randy Yu 
eid2: ry4272

This project is an infinitely large voxel world that the user may interact with using mouse and keyboard controls.
The content is as follows: The game.py files creates the window for the world as well as handles inputs and puts everything together;
the shaders folder contains the shaders for our project (it's how we display stuff onto the GPU); the textures.py file procedurally generates
textures for the block faces to use; the camera.py file updates the camera's orientation and the Model-View-Projection Matrix that 
makes the scene 3 dimensional; the chunk.py file contains everything needed to load chunks into the world; the matrix_pyglm.py
file makes it easy to convert glm matrices into python matrices so that it's convenient to pass into shaders; the world.py file
generates chunks and draws them onto the window. 

HOW TO RUN THE PROJECT DEMO:
1. Install Python and PIP from https://www.python.org/
2. Install the following libraries:
Pyglet
PyGLM
NumPy
perlin_noise
3. Change Directory into the root directory
4. Type in the following line: Python game.py

HOW TO OPERATE INSIDE THE DEMO:
'WASD' to move your camera
'Mouse Button 1' to break a block
'Mouse Button 2' to place a block
'Mouse Button 3' to select a block to be placed
'R' to toggle fast traveling
'Escape' to pause the game
'Shift' to move down
'Space' to move up

On my honor, I have submitted the eCIS survey.
Signed:
Yian Wong
Randy Yu