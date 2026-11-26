from PIL import Image
from OpenGL.GL import *

# R06: carrega uma imagem (Pillow) e cria a textura no OpenGL
class Texture:
    # sem arquivo e sem img = textura branca 1x1, o objeto aparece so com a cor (color)
    # img = imagem PIL ja pronta (usada para os textos)
    # suave = True usa GL_LINEAR (bom para texto), False usa GL_NEAREST (pixel art)
    def __init__(self, fileName=None, img=None, suave=False):
        if img is None:
            if fileName is None:
                img = Image.new("RGBA", (1, 1), (255, 255, 255, 255))
            else:
                img = Image.open(fileName)
        img = img.transpose(Image.FLIP_TOP_BOTTOM) #inverte a imagem verticalmente
        imgData = img.convert("RGBA").tobytes() #converter a imagem para um vetor de bytes

        filtro = GL_LINEAR if suave else GL_NEAREST

        self.texId = glGenTextures(1) #criar textura
        glBindTexture(GL_TEXTURE_2D, self.texId) # tornei ela ativa
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filtro)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filtro)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                     img.width, img.height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, imgData)
        glBindTexture(GL_TEXTURE_2D, 0)
