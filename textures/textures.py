import pyglet
import pyglet.gl as gl


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


