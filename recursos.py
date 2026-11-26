from texture import Texture

# texturas usadas por varios arquivos
branca = None   # 1x1 branca: objeto aparece so com a cor
tijolos = []    # uma textura de tijolo para cada linha
raquete = None
bola = None
estrela = None

# R06: varias texturas diferentes, carregadas de arquivo (imagens do Kenney.nl)
def init():
    global branca, raquete, bola, estrela
    branca = Texture().texId
    for nome in ['red', 'yellow', 'green', 'blue', 'purple']:
        tijolos.append(Texture(f'texturas/element_{nome}_rectangle.png', suave=True).texId)
    raquete = Texture('texturas/paddleBlu.png', suave=True).texId
    bola = Texture('texturas/ballBlue.png', suave=True).texId
    estrela = Texture('texturas/particleCartoonStar.png', suave=True).texId
