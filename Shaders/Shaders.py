import pyglet.gl as gl
from ctypes import byref, sizeof

class Shader:
    def __init__(self, vertShaderPath, fragShaderPath):
        self.glProgram = gl.glCreateProgram()

        # init vertex shader
        self.vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        initShader(self.vertexShader, vertShaderPath)
        gl.glAttachShader(self.glProgram, self.vertexShader)

        # init fragment shader
        self.fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        initShader(self.fragmentShader, fragShaderPath)
        gl.glAttachShader(self.glProgram, self.fragmentShader)

        gl.glLinkProgram(self.glProgram)

        gl.glDeleteShader(self.vertexShader)
        gl.glDeleteShader(self.fragmentShader)

    def use(self):
        gl.glUseProgram(self.glProgram)

    def delete(self):
        gl.glDeleteProgram(self.glProgram)

    def getUniformInShaders(self, name):
        return gl.glGetUniformLocation(self.glProgram, ctypes.create_string_buffer(name))

    def passMatrixToShaders(self, dest, mat):
        gl.glUniformMatrix4fv(dest, 1, gl.GL_FALSE, (gl.GLfloat * 16) (*sum(mat.getPyMatrix(), [])))

def initShader(shader, path):
    # read shader file
    tempFile = open(path, "rb")
    shaderDest = tempFile.read()
    tempFile.close()

    # compile shader
    pointerToBuffer = ctypes.cast(ctypes.pointer(ctypes.pointer(ctypes.create_string_buffer(shaderDest))), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))

    gl.glShaderSource(shader, 1, pointerToBuffer, ctypes.byref(ctypes.c_int(len(shaderDest) + 1)))
    gl.glCompileShader(shader)

    # handle errors
    logLength = gl.GLint(0)
    gl.glGetShaderiv(shader, gl.GL_INFO_LOG_LENGTH, ctypes.byref(logLength))
    
    stringBuffer = ctypes.create_string_buffer(logLength.value)
    gl.glGetShaderInfoLog(shader, logLength, None, stringBuffer)

    if logLength:
        raise ShaderErrorHandler(str(stringBuffer.value))

class ShaderErrorHandler(Exception):
    def __init__(self, error):
        self.error = error