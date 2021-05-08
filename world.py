import math
from cube import CubeTypes
from chunk import Chunk


# This class holds the multiple chunk meshes that make up the world.
# Only chunks that are close to the viewer will be rendered.
class World:
    def __init__(self, cube_types):
        self.cube_types = cube_types
        self.chunks = {}

        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    self.chunks[(x, y, z)] = Chunk((x * 16, y * 16, z * 16), self.cube_types, self)

        self.set_block_type_at((0, 0, 0), CubeTypes.cobble)

    def get_block_type_at(self, pos):
        chunk = self.chunks[self.block_coord_to_chunk_pos(pos)]
        if chunk is not None:
            local_pos = (int(math.floor(pos[0] % chunk.Chunk.SIDE_LENGTH)),
                         int(math.floor(pos[1] % chunk.Chunk.SIDE_LENGTH)),
                         int(math.floor(pos[1] % chunk.Chunk.SIDE_LENGTH)))
            return chunk.block_types[local_pos[0]][local_pos[1]][local_pos[2]]
        return CubeTypes.air

    def set_block_type_at(self, pos, block_type):
        chunk = self.chunks[self.block_coord_to_chunk_pos(pos)]
        if chunk is not None:
            local_pos = (int(math.floor(pos[0] % Chunk.SIDE_LENGTH)),
                         int(math.floor(pos[1] % Chunk.SIDE_LENGTH)),
                         int(math.floor(pos[1] % Chunk.SIDE_LENGTH)))
            chunk.set_block(local_pos, block_type)

    @staticmethod
    def block_coord_to_chunk_pos(block_coord):
        chunk_coord = (int(math.floor(block_coord[0] / Chunk.SIDE_LENGTH)),
                       int(math.floor(block_coord[1] / Chunk.SIDE_LENGTH)),
                       int(math.floor(block_coord[2] / Chunk.SIDE_LENGTH)))
        return chunk_coord

    def draw(self):
        for chunk in self.chunks:
            if not chunk.synced_with_gpu:
                chunk.synced_with_gpu()
            chunk.draw()
