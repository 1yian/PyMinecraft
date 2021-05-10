import math
from cube import CubeTypes
from chunk import Chunk
from perlin_noise import PerlinNoise


# This class holds the multiple chunk meshes that make up the world.
# Only chunks that are close to the viewer will be rendered.
class World:
    def __init__(self, cube_types):
        self.cube_types = cube_types
        self.chunks = {}
        noise1 = PerlinNoise(octaves=1.5, seed=1)
        noise2 = PerlinNoise(octaves=3, seed=2)
        noise3 = PerlinNoise(octaves=8, seed=3)
        noise4 = PerlinNoise(octaves=12, seed=4)
        for x in range(-64, 64):
            for z in range(-64, 64):
                noise_val = noise1([x / 128, z / 128])
                noise_val += 0.5 * noise2([x / 128, z / 128])
                noise_val += 0.25 * noise3([x / 128, z / 128])
                noise_val += 0.125 * noise4([x / 128, z / 128])
                self.set_top_block((x, noise_val * 75, z))

    def get_block_type_at(self, pos):
        chunk_coord = self.block_coord_to_chunk_pos(pos)
        if chunk_coord not in self.chunks:
            # print(chunk_coord, pos)
            return CubeTypes.air
        chunk = self.chunks[chunk_coord]
        if chunk is not None:
            local_pos = (int(math.floor(pos[0] % Chunk.SIDE_LENGTH)),
                         int(math.floor(pos[1] % Chunk.SIDE_LENGTH)),
                         int(math.floor(pos[2] % Chunk.SIDE_LENGTH)))
            return chunk.block_types[local_pos[0]][local_pos[1]][local_pos[2]]
        return CubeTypes.air

    def set_block_type_at(self, pos, block_type):
        chunk_coord = self.block_coord_to_chunk_pos(pos)
        if chunk_coord not in self.chunks:
            self.chunks[chunk_coord] = Chunk((chunk_coord[0] * Chunk.SIDE_LENGTH, chunk_coord[1] * Chunk.SIDE_LENGTH,
                                              chunk_coord[2] * Chunk.SIDE_LENGTH), self.cube_types, self)
        chunk = self.chunks[self.block_coord_to_chunk_pos(pos)]
        if chunk is not None:
            local_pos = (int(math.floor(pos[0] % Chunk.SIDE_LENGTH)),
                         int(math.floor(pos[1] % Chunk.SIDE_LENGTH)),
                         int(math.floor(pos[2] % Chunk.SIDE_LENGTH)))
            chunk.set_block(local_pos, block_type)

    def set_top_block(self, pos):
        for i in range(-120, int(pos[1])):
            self.set_block_type_at((pos[0], i, pos[2]), CubeTypes.dirt)

        self.set_block_type_at(pos, CubeTypes.grass)
    @staticmethod
    def block_coord_to_chunk_pos(block_coord):
        chunk_coord = (int(math.floor(block_coord[0] / Chunk.SIDE_LENGTH)),
                       int(math.floor(block_coord[1] / Chunk.SIDE_LENGTH)),
                       int(math.floor(block_coord[2] / Chunk.SIDE_LENGTH)))
        return chunk_coord

    def draw(self, camera_pos):
        for chunk in self.chunks.values():
            if not chunk.synced_with_gpu:
                chunk.pass_to_gpu()
            # if chunk.is_in_range(camera_pos, 1300):
            chunk.draw()
