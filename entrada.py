import glfw
import estado

# posicao do mouse ja convertida para o mundo do jogo (-1 a 1)
mouseX = 0
mouseMexeu = False

# R09: entrada por teclado e mouse
def init(janela):
    glfw.set_key_callback(janela, tecla)
    glfw.set_cursor_pos_callback(janela, mouse)
    glfw.set_mouse_button_callback(janela, clique)

# o glfw chama essa funcao quando uma tecla e apertada
# quem decide o que fazer e a tela atual
def tecla(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return
    estado.telas[estado.tela].tecla(key)

# o glfw chama quando o mouse anda: xpos vai de 0 ate a largura da janela
def mouse(window, xpos, ypos):
    global mouseX, mouseMexeu
    largura = glfw.get_window_size(window)[0]
    mouseX = xpos / largura * 2 - 1
    mouseMexeu = True

# clique do mouse: so as telas que tem a funcao clique() respondem
def clique(window, botao, acao, mods):
    if botao == glfw.MOUSE_BUTTON_LEFT and acao == glfw.PRESS:
        modulo = estado.telas[estado.tela]
        if hasattr(modulo, 'clique'):
            modulo.clique()

# -1 esquerda, 0 parado, 1 direita
def direcao():
    j = estado.janela
    d = 0
    if glfw.get_key(j, glfw.KEY_LEFT) == glfw.PRESS or glfw.get_key(j, glfw.KEY_A) == glfw.PRESS:
        d -= 1
    if glfw.get_key(j, glfw.KEY_RIGHT) == glfw.PRESS or glfw.get_key(j, glfw.KEY_D) == glfw.PRESS:
        d += 1
    return d
