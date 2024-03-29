import pyglet
import pyglet.gl as gl
from world import World
from cube import Cube, CubeTypes
from textures.textures import TextureDict
import camera
import shaders.shaders as shaders
import math
import numpy

MIN_SIZE = 50


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(MIN_SIZE, MIN_SIZE)

        self.camera = camera.Camera()

        self.textures_dict = TextureDict(16, 16)

        self.cube_types = {

            CubeTypes.dirt: Cube(self.textures_dict, {
                'right': 'dirt',
                'left': 'dirt',
                'top': 'dirt',
                'bottom': 'dirt',
                'front': 'dirt',
                'back': 'dirt',
            }),

            CubeTypes.cobble: Cube(self.textures_dict, {
                'right': 'cobble',
                'left': 'cobble',
                'top': 'cobble',
                'bottom': 'cobble',
                'front': 'cobble',
                'back': 'cobble',
            }),

            CubeTypes.grass: Cube(self.textures_dict, {
                'right': 'grass_side',
                'left': 'grass_side',
                'top': 'grass',
                'bottom': 'dirt',
                'front': 'grass_side',
                'back': 'grass_side',
            }),
        }

        self.textures_dict.generate_mipmaps()

        self.world = World(self.cube_types)
        # init shader
        self.shader = shaders.Shader("shaders\VertexShader.glsl", "shaders\FragmentShader.glsl")
        self.shader.use()

        self.pause = False
        self.set_exclusive_mouse(True)

        self.currentBlockType = CubeTypes.air

        pyglet.clock.schedule_interval(self.update, 1.0 / 10000)

    def update(self, dt):
        if self.pause:
            self.camera.movementInput = [0, 0, 0]
        self.camera.changeCameraOrientation(dt)

    def on_draw(self):
        gl.glEnable(gl.GL_DEPTH_TEST)
        self.camera.updateMVP(self.shader, self.width, self.height)
        self.clear()
        self.world.draw(self.camera.currentPosition)
        

    def on_resize(self, width, height):
        gl.glViewport(0, 0, width, height)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_movement_action(dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse_movement_action(dx, dy)

    def mouse_movement_action(self, dx, dy):
        if not self.pause:
            sens = 0.001
            self.camera.currentRotation[0] += sens * dx
            self.camera.currentRotation[1] += sens * dy

            forward = math.tau / 4
            self.camera.currentRotation[1] = max(min(forward, self.camera.currentRotation[1]),
                                          -forward)  # don't want to snap the character's neck

    def on_mouse_press(self, x, y, button, modifiers):
        unitRay = self.camera.getRay()
        for distance in numpy.arange(0, 3, 0.1):
            pos = self.camera.currentPosition.copy()
            pos[0] += unitRay[0] * distance
            pos[1] += unitRay[1] * distance
            pos[2] += unitRay[2] * distance
            intersectedBlockType = self.world.get_block_type_at(pos)
            if button == pyglet.window.mouse.LEFT:
                if intersectedBlockType != CubeTypes.air:
                    self.world.set_block_type_at(pos, CubeTypes.air)
                    break
            elif button == pyglet.window.mouse.MIDDLE:
                if intersectedBlockType != CubeTypes.air:
                    self.currentBlockType = intersectedBlockType
                    break
            elif button == pyglet.window.mouse.RIGHT:
                tempPos = self.camera.currentPosition.copy()
                tempPos[0] += unitRay[0] * (distance - 0.1)
                tempPos[1] += unitRay[1] * (distance - 0.1)
                tempPos[2] += unitRay[2] * (distance - 0.1)
                if intersectedBlockType != CubeTypes.air:
                    if self.world.get_block_type_at(tempPos) == CubeTypes.air:
                        self.world.set_block_type_at(tempPos, self.currentBlockType)
                        break


    def on_key_press(self, key, modifiers):
        currKey = pyglet.window.key
        if not self.pause:
            if key == currKey.W:
                self.camera.movementInput[2] += 1
            elif key == currKey.A:
                self.camera.movementInput[0] -= 1
            elif key == currKey.S:
                self.camera.movementInput[2] -= 1
            elif key == currKey.D:
                self.camera.movementInput[0] += 1
            elif key == currKey.SPACE:
                self.camera.movementInput[1] += 1
            elif key == currKey.LSHIFT:
                self.camera.movementInput[1] -= 1
            elif key == currKey.R:
                self.camera.sprinting = not self.camera.sprinting
        if key == currKey.ESCAPE:
            self.pause = not self.pause
            self.set_exclusive_mouse(not self.pause)

    def on_key_release(self, key, modifiers):
        if not self.pause:
            currKey = pyglet.window.key
            if key == currKey.W:
                self.camera.movementInput[2] -= 1
            elif key == currKey.A:
                self.camera.movementInput[0] += 1
            elif key == currKey.S:
                self.camera.movementInput[2] += 1
            elif key == currKey.D:
                self.camera.movementInput[0] -= 1
            elif key == currKey.SPACE:
                self.camera.movementInput[1] -= 1
            elif key == currKey.LSHIFT:
                self.camera.movementInput[1] += 1


if __name__ == "__main__":
    window = Window(width = 1600, height = 900, caption = "Voxel World", resizable = True, vsync = False)
    gl.glClearColor(0.5, 0.7, 1, 1)
    pyglet.app.run()
