import math
import matrix_pyglm
import glm

class Camera:
    def __init__(self, shader, width, height):
        self.width = width
        self.height = height

        # model view matrix and projection matrix
        self.mv_matrix = matrix_pyglm.MatrixGLM4D(glm.mat4(1.0))
        self.p_matrix = matrix_pyglm.MatrixGLM4D(glm.mat4(1.0))

        self.shader = shader
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")

        #position and rotation
        self.position = [0, 0, -3]
        self.rotation = [math.tau / 4, 0]

        #input
        self.input = [0, 0, 0]

    def update_camera(self, dt):
        speed = 7
        multiplier = speed * dt

        self.position[1] += self.input[1] * multiplier

        if self.input[0] or self.input[2]:
            angle = self.rotation[0] + math.atan2(self.input[2], self.input[0]) - math.tau / 4
            self.position[0] += math.cos(angle) * multiplier
            self.position[2] += math.sin(angle) * multiplier

    def update_matrices(self):
        # projection matrix
        self.p_matrix.alter(glm.perspective(math.radians(90), float(self.width) / self.height, 0.1, 500))

        # model view matrix
        self.mv_matrix.alter(glm.mat4(1.0))
        self.mv_matrix.alter(glm.rotate(self.mv_matrix.getGLMMatrix(), -(self.rotation[0] - math.tau / 4), glm.vec3(0, 1, 0)))
        self.mv_matrix.alter(glm.rotate(self.mv_matrix.getGLMMatrix(), -self.rotation[1], glm.vec3(math.cos(-(self.rotation[0] - math.tau / 4)), 0, math.sin(-(self.rotation[0] - math.tau / 4)))))
        self.mv_matrix.alter(glm.translate(self.mv_matrix.getGLMMatrix(), glm.vec3(-self.position[0], -self.position[1], self.position[2])))

        #mvp matrix
        mvp_matrix = matrix_pyglm.MatrixGLM4D((self.p_matrix.getGLMMatrix()) * (self.mv_matrix.getGLMMatrix()))
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)