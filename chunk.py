import ctypes
import math
import cube
import pyglet.gl as gl
import enum


class BlockTypes(enum.Enum):
    air = 0
    dirt = 1
    grass = 2
    cobble = 3
    wood = 4


# Represents a single mesh of the exposed faces of a chunk of cubes.
class Chunk:
    SIDE_LENGTH = 16

    def __init__(self, chunk_coord_pos, textures, world):
        # Set position variables
        self.chunk_coord_pos = chunk_coord_pos
        self.world_coord_pos = (
            self.chunk_coord_pos[0] * Chunk.SIDE_LENGTH, self.chunk_coord_pos[1] * Chunk.SIDE_LENGTH,
            self.chunk_coord_pos[2] * Chunk.SIDE_LENGTH)

        # Abstractly store each block in the chunk
        self.block_types = [[[BlockTypes.air for _ in range(Chunk.SIDE_LENGTH)] for _ in range(Chunk.SIDE_LENGTH)] for _
                            in
                            range(Chunk.SIDE_LENGTH)]

        self.textures = textures
        self.world = world

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
            positions, _, texture_coords, shading_vals = cube.Cube.get_face_info(face_type)
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
                    if block_type != BlockTypes.air:
                        position = (self.world_coord_pos[0] + x,
                                    self.world_coord_pos[1] + y,
                                    self.world_coord_pos[0] + z)

                        if self.world.get_block_type_at((x + 1, y, z)) != BlockTypes.air:
                            add_face(0, position)
                        if self.world.get_block_type_at((x - 1, y, z)) != BlockTypes.air:
                            add_face(1, position)
                        if self.world.get_block_type_at((x, y + 1, z)) != BlockTypes.air:
                            add_face(2, position)
                        if self.world.get_block_type_at((x, y - 1, z)) != BlockTypes.air:
                            add_face(3, position)
                        if self.world.get_block_type_at((x, y, z + 1)) != BlockTypes.air:
                            add_face(4, position)
                        if self.world.get_block_type_at((x, y, z - 1)) != BlockTypes.air:
                            add_face(5, position)

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

    def draw(self):
        gl.glBindVertexArray(self.vao)

        gl.glDrawElements(
            gl.GL_TRIANGLES,
            len(self.mesh_indices),
            gl.GL_UNSIGNED_INT,
            None)
