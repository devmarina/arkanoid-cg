from OpenGL.GL import *
from gameObject import GameObject
from texto import criaTexto
import cores
import recursos

MAX_VIDAS = 3
icones = []
pontosTexto = None

def init():
    for i in range(MAX_VIDAS):
        icone = GameObject(-0.9 + i * 0.14, 0.95, 0.1, 0.023, (1, 1, 1))
        icone.texId = recursos.raquete
        icones.append(icone)
def setPontos(n):
    global pontosTexto
    if pontosTexto is not None:
        glDeleteTextures([pontosTexto.texId])  # apaga a textura antiga
    pontosTexto = criaTexto(f"pontos: {n}", 0.06, 0, 0.95, cores.ROXO_CLARO)
    pontosTexto.pos.x = 0.95 - pontosTexto.scale.x / 2  # encosta na direita

def render(programa, vidas):
    for i in range(MAX_VIDAS):
        if i < vidas:
            icones[i].color = [1, 1, 1]
        else:
            icones[i].color = [0.25, 0.25, 0.35]  # escurece o icone da vida perdida
        icones[i].draw(programa)
    pontosTexto.draw(programa)
