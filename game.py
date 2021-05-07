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

        self.camera = camera.Camera(self.shader, self.width, self.height)

        # Initialize VAO
        self.VAO = gl.GLuint(0)
        gl.glGenVertexArrays(byref(self.VAO))
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

        # Initialize model matrix, perspective

    def update(self, t):
        if not self.mouse_captured:
            self.camera.input = [0, 0, 0]
        self.camera.update_camera(t)

    def on_draw(self):
        self.clear()


if __name__ == "__main__":
    window = Window(width=400, height=400, caption='Minecraft')
    gl.glClearColor(0.5, 0.7, 1, 1)
    pyglet.app.run()
