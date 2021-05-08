import pyglet.gl as gl
from ctypes import byref, sizeof

class Shader:
    def __init__(self, vertShaderPath, fragShaderPath):
        self.glProgram = gl.glCreateProgram()

        # init vertex shader
        self.vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        initShader(self.vertexShader, vertShaderPath) #todo
        gl.glAttachShader(self.glProgram, self.vertexShader)

        # init fragment shader
        self.fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        initShader(self.fragmentShader, fragShaderPath) #todo
        gl.glAttachShader(self.glProgram, self.fragmentShader)

        gl.glLinkProgram(self.glProgram)

        gl.glDeleteShader(self.vertexShader)
        gl.glDeleteShader(self.fragmentShader)

def initShader(shader, path):
    