import ctypes
from cube import Cube, CubeTypes
import pyglet.gl as gl
import math
import copy


# Represents a single mesh of the exposed faces of a chunk of cubes.
class Chunk:
    SIDE_LENGTH = 16

    def __init__(self, world_coord_pos, cube_types, world):

        # Set position variables
        self.world_coord_pos = world_coord_pos
        # Abstractly store each block in the chunk
        self.block_types = [[[CubeTypes.air for _ in range(Chunk.SIDE_LENGTH)] for _ in range(Chunk.SIDE_LENGTH)] for _
                            in
                            range(Chunk.SIDE_LENGTH)]

        self.world = world
        self.cube_types = cube_types
        self.generated = False

        # Initialize a VAO
        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1, self.vao)
        gl.glBindVertexArray(self.vao)

        # Initialize a VBO
        self.vertex_position_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, self.vertex_position_vbo)

        # Initialize a VBO for texture coordinates
        self.tex_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, self.tex_vbo)

        # Initialize a VBO for shading values
        self.shading_values_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, self.shading_values_vbo)

        # Initialize an IBO
        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, self.ibo)

        # Create internal data structures before passing them to GPU
        self.vertices = []
        self.tex_coords = []
        self.shading_values = []
        self.indices = []
        self.synced_with_gpu = False
        self.generate_chunk()

    def pass_to_gpu(self):
        self.vertices, self.tex_coords, self.shading_values, self.indices = [], [], [], []

        def add_face(face_type, position):
            x, y, z = position
            block_type = self.block_types[x][y][z]

            cube = self.cube_types[block_type]
            # print(cube.textures)
            positions, _, texture_coords, shading_vals = cube.get_face_info(face_type)

            xw, yw, zw = (self.world_coord_pos[0] + x,
                          self.world_coord_pos[1] + y,
                          self.world_coord_pos[2] + z)

            for i in range(4):
                positions[i * 3] += xw
                positions[i * 3 + 1] += yw
                positions[i * 3 + 2] += zw
            self.vertices += positions

            min_index = 0 if len(self.indices) == 0 else max(self.indices) + 1
            for idx in [0, 1, 2, 0, 2, 3]:
                self.indices.append(idx + min_index)

            self.tex_coords += texture_coords
            self.shading_values += shading_vals

        for x in range(Chunk.SIDE_LENGTH):
            for y in range(Chunk.SIDE_LENGTH):
                for z in range(Chunk.SIDE_LENGTH):
                    block_type = self.block_types[x][y][z]
                    if block_type != CubeTypes.air:
                        xw, yw, zw = (self.world_coord_pos[0] + x,
                                      self.world_coord_pos[1] + y,
                                      self.world_coord_pos[2] + z)

                        position = (x, y, z)

                        if self.world.get_block_type_at((xw + 1, yw, zw)) == CubeTypes.air:
                            add_face(0, position)
                        if self.world.get_block_type_at((xw - 1, yw, zw)) == CubeTypes.air:
                            add_face(1, position)
                        if self.world.get_block_type_at((xw, yw + 1, zw)) == CubeTypes.air:
                            add_face(2, position)
                        if self.world.get_block_type_at((xw, yw - 1, zw)) == CubeTypes.air:
                            add_face(3, position)
                        if self.world.get_block_type_at((xw, yw, zw + 1)) == CubeTypes.air:
                            add_face(4, position)
                        if self.world.get_block_type_at((xw, yw, zw - 1)) == CubeTypes.air:
                            add_face(5, position)

        if len(self.vertices) == 0:
            self.synced_with_gpu = True
            return
        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_position_vbo)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLfloat * len(self.vertices)),
            (gl.GLfloat * len(self.vertices))(*self.vertices),
            gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.tex_vbo)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLfloat * len(self.tex_coords)),
            (gl.GLfloat * len(self.tex_coords))(*self.tex_coords),
            gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.shading_values_vbo)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLfloat * len(self.shading_values)),
            (gl.GLfloat * len(self.shading_values))(*self.shading_values),
            gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(2, 1, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(2)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLuint * len(self.indices)),
            (gl.GLuint * len(self.indices))(*self.indices),
            gl.GL_STATIC_DRAW)

        self.synced_with_gpu = True

    def set_block(self, local_position, block_type):

        x, y, z = local_position
        self.block_types[x][y][z] = block_type
        self.synced_with_gpu = False

    def is_in_range(self, camera_pos, max_distance):
        dist = math.sqrt(sum([(camera_pos[i] - self.world_coord_pos[i]) ** 2 for i in [0, 2]]))
        return dist <= max_distance

    def generate_chunk(self):
        if self.generated:
            return
        if self.world_coord_pos[1] > 70 or self.world_coord_pos[1] < -70:
            return
        for x in range(Chunk.SIDE_LENGTH):
            for z in range(Chunk.SIDE_LENGTH):
                world_x = self.world_coord_pos[0] + x
                world_z = self.world_coord_pos[2] + z
                y = self.world.get_height_at(world_x, world_z) + 1

                i = 0
                while i <= (y - self.world_coord_pos[1]) and i < Chunk.SIDE_LENGTH:
                    self.block_types[x][i][z] = CubeTypes.dirt
                    if i == int(y - self.world_coord_pos[1]):
                        self.block_types[x][i][z] = CubeTypes.grass
                    i += 1

        self.generated = True
        self.synced_with_gpu = False

    def draw(self):
        if len(self.indices) == 0:
            return
        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(
            gl.GL_TRIANGLES,
            len(self.indices),
            gl.GL_UNSIGNED_INT,
            None)
