import chunk
import math


# This class holds the multiple chunk meshes that make up the world.
# Only chunks that are close to the viewer will be rendered.
class World:
    def __init__(self):
        self.chunks = {}

    def get_block_type_at(self, pos):
        chunk = self.chunks[self.block_coord_to_chunk_pos(pos)]
        if chunk is not None:
            local_pos = (int(math.floor(pos[0] / chunk.Chunk.SIDE_LENGTH)),
                         int(math.floor(pos[1] / chunk.Chunk.SIDE_LENGTH)),
                         int(math.floor(pos[1] / chunk.Chunk.SIDE_LENGTH)))
            return chunk.block_types[local_pos[0]][local_pos[1]][local_pos[2]]
        return chunk.BlockType.air

    @staticmethod
    def block_coord_to_chunk_pos(block_coord):
        chunk_coord = (int(math.floor(block_coord[0] / chunk.Chunk.SIDE_LENGTH)),
                       int(math.floor(block_coord[1] / chunk.Chunk.SIDE_LENGTH)),
                       int(math.floor(block_coord[2] / chunk.Chunk.SIDE_LENGTH)))
        return chunk_coord

    def draw(self):
        for chunk in self.chunks:
            chunk.draw()
