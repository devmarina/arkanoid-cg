# Arkanoid

Trabalho final de Computação Gráfica (UFC Russas).

**Equipe:** Beatriz Gomes, Iara Santos, Marina Lima

Jogo estilo Arkanoid feito em Python com OpenGL moderno (3.3 core).

## Como instalar

Python 3.14 e as bibliotecas:

    pip install glfw PyOpenGL PyGLM numpy Pillow

No Linux Mint, se o pip reclamar de "externally-managed-environment":

    pip install --user --break-system-packages glfw PyOpenGL PyGLM numpy Pillow

## Como rodar

Dentro da pasta do projeto:

    python main.py        (Windows)
    python3 main.py       (Linux)

## Controles

| Ação | Tecla / mouse |
|---|---|
| Mover a raquete | setas, A / D ou mover o mouse |
| Soltar a bola / começar | ESPAÇO ou clique |
| Jogar de novo (vitória ou derrota) | R |
| Voltar ao menu / sair | ESC |

## Como se joga

Solte a bola e quebre todos os tijolos. Cada tijolo vale 10 pontos.
São 3 vidas (ícones no canto de cima); se a bola cair, perde uma.
Onde a bola bate na raquete muda o ângulo em que ela sai.

## Onde está cada requisito

Cada requisito está marcado no código com um comentário `# Rxx`
(use a busca do editor, por exemplo `R06`).

| Requisito | Onde |
|---|---|
| R01 primitivas (triângulos) | `gameObject.py` |
| R02 VBO / VAO | `gameObject.py` (`criaVao`) |
| R03 vertex e fragment shader | `shaders/sprite.vert`, `shaders/sprite.frag`, `shader.py` |
| R04 transformações | `gameObject.py` (`getModelMatrix`) |
| R05 projeção ortográfica | `render.py` (`comeca`) |
| R06 duas ou mais texturas | `texture.py`, `recursos.py` (8 imagens da pasta `texturas/`) |
| R07 objeto animado | `jogo.py` (bola), `menu.py`, `particulas.py` |
| R08 tela inicial | `menu.py` |
| R09 teclado e mouse | `entrada.py`, `jogo.py` |
| R10 mais de um tipo de objeto | `jogo.py` (raquete, bola, tijolos), `particulas.py` |
| R11 colisões | `jogo.py` (`sobreposicao`) |
| R12 progresso (pontos e vidas) | `jogo.py`, `hud.py` |
| R13 vitória e derrota | `vitoria.py`, `derrota.py` |
| R14 reiniciar | `jogo.py` (`entra`), teclas R em `derrota.py` e `vitoria.py` |
| R15 código modular | um arquivo para cada parte (lista abaixo) |
| R16 README | este arquivo |
| R17 requisitos identificados no código | comentários `# Rxx` + esta tabela |

**Desafio gráfico adicional:** sistema de partículas quando um tijolo quebra
(`particulas.py`, com transparência controlada no fragment shader) e efeito
de shader na tela de derrota (a cena vai ficando cinza, uniform `cinza` em
`shaders/sprite.frag`).

## Módulos

| Arquivo | O que faz |
|---|---|
| `main.py` | cria a janela e roda o loop principal |
| `estado.py` | guarda qual tela está ativa e troca de tela |
| `render.py` | começa cada frame, câmera, projeção e efeito cinza |
| `entrada.py` | teclado e mouse |
| `recursos.py` | carrega as texturas |
| `gameObject.py` | o objeto desenhável (quadrado com posição, tamanho, cor, textura) |
| `shader.py` | compila os shaders |
| `texture.py` | cria texturas a partir de imagens |
| `texto.py` | transforma texto em textura |
| `cores.py` | paleta de cores |
| `hud.py` | vidas e pontos |
| `menu.py`, `jogo.py`, `derrota.py`, `vitoria.py` | as telas do jogo |
| `particulas.py` | partículas (quebra de tijolo e confete) |

## Créditos dos assets

- Imagens de `texturas/` (tijolos, raquete, bola e estrelinha): pacote
  **Puzzle Game Art** de **Kenney Vleugels** ([Kenney.nl](https://www.kenney.nl),
  www.kenney.nl), publicado em
  https://opengameart.org/content/puzzle-game-art. O autor permite uso em
  projetos pessoais e comerciais e pede o crédito (texto original em
  `texturas/LEIA-ME_kenney.txt`).
- Fonte dos textos: DejaVu Sans Bold (ou Liberation Sans / Arial, a que o
  sistema tiver), carregada pelo Pillow.

