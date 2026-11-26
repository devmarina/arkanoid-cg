# Arkanoid

Trabalho final de Computação Gráfica.

**Equipe:** Beatriz Gomes, Iara Santos, Marina Lima

Jogo estilo Arkanoid feito em Python com OpenGL moderno.

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
(`// Rxx` nos shaders).

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
| R16 README | este arquivo (seção "Recursos gráficos utilizados") |
| R17 requisitos identificados no código | comentários `# Rxx` e `// Rxx` + esta tabela |

**Desafio gráfico adicional:** sistema de partículas quando um tijolo quebra
(`particulas.py`, com transparência controlada no fragment shader) e efeito
de shader na tela de derrota (a cena vai ficando cinza, uniform `cinza` em
`shaders/sprite.frag`).

## Recursos gráficos utilizados

**Primitivas e vértices (R01).** Todo objeto é um quadrado feito de 2
triângulos (`GL_TRIANGLES`), com 4 vértices e 6 índices lógicos. Cada vértice
tem posição (x, y, z) e coordenada de textura (u, v).

**VBO e VAO (R02).** O quadrado é enviado uma vez para a GPU, num VBO
(`GL_STATIC_DRAW`) guardado num VAO, em `gameObject.py` (`criaVao`). O atributo
0 é a posição e o atributo 1 é a coordenada de textura. Todos os objetos
(tijolos, raquete, bola, partículas, textos) usam esse mesmo VAO e só mudam
posição, tamanho, cor e textura.

**Shaders (R03).** O `shaders/sprite.vert` calcula a posição final de cada
vértice (`projMatrix * viewMatrix * modelMatrix * posição`) e repassa a
coordenada de textura. O `shaders/sprite.frag` define a cor de cada pixel:
cor da textura vezes a cor do objeto. Ele também tem os uniforms `alfa`
(transparência, usado nas partículas) e `cinza` (efeito da tela de derrota).
Os shaders são compilados e ligados em `shader.py`.

**Transformações (R04).** A matriz model de cada objeto é translação vezes
escala (`getModelMatrix`). A translação é dinâmica: bola, raquete e
partículas mudam de posição a cada frame. A escala define o tamanho de cada
objeto (tijolo, raquete, bola, texto).

**Coordenadas e projeção (R05).** O mundo do jogo vai de -1 a 1 nos dois eixos,
com a origem no centro da janela e o y para cima. A projeção é ortográfica
(`glm.ortho(-1, 1, -1, 1, 0.1, 10)`) e a câmera é fixa, olhando para a origem
(`glm.lookAt`). A janela é quadrada (700 x 700), então nada fica distorcido.
A posição do mouse é convertida de pixels para esse mundo em `entrada.py`.

**Texturas (R06).** As imagens são carregadas com o Pillow em `texture.py` e
viram texturas 2D RGBA (`GL_LINEAR`, `GL_CLAMP_TO_EDGE`). O jogo usa uma textura
por linha de tijolos, uma para a raquete, uma para a bola e uma para as
partículas. Uma textura branca de 1 pixel serve para objetos de cor lisa. Os
textos também viram textura (o Pillow desenha o texto numa imagem). A mistura
de transparência (`glBlendFunc`) deixa os fundos transparentes.

**Animação (R07).** A cada frame o `main.py` calcula o `dt` (tempo desde o
frame anterior) e as posições são atualizadas com velocidade vezes `dt`, para
a velocidade ser a mesma em qualquer computador. Animados: a bola, a bolinha
do menu, o texto que pisca e as partículas.

**Colisões (R11).** Teste entre retângulos alinhados aos eixos (AABB) em
`jogo.py`: a bola contra as paredes, a raquete e os tijolos. O ângulo de saída
da bola na raquete depende de onde ela bate.

**Desafio gráfico adicional.**
- *Sistema de partículas* (`particulas.py`): ao quebrar um tijolo saem
  estrelinhas que sobem, caem com gravidade e vão ficando transparentes. Na
  vitória, cai confete.
- *Efeito com shader*: na tela de derrota o uniform `cinza` vai de 0 a 1 e o
  fragment shader transforma a cena em tons de cinza, escurecendo.

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
  projetos pessoais e comerciais e agradece o crédito (texto original em
  `texturas/LEIA-ME_kenney.txt`).
- Fonte dos textos: DejaVu Sans Bold (ou Liberation Sans / Arial, a que o
  sistema tiver), carregada pelo Pillow.

