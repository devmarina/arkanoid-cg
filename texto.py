from PIL import Image, ImageDraw, ImageFont
from gameObject import GameObject
from texture import Texture

# OpenGL n desenha texto sozinho ent o texto vira uma imagem  e depois uma textura num quadrado igual aos outros objetos
NOMES_FONTE = ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf"]

fontes = {}

def pegaFonte(px):
    if px not in fontes:
        fonte = None
        for nome in NOMES_FONTE:
            try:
                fonte = ImageFont.truetype(nome, px)
                break
            except OSError:
                pass
        if fonte is None:
            fonte = ImageFont.load_default(px)
        fontes[px] = fonte
    return fontes[px]

#tam = altura da letra em unidades do mundo 
def criaTexto(texto, tam, x, y, cor=(1, 1, 1), larguraMax=1.9):
    px = max(12, int(tam * 700)) 
    fonte = pegaFonte(px)
    asc, desc = fonte.getmetrics()
    pad = 6

    larg = int(fonte.getlength(texto)) + 2 * pad
    alt = asc + desc + 2 * pad
    img = Image.new("RGBA", (larg, alt), (255, 255, 255, 0))
    ImageDraw.Draw(img).text((pad, pad + asc), texto, font=fonte, fill=(255, 255, 255, 255), anchor="ls")

    escala = tam / px
    w = larg * escala
    h = alt * escala
    if w > larguraMax:  
        h = h * larguraMax / w
        w = larguraMax

    obj = GameObject(x, y, w, h, cor)
    obj.texId = Texture(img=img, suave=True).texId
    return obj
def sombraDe(obj, dx, dy, cor):
    s = GameObject(obj.pos.x + dx, obj.pos.y + dy, obj.scale.x, obj.scale.y, cor)
    s.texId = obj.texId
    return s
