import glfw
import glm
from OpenGL.GL import *
from gameObject import GameObject
from shader import criaPrograma

VEL_RAQUETE = 1.5
VEL_BOLA = 1.1

COR_FUNDO = (0.04, 0.05, 0.13)
COR_DERROTA = (0.25, 0.05, 0.07)
COR_VITORIA = (0.05, 0.22, 0.10)

programa = None
raquete = None
bola = None
tijolos = []
velBola = glm.vec2(0, 0)
preso = True  # bola grudada na raquete esperando o espaco
vidas = 3
pontos = 0
estado = 'jogando'# 'jogando', 'derrota' ou 'vitoria'

def resize(window, w, h):
    glViewport(0, 0, w, h)

def criaTijolos():
    global tijolos
    tijolos = []
    # 5 linhas de 8 tijolos, uma cor para cada linha
    cores = [
        (0.9, 0.2, 0.2),
        (0.95, 0.6, 0.15),
        (0.95, 0.9, 0.2),
        (0.3, 0.8, 0.3),
        (0.3, 0.5, 0.95),
    ]
    for j in range(5):
        for i in range(8):
            x = -0.77 + i * 0.22
            y = 0.85 - j * 0.1
            tijolos.append(GameObject(x, y, 0.2, 0.08, cores[j]))

def init():
    global programa, raquete, bola
    glClearColor(*COR_FUNDO, 1)

    programa = criaPrograma('shaders/basico.vert', 'shaders/basico.frag')

    raquete = GameObject(0, -0.9, 0.3, 0.05, (0.65, 0.48, 0.95))
    bola = GameObject(0, -0.855, 0.04, 0.04, (1, 1, 1))
    criaTijolos()

def atualizaTitulo(window):
    if estado == 'jogando':
        titulo = f'arkanoid - cg   vidas: {vidas}  pontos: {pontos}'
    elif estado == 'derrota':
        titulo = f'GAME OVER!    pontos: {pontos}    aperte R para jogar de novo'
    else:
        titulo = f'VOCE GANHOU!    pontos: {pontos}    aperte R para jogar de novo'
    glfw.set_window_title(window, titulo)

def reiniciar(window):
    global vidas, pontos, preso, estado
    vidas = 3
    pontos = 0
    preso = True
    estado = 'jogando'
    raquete.pos.x = 0
    criaTijolos()
    glClearColor(*COR_FUNDO, 1)
    atualizaTitulo(window)

def sobreposicao(a, b):
    # quanto os retangulos a e b entram um no outro em x e y (> 0 nos dois = colidiu)
    dx = (a.scale.x + b.scale.x) / 2 - abs(a.pos.x - b.pos.x)
    dy = (a.scale.y + b.scale.y) / 2 - abs(a.pos.y - b.pos.y)
    return dx, dy

def update(window, dt):
    global preso, velBola, vidas, pontos, estado

    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if estado != 'jogando':
        if glfw.get_key(window, glfw.KEY_R) == glfw.PRESS: 
            reiniciar(window) # fim de jogo: so espera o R
        return

    # raquete
    direcao = 0
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS or glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        direcao -= 1
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS or glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        direcao += 1
    raquete.pos.x += direcao * VEL_RAQUETE * dt
    meia = raquete.scale.x / 2
    raquete.pos.x = max(-1 + meia, min(1 - meia, raquete.pos.x))

    # bola grudada na raquete, acompanha ate apertar espaco
    if preso:
        bola.pos.x = raquete.pos.x
        bola.pos.y = raquete.pos.y + raquete.scale.y / 2 + bola.scale.y / 2
        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            preso = False
            velBola = glm.normalize(glm.vec2(0.4, 1)) * VEL_BOLA
        return
    
    bola.pos.x += velBola.x * dt     #p mover a bola
    bola.pos.y += velBola.y * dt

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

    if bola.pos.y + r < -1:
        vidas -= 1 #se cai embaixo perde 1 vida
        preso = True
        if vidas <= 0:
            estado = 'derrota'
            glClearColor(*COR_DERROTA, 1)
        atualizaTitulo(window)
        return

    dx, dy = sobreposicao(bola, raquete) #raquete
    if dx > 0 and dy > 0 and velBola.y < 0:
        desvio = (bola.pos.x - raquete.pos.x) / (raquete.scale.x / 2) #mais oonge do centro -> bola mais inclinada
        velBola = glm.normalize(glm.vec2(desvio, 1)) * VEL_BOLA
        bola.pos.y = raquete.pos.y + raquete.scale.y / 2 + r

    for t in tijolos:
        dx, dy = sobreposicao(bola, t)
        if dx > 0 and dy > 0:
            if dx < dy: #bateu de lado
                if bola.pos.x < t.pos.x:
                    velBola.x = -abs(velBola.x)
                else:
                    velBola.x = abs(velBola.x)
            else: #bateu em cima ou embaixo
                if bola.pos.y < t.pos.y:
                    velBola.y = -abs(velBola.y)
                else:
                    velBola.y = abs(velBola.y)
            tijolos.remove(t)
            pontos += 10
            atualizaTitulo(window)
            break

    if len(tijolos) == 0:
        estado = 'vitoria'  #acabaram os tijolos: ganhou
        glClearColor(*COR_VITORIA, 1)
        atualizaTitulo(window)

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(programa)

    P = glm.ortho(-1, 1, -1, 1, 0.1, 10)
    V = glm.lookAt(glm.vec3(0, 0, 1), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    glUniformMatrix4fv(glGetUniformLocation(programa, "projMatrix"), 1, GL_FALSE, glm.value_ptr(P))
    glUniformMatrix4fv(glGetUniformLocation(programa, "viewMatrix"), 1, GL_FALSE, glm.value_ptr(V))

    for t in tijolos:
        t.draw(programa)
    raquete.draw(programa)
    bola.draw(programa)

def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, False)

    window = glfw.create_window(700, 700, 'arkanoid - etapa 2', None, None)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    glfw.set_framebuffer_size_callback(window, resize)
    resize(window, *glfw.get_framebuffer_size(window))

    init()
    atualizaTitulo(window)

    ultimo = glfw.get_time()
    while not glfw.window_should_close(window):
        agora = glfw.get_time()
        dt = min(agora - ultimo, 0.05)#se a janela travar, a bola nao pula tijolos
        ultimo = agora

        glfw.poll_events()
        update(window, dt)
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()