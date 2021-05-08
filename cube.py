from copy import deepcopy
from textures.textures import TextureDict
import enum


class CubeTypes(enum.Enum):
    air = 0
    dirt = 1
    grass = 2
    cobble = 3


class Cube:
    VERTICES = [
        [0.5, 0.5, 0.5, 0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5, 0.5, -0.5],  # right
        [-0.5, 0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5],  # left
        [0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, 0.5],  # top
        [-0.5, -0.5, 0.5, -0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5],  # bottom
        [-0.5, 0.5, 0.5, -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5],  # front
        [0.5, 0.5, -0.5, 0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5],  # back
    ]

    INDICES = [
        [0, 1, 2, 0, 2, 3],  # right
        [4, 5, 6, 4, 6, 7],  # left
        [8, 9, 10, 8, 10, 11],  # top
        [12, 13, 14, 12, 14, 15],  # bottom
        [16, 17, 18, 16, 18, 19],  # front
        [20, 21, 22, 20, 22, 23],  # back
    ]

    TEXTURE_COORDS = [
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0],
    ]

    SHADING_VALS = [
        [0.6, 0.6, 0.6, 0.6],
        [0.6, 0.6, 0.6, 0.6],
        [1.0, 1.0, 1.0, 1.0],
        [0.4, 0.4, 0.4, 0.4],
        [0.8, 0.8, 0.8, 0.8],
        [0.8, 0.8, 0.8, 0.8],
    ]

    ALL_FACES = ['right', 'left', 'top', 'bottom', 'front', 'back']

    def __init__(self, texture_dict, textures=None):
        if textures is None:
            textures = {
                'right': 'cobble',
                'left': 'cobble',
                'top': 'cobble',
                'bottom': 'cobble',
                'front': 'cobble',
                'back': 'cobble',
            }

        self.textures = textures

        self.texture_coords = deepcopy(Cube.TEXTURE_COORDS)

        for face in Cube.ALL_FACES:
            texture = self.textures[face]
            texture_idx = texture_dict.get(texture)
            face_idx = Cube.ALL_FACES.index(face)
            for i in range(4):
                self.texture_coords[face_idx][i * 3 + 2] = texture_idx

    def get_face_info(self, face_type):
        # idx = Cube.ALL_FACES.index(face_type)
        idx = face_type
        return Cube.VERTICES[idx].copy(), Cube.INDICES[idx].copy(), self.texture_coords[idx], Cube.SHADING_VALS[
            idx].copy()
