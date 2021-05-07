

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

    def __init__(self, texture, faces=['right', 'left', 'top', 'bottom', 'front', 'back']):

        self.texture_coords = Cube.TEXTURE_COORDS.copy()

        for face in faces:
            if face in Cube.ALL_FACES:
                face_idx = Cube.ALL_FACES.index(face)

    @staticmethod
    def get_face_info(face_type):
        idx = Cube.ALL_FACES.index(face_type)
        return Cube.VERTICES[idx].copy(), Cube.INDICES[idx].copy(), Cube.TEXTURE_COORDS[idx].copy(), Cube.SHADING_VALS[idx].copy()





