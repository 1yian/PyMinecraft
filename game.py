import pyglet
import pyglet.gl as gl
import glm
from cube import Cube
from ctypes import byref, sizeof
import camera

MIN_SIZE = 50


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(MIN_SIZE, MIN_SIZE)

        self.camera = camera.Camera()

        # Initialize VAO
        self.VAO = gl.GLuint(0)
        gl.glGenVertexArrays(1, byref(self.VAO))
        gl.glBindVertexArray(self.VAO)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(0)

        # Initialize vertex VBO
        self.vertex_VBO = gl.GLuint(0)
        gl.glGenBuffers(1, byref(self.vertex_VBO))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_VBO)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(gl.GLfloat * len(Cube.VERTICES)),
                        (gl.GLfloat * len(Cube.VERTICES))(*Cube.VERTICES), gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(1)

        # Initialize index BO
        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, self.ibo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, sizeof(gl.GLuint * len(Cube.INDICES)),
                        (gl.GLuint * len(Cube.INDICES))(*Cube.INDICES), gl.GL_STATIC_DRAW)
        
        self.pause = False
        self.set_exclusive_mouse(True)

    def update(self, dt):
        if self.pause:
            self.camera.movementInput = [0, 0, 0]
        self.camera.changeCameraOrientation(dt)

    def on_draw(self):
        self.camera.updateMVP(shader, self.width, self.height)
        self.clear()

    def on_resize(self, width, height):
        print(f"Resize {width} * {height}") # print out window size
        gl.glViewport(0, 0, width, height)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_movement_action(dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse_movement_action(dx, dy)

    def mouse_movement_action(self, dx, dy):
        if not self.pause:
            sens = 0.001
            self.camera.rotation[0] -= sens * dx
            self.camera.rotation[1] += sens * dy

            forward = math.tau / 4
            self.camera.rotation[1] = max(min(forward, self.camera.rotation[1]), -forward) # don't want to snap the character's neck

if __name__ == "__main__":
    window = Window(width = 400, height = 400, caption = 'Minecraft')
    gl.glClearColor(0.5, 0.7, 1, 1)
    pyglet.app.run()
