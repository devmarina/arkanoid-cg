import glfw
import glm
from OpenGL.GL import *
from gameObject import GameObject
from shader import criaPrograma

VEL_RAQUETE = 1.5

programa = None
raquete = None
bola = None
tijolos = []

def resize(window, w, h):
    glViewport(0, 0, w, h)

def init():
    global programa, raquete, bola
    glClearColor(0.04, 0.05, 0.13, 1)

    programa = criaPrograma('shaders/basico.vert', 'shaders/basico.frag')

    raquete = GameObject(0, -0.9, 0.3, 0.05, (0.65, 0.48, 0.95))
    bola = GameObject(0, -0.855, 0.04, 0.04, (1, 1, 1))

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

def update(window, dt):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    direcao = 0
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS or glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        direcao -= 1
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS or glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        direcao += 1

    # velocidade * dt: anda a mesma distancia por segundo em qualquer computador
    raquete.pos.x += direcao * VEL_RAQUETE * dt

    # nao deixa a raquete sair da tela
    meia = raquete.scale.x / 2
    raquete.pos.x = max(-1 + meia, min(1 - meia, raquete.pos.x))

    # por enquanto a bola so acompanha a raquete
    bola.pos.x = raquete.pos.x

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

    window = glfw.create_window(700, 700, 'arkanoid', None, None)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    glfw.set_framebuffer_size_callback(window, resize)
    resize(window, *glfw.get_framebuffer_size(window))

    init()

    ultimo = glfw.get_time()
    while not glfw.window_should_close(window):
        agora = glfw.get_time()
        dt = agora - ultimo
        ultimo = agora

        glfw.poll_events()
        update(window, dt)
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
