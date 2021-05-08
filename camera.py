import math
import matrix_pyglm
import glm

forward = math.tau / 4

class Camera:
    def __init__(self):
        self.projectionMatrix = matrix_pyglm.MatrixGLM4D(glm.mat4(1.0))
        self.modelviewMatrix = matrix_pyglm.MatrixGLM4D(glm.mat4(1.0))

        self.currentPosition = [0, 0, -3]
        self.currentRotation = [forward, 0]

        self.movementInput = [0, 0, 0]

    def changeCameraOrientation(self, dt):
        distanceUnit = 5 * dt

        if self.movementInput[0] or self.movementInput[2]:
            theta = self.currentRotation[0] + math.atan2(self.movementInput[2], self.movementInput[0]) - forward
            self.currentPosition[0] += math.cos(theta) * distanceUnit
            self.currentPosition[2] += math.sin(theta) * distanceUnit
        self.currentPosition[1] += self.movementInput[1] * distanceUnit
    
    def updateMVP(self, shader, windowWidth, windowHeight):
        # projection matrix
        self.projectionMatrix.alter(glm.perspective(math.radians(90), float(self.windowWidth) / self.windowHeight, 0.1, 500))

        # model-view matrix
        self.modelviewMatrix.alter(glm.mat4(1.0))
        self.modelviewMatrix.alter(glm.rotate(self.modelviewMatrix.getGLMMatrix(), -(self.currentRotation[0] - forward), glm.vec3(0, 1, 0)))
        self.modelviewMatrix.alter(glm.rotate(self.modelviewMatrix.getGLMMatrix(), -self.currentRotation[1], 
                                    glm.vec3(math.cos(-(self.currentRotation[0] - forward)), 0, math.sin(-(self.currentRotation[0] - forward)))))
        self.modelviewMatrix.alter(glm.translate(self.modelviewMatrix.getGLMMatrix(), glm.vec3(-self.currentPosition[0], -self.currentPosition[1], self.currentPosition[2])))

        # MVP matrix
        mvpMatrix = matrix_pyglm.MatrixGLM4D((self.projectionMatrix.getGLMMatrix()) * (self.modelviewMatrix.getGLMMatrix()))
        # Send MVP matrix to shader
        shader.passMatrixToShaders(shader.getUniformInShaders(b"mvpMatrix"), mvpMatrix)