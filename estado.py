import glfw
tela = 'menu'
telas = {}      
janela = None

def vaiPara(nome):
    global tela
    tela = nome
    modulo = telas[nome]
    if hasattr(modulo, 'entra'):
        modulo.entra()  # cada tela prepara o que precisa ao ser aberta

def titulo(texto):
    glfw.set_window_title(janela, texto)
