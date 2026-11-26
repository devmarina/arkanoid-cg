import glfw
import glm
from gameObject import GameObject
import recursos
import estado
import entrada
import hud
import particulas

VEL_RAQUETE = 1.5
VEL_BOLA = 1.1
COLUNAS = 8
LINHAS = 5
CORES_LINHAS = [
    (0.9, 0.2, 0.2),
    (0.95, 0.6, 0.15),
    (0.95, 0.9, 0.2),
    (0.3, 0.8, 0.3),
    (0.3, 0.5, 0.95),
]

raquete = None
bola = None
tijolos = []
velBola = glm.vec2(0, 0)
preso = True   # bola grudada na raquete esperando o espaco
vidas = hud.MAX_VIDAS
pontos = 0

# R10: o jogo tem varios tipos de objeto (raquete, bola, tijolos e particulas)
def criaTijolos():
    global tijolos
    tijolos = []
    for j in range(LINHAS):
        for i in range(COLUNAS):
            x = -0.77 + i * 0.22
            y = 0.85 - j * 0.11
            t = GameObject(x, y, 0.2, 0.1, (1, 1, 1))  # branco = mostra a textura sem tingir
            t.texId = recursos.tijolos[j]
            t.corParticula = CORES_LINHAS[j]
            tijolos.append(t)

def init():
    global raquete, bola
    raquete = GameObject(0, -0.9, 0.3, 0.07, (1, 1, 1))
    bola = GameObject(0, 0, 0.04, 0.04, (1, 1, 1))
    raquete.texId = recursos.raquete
    bola.texId = recursos.bola

# chamada pelo estado.vaiPara('jogo'): comeca uma partida do zero (R14)
def entra():
    global vidas, pontos, preso
    vidas = hud.MAX_VIDAS
    pontos = 0
    preso = True
    raquete.pos.x = 0
    criaTijolos()
    particulas.limpa()
    entrada.mouseMexeu = False  # ignora a posicao antiga do mouse
    hud.setPontos(0)
    estado.titulo('arkanoid')

def lanca():
    global preso, velBola
    if preso:
        preso = False
        velBola = glm.normalize(glm.vec2(0.4, 1)) * VEL_BOLA

# R09: teclado (aqui) e mouse (clique) soltam a bola
def tecla(key):
    if key == glfw.KEY_ESCAPE:
        estado.vaiPara('menu')
    elif key == glfw.KEY_SPACE:
        lanca()

def clique():
    lanca()

# R11: colisao entre retangulos (AABB)
def sobreposicao(a, b):
    # quanto os retangulos a e b entram um no outro em x e y (> 0 nos dois = colidiu)
    dx = (a.scale.x + b.scale.x) / 2 - abs(a.pos.x - b.pos.x)
    dy = (a.scale.y + b.scale.y) / 2 - abs(a.pos.y - b.pos.y)
    return dx, dy

def update(dt):
    global preso, velBola, vidas, pontos

    particulas.update(dt)

    # raquete: teclado, e o mouse manda se mexeu
    raquete.pos.x += entrada.direcao() * VEL_RAQUETE * dt
    if entrada.mouseMexeu:
        raquete.pos.x = entrada.mouseX
        entrada.mouseMexeu = False
    meia = raquete.scale.x / 2
    raquete.pos.x = max(-1 + meia, min(1 - meia, raquete.pos.x))

    # bola grudada na raquete (o espaco que solta ela esta na funcao tecla)
    if preso:
        bola.pos.x = raquete.pos.x
        bola.pos.y = raquete.pos.y + raquete.scale.y / 2 + bola.scale.y / 2
        return

    # R07: move a bola (velocidade * dt)
    bola.pos.x += velBola.x * dt
    bola.pos.y += velBola.y * dt

    # paredes e teto
    r = bola.scale.x / 2
    if bola.pos.x - r < -1:
        bola.pos.x = -1 + r
        velBola.x = abs(velBola.x)
    if bola.pos.x + r > 1:
        bola.pos.x = 1 - r
        velBola.x = -abs(velBola.x)
    if bola.pos.y + r > 1:
        bola.pos.y = 1 - r
        velBola.y = -abs(velBola.y)

    # caiu embaixo: perde vida (R12) e, sem vidas, derrota (R13)
    if bola.pos.y + r < -1:
        vidas -= 1
        preso = True
        if vidas <= 0:
            estado.vaiPara('derrota')
        return

    # raquete
    dx, dy = sobreposicao(bola, raquete)
    if dx > 0 and dy > 0 and velBola.y < 0:
        # quanto mais longe do centro, mais inclinada sai a bola
        desvio = (bola.pos.x - raquete.pos.x) / (raquete.scale.x / 2)
        velBola = glm.normalize(glm.vec2(desvio, 1)) * VEL_BOLA
        bola.pos.y = raquete.pos.y + raquete.scale.y / 2 + r

    # tijolos (um por frame)
    for t in tijolos:
        dx, dy = sobreposicao(bola, t)
        if dx > 0 and dy > 0:
            if dx < dy:  # bateu de lado
                if bola.pos.x < t.pos.x:
                    velBola.x = -abs(velBola.x)
                else:
                    velBola.x = abs(velBola.x)
            else:        # bateu em cima ou embaixo
                if bola.pos.y < t.pos.y:
                    velBola.y = -abs(velBola.y)
                else:
                    velBola.y = abs(velBola.y)
            particulas.explode(t.pos.x, t.pos.y, t.corParticula)
            tijolos.remove(t)
            pontos += 10
            hud.setPontos(pontos)
            break

    # acabaram os tijolos: vitoria (R13)
    if len(tijolos) == 0:
        estado.vaiPara('vitoria')

def render(programa):
    for t in tijolos:
        t.draw(programa)
    raquete.draw(programa)
    bola.draw(programa)
    particulas.render(programa)
    hud.render(programa, vidas)
