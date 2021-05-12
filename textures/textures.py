import pyglet
import pyglet.gl as gl
import numpy as np
import math
from perlin_noise import PerlinNoise

# Textures primarily used for blocks
class TextureDict:
    def __init__(self, height, width):
        self.height, self.width = height, width

        self.textures = []
        self.texture_array = gl.GLuint(0)
        gl.glGenTextures(1, self.texture_array)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.texture_array)

        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        gl.glTexImage3D(
            gl.GL_TEXTURE_2D_ARRAY, 0, gl.GL_RGBA,
            self.width, self.height, 256,
            0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, None)

    def generate_mipmaps(self):
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D_ARRAY)

    def add_texture(self, texture_name):
        if texture_name not in self.textures:
            self.textures.append(texture_name)

            texture_image = pyglet.image.load(f"textures/{texture_name}.png").get_image_data()

            def create(X, Y):
                #img = (np.random.random((3, X, Y)) * 255).astype('uint8')

                img = np.zeros((X, Y, 3))
                if texture_name == 'grass' or texture_name == 'grass_side' or texture_name == 'dirt':
                    for x in range(X):
                        for y in range(Y):
                            intensity = PerlinNoise(octaves=15, seed=1)
                            a = ((intensity([x / X, y / Y]) + 1) / 0.5) * 0.25 + 0.35
                            img[x][y][1] = 137 * a
                            img[x][y][0] = 97 * a
                            img[x][y][2] = 61 * a
                            if texture_name == 'grass_side' or texture_name == 'dirt':
                                intensity = PerlinNoise(seed=2)
                                a = ((intensity([x / X, y / Y]) + 1) / 0.5) * 0.25 + 0.35
                                if x < 1.5 * math.sin(y) + 10 or texture_name == 'dirt':
                                    img[x][y][0] = 153 * a
                                    img[x][y][1] = 117 * a
                                    img[x][y][2] = 81 * a
                return img.astype('uint8')

            def img(x, y):
                data = np.array(create(x, y))
                data = (gl.GLubyte * data.size).from_buffer(data)
                return pyglet.image.ImageData(x, y, 'RGB', data)
            texture_image = img(self.height, self.width)

            #if texture_name == 'grass_side':
             #   texture_image = pyglet.image.load(f"textures/{texture_name}.png").get_image_data()

            gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.texture_array)

            gl.glTexSubImage3D(
                gl.GL_TEXTURE_2D_ARRAY, 0,
                0, 0, len(self.textures) - 1,
                self.width, self.height, 1,
                gl.GL_RGBA, gl.GL_UNSIGNED_BYTE,
                texture_image.get_data("RGBA", texture_image.width * 4))


    def get(self, texture_name):
        self.add_texture(texture_name)
        return self.textures.index(texture_name) if texture_name in self.textures else None