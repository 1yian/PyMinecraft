import ctypes
from cube import Cube, CubeTypes
import pyglet.gl as gl


# Represents a single mesh of the exposed faces of a chunk of cubes.
class Chunk:
    SIDE_LENGTH = 16

    def __init__(self, chunk_coord_pos, cube_types, world):

        # Set position variables
        self.chunk_coord_pos = chunk_coord_pos
        self.world_coord_pos = (
            self.chunk_coord_pos[0] * Chunk.SIDE_LENGTH, self.chunk_coord_pos[1] * Chunk.SIDE_LENGTH,
            self.chunk_coord_pos[2] * Chunk.SIDE_LENGTH)

        # Abstractly store each block in the chunk
        self.block_types = [[[CubeTypes.air for _ in range(Chunk.SIDE_LENGTH)] for _ in range(Chunk.SIDE_LENGTH)] for _
                            in
                            range(Chunk.SIDE_LENGTH)]

        self.world = world
        self.cube_types = cube_types

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

    def pass_to_gpu(self):
        self.vertices, self.tex_coords, self.shading_values, self.indices = [], [], [], []

        def add_face(face_type, position):
            block_type = self.world.get_block_type_at(position)
            if block_type == CubeTypes.air:
                return

            cube = self.cube_types[block_type]
            positions, _, texture_coords, shading_vals = cube.get_face_info(face_type)
            x, y, z = position
            for i in range(4):
                positions[i * 3] += x
                positions[i * 3 + 1] += y
                positions[i * 3 + 2] += z
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
                                      self.world_coord_pos[0] + z)
                        add_face(0, (xw + 1, yw, zw))
                        add_face(1, (xw - 1, yw, zw))
                        add_face(2, (xw, yw + 1, zw))
                        add_face(3, (xw, yw - 1, zw))
                        add_face(4, (xw, yw, zw + 1))
                        add_face(5, (xw, yw, zw - 1))

        if len(self.vertices) == 0:
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

    def draw(self):
        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(
            gl.GL_TRIANGLES,
            len(self.indices),
            gl.GL_UNSIGNED_INT,
            None)
