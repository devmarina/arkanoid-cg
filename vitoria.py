import glfw
import random
from OpenGL.GL import *
import cores
import estado
import jogo
import particulas
from texto import criaTexto, sombraDe

tempo = 0
proximoConfete = 0
titulo = None
sombraTitulo = None
pontosTexto = None
recomecar = None
voltar = None

def init():
    global titulo, sombraTitulo, recomecar, voltar
    titulo = criaTexto("VOCÊ VENCEU!", 0.18, 0, 0.1, cores.ROXO_CLARO)
    sombraTitulo = sombraDe(titulo, 0.01, -0.01, cores.ROXO_ESCURO)
    recomecar = criaTexto("R para jogar de novo", 0.065, 0, -0.35, cores.ROXO)
    voltar = criaTexto("ESC para voltar ao menu", 0.055, 0, -0.45, cores.ROXO)

# chamada pelo estado.vaiPara('vitoria')
def entra():
    global tempo, proximoConfete, pontosTexto
    tempo = 0
    proximoConfete = 0
    if pontosTexto is not None:
        glDeleteTextures([pontosTexto.texId])
    pontosTexto = criaTexto(f"pontos: {jogo.pontos}", 0.08, 0, -0.12, cores.ROXO_CLARO)

def tecla(key):
    if key == glfw.KEY_R:
        estado.vaiPara('jogo')
    elif key == glfw.KEY_ESCAPE:
        estado.vaiPara('menu')

def update(dt):
    global tempo, proximoConfete
    tempo += dt
    particulas.update(dt)

    # chuva de confete: um novo a cada 0.03 s
    proximoConfete -= dt
    while proximoConfete <= 0:
        particulas.confete(random.choice(jogo.CORES_LINHAS))
        proximoConfete += 0.03

def render(programa):
    jogo.render(programa)
    sombraTitulo.draw(programa)
    titulo.draw(programa)
    pontosTexto.draw(programa)
    if tempo > 0.8:
        recomecar.draw(programa)
        voltar.draw(programa)
