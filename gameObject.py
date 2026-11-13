import ctypes
import numpy as np
import glm
from OpenGL.GL import *

class GameObject:
    vaoId = None  # o quadrado e o mesmo p todos os objetos, entao so cria uma vez

    def __init__(self, x=0, y=0, w=1, h=1, color=(1, 1, 1)):
        self.vertices = [
            [-0.5, -0.5, 0],  # v0
            [0.5, -0.5, 0],   # v1
            [0.5, 0.5, 0],    # v2
            [-0.5, 0.5, 0],   # v3
        ]

        self.faces = [
            [0, 1, 2],
            [0, 2, 3],
        ]

        self.color = list(color)
        self.pos = glm.vec3(x, y, 0)
        self.scale = glm.vec3(w, h, 1)

        if GameObject.vaoId is None:
            self.criaVao()

    def criaVao(self):
        # lista com x y z de cada vertice de cada triangulo
        dados = []
        for f in self.faces:
            for vid in f:
                dados += self.vertices[vid]
        dados = np.array(dados, dtype=np.float32)
        GameObject.qtdVertices = len(self.faces) * 3

        GameObject.vaoId = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        glBindVertexArray(GameObject.vaoId)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, dados.nbytes, dados, GL_STATIC_DRAW)

        # atributo 0 = posicao (3 floats por vertice)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glBindVertexArray(0)

    #pt mais matematica, m= t *s
    def getModelMatrix(self):
        M = glm.translate(glm.mat4(1), self.pos)
        M = glm.scale(M, self.scale)
        return M

    def draw(self, programa):
        M = self.getModelMatrix()
        glUniformMatrix4fv(glGetUniformLocation(programa, "modelMatrix"), 1, GL_FALSE, glm.value_ptr(M))
        glUniform3f(glGetUniformLocation(programa, "color"), *self.color)

        glBindVertexArray(GameObject.vaoId)
        glDrawArrays(GL_TRIANGLES, 0, GameObject.qtdVertices)
