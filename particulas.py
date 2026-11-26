import random
import glm
from gameObject import GameObject
import recursos

# R07 (desafio extra): sistema de particulas
# cada particula e uma lista [objeto, velocidade, vida que resta, vida total]
lista = []
GRAVIDADE = -1.2
TAM = 0.04

# solta pedacinhos do tijolo que acabou de quebrar
def explode(x, y, cor, qtd=14):
    for _ in range(qtd):
        p = GameObject(x + random.uniform(-0.1, 0.1), y, TAM, TAM, cor)
        p.texId = recursos.estrela
        vel = glm.vec2(random.uniform(-0.5, 0.5), random.uniform(0.1, 0.8))
        vida = random.uniform(0.4, 0.9)
        lista.append([p, vel, vida, vida])

# papel picado caindo do alto (tela de vitoria)
def confete(cor):
    p = GameObject(random.uniform(-1, 1), 1.05, TAM, TAM, cor)
    p.texId = recursos.estrela
    vel = glm.vec2(random.uniform(-0.2, 0.2), random.uniform(-0.7, -0.3))
    vida = random.uniform(1.5, 2.5)
    lista.append([p, vel, vida, vida])

def limpa():
    lista.clear()

def update(dt):
    for item in list(lista):  # copia da lista, porque vamos remover itens dentro do for
        p, vel, vida, total = item

        vel.y += GRAVIDADE * dt
        p.pos.x += vel.x * dt
        p.pos.y += vel.y * dt

        item[2] -= dt
        if item[2] <= 0:
            lista.remove(item)
        else:
            p.alfa = item[2] / total  # vai sumindo conforme a vida acaba

def render(programa):
    for item in lista:
        item[0].draw(programa)
