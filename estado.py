import glfw

# guarda em qual tela o jogo esta e permite trocar de tela
tela = 'menu'
telas = {}      # nome -> modulo (preenchido no main.py)
janela = None

def vaiPara(nome):
    global tela
    tela = nome
    modulo = telas[nome]
    if hasattr(modulo, 'entra'):
        modulo.entra()  # cada tela prepara o que precisa ao ser aberta

def titulo(texto):
    glfw.set_window_title(janela, texto)
