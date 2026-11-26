import glfw
from OpenGL.GL import *
import cores
import estado
import jogo
import render as renderer
from texto import criaTexto, sombraDe

tempo = 0
titulo = None
sombraTitulo = None
pontosTexto = None
recomecar = None
voltar = None

def init():
    global titulo, sombraTitulo, recomecar, voltar
    titulo = criaTexto("GAME OVER", 0.2, 0, 0.2, cores.ROXO_CLARO)
    sombraTitulo = sombraDe(titulo, 0.01, -0.01, cores.ROXO_ESCURO)
    recomecar = criaTexto("R para jogar de novo", 0.065, 0, -0.2, cores.ROXO)
    voltar = criaTexto("ESC para voltar ao menu", 0.055, 0, -0.3, cores.ROXO)

# chamada pelo estado.vaiPara('derrota')
def entra():
    global tempo, pontosTexto
    tempo = 0
    if pontosTexto is not None:
        glDeleteTextures([pontosTexto.texId])  # apaga o texto da partida anterior
    pontosTexto = criaTexto(f"pontos: {jogo.pontos}", 0.08, 0, -0.02, cores.ROXO_CLARO)

def tecla(key):
    if key == glfw.KEY_R:  # R14: reiniciar
        estado.vaiPara('jogo')
    elif key == glfw.KEY_ESCAPE:
        estado.vaiPara('menu')

def update(dt):
    global tempo
    tempo += dt

# R13: tela de derrota; o efeito de shader (cinza) e o desafio grafico extra
def render(programa):
    # a cena do jogo fica parada e vai perdendo a cor (efeito no fragment shader)
    renderer.cinza(min(tempo / 1.2, 1))
    jogo.render(programa)

    # textos sem o efeito, aparecem um depois do outro
    renderer.cinza(0)
    if tempo > 0.6:
        sombraTitulo.draw(programa)
        titulo.draw(programa)
        pontosTexto.draw(programa)
    if tempo > 1.2:
        recomecar.draw(programa)
        voltar.draw(programa)
