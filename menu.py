import glfw
import glm
from gameObject import GameObject
from texto import criaTexto, sombraDe
import cores
import estado
import recursos

TONS_TIJOLO = [
    (1, 1, 1),
    (0.8, 0.7, 1),
    (0.9, 0.85, 1),
    (0.7, 0.6, 0.95),
    (0.85, 0.75, 1),
]

desenhos = []   # tudo que e desenhado fixo, na ordem
pressione = None
bola = None
raquete = None
velBola = glm.vec2(0.6, 0.4)

# R08: tela inicial com titulo, equipe e instrucao
def init():
    global pressione, bola, raquete
    # tijolinhos la em cima
    for j in range(2):
        for i in range(8):
            t = GameObject(-0.77 + i * 0.22, 0.88 - j * 0.11, 0.2, 0.1, TONS_TIJOLO[(i + j) % 5])
            t.texId = recursos.tijolos[4]
            desenhos.append(t)

    desenhos.append(criaTexto("Trabalho de CG", 0.09, 0, 0.6, cores.ROXO_CLARO))

    titulo = criaTexto("ARKANOID", 0.26, 0, 0.3, cores.ROXO)
    desenhos.append(sombraDe(titulo, 0.012, -0.012, cores.ROXO_ESCURO))
    desenhos.append(titulo)

    desenhos.append(criaTexto("Beatriz Gomes", 0.08, 0, -0.02, cores.ROXO_CLARO))
    desenhos.append(criaTexto("Iara Santos", 0.08, 0, -0.14, cores.ROXO_CLARO))
    desenhos.append(criaTexto("Marina Lima", 0.08, 0, -0.26, cores.ROXO_CLARO))

    pressione = criaTexto("ESPAÇO ou clique para começar", 0.065, 0, -0.52, cores.ROXO)

    # bolinha quicando na raquete la embaixo
    raquete = GameObject(0, -0.9, 0.3, 0.07, (1, 1, 1))
    raquete.texId = recursos.raquete
    bola = GameObject(0, -0.8, 0.04, 0.04, (1, 1, 1))
    bola.texId = recursos.bola

# chamada pelo estado.vaiPara('menu')
def entra():
    estado.titulo('arkanoid')

def tecla(key):
    if key == glfw.KEY_SPACE or key == glfw.KEY_ENTER:
        estado.vaiPara('jogo')
    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(estado.janela, True)

def clique():
    estado.vaiPara('jogo')

def update(dt):
    global velBola

    bola.pos.x += velBola.x * dt
    bola.pos.y += velBola.y * dt
    if bola.pos.x > 0.95:
        bola.pos.x = 0.95
        velBola.x = -abs(velBola.x)
    if bola.pos.x < -0.95:
        bola.pos.x = -0.95
        velBola.x = abs(velBola.x)
    if bola.pos.y > -0.74:
        bola.pos.y = -0.74
        velBola.y = -abs(velBola.y)
    if bola.pos.y < -0.83:
        bola.pos.y = -0.83
        velBola.y = abs(velBola.y)

    raquete.pos.x = bola.pos.x

def render(programa):
    for obj in desenhos:
        obj.draw(programa)
    raquete.draw(programa)
    bola.draw(programa)
    if int(glfw.get_time() * 2) % 2 == 0:  # pisca
        pressione.draw(programa)
