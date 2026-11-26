import glm
from OpenGL.GL import *
import cores
from shader import criaPrograma

programa = None

def init():
    global programa
    glClearColor(*cores.COR_FUNDO, 1)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  
    programa = criaPrograma('shaders/sprite.vert', 'shaders/sprite.frag')

def resize(window, w, h):
    glViewport(0, 0, w, h)

#comeca um frame novo: limpa a tela e envia camera e projecao
def comeca():
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(programa)

    # R05: projecao ortografica (o mundo vai de -1 a 1 nos dois eixos)
    P = glm.ortho(-1, 1, -1, 1, 0.1, 10)
    V = glm.lookAt(glm.vec3(0, 0, 1), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    glUniformMatrix4fv(glGetUniformLocation(programa, "projMatrix"), 1, GL_FALSE, glm.value_ptr(P))
    glUniformMatrix4fv(glGetUniformLocation(programa, "viewMatrix"), 1, GL_FALSE, glm.value_ptr(V))
    cinza(0)

# efeito de shader: 0 = cores normais, 1 = tudo cinza e escurecido vale p tudo q for desenhado depois da chamada
def cinza(valor):
    glUniform1f(glGetUniformLocation(programa, "cinza"), valor)
