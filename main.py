import glfw
import estado
import render
import recursos
import entrada
import hud
import menu
import jogo
import derrota
import vitoria

#R15: codigo  dividido em modulos. este arquivo so cria a janela e roda o loop
def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, False)

    estado.janela = glfw.create_window(700, 700, 'arkanoid', None, None)
    glfw.make_context_current(estado.janela)
    glfw.swap_interval(1)
    glfw.set_framebuffer_size_callback(estado.janela, render.resize)
    render.resize(estado.janela, *glfw.get_framebuffer_size(estado.janela))
    entrada.init(estado.janela)

    # a ordem importa: render e recursos primeiro, porque os outros usam
    render.init()
    recursos.init()
    hud.init()
    menu.init()
    jogo.init()
    derrota.init()
    vitoria.init()

    estado.telas = {'menu': menu, 'jogo': jogo, 'derrota': derrota, 'vitoria': vitoria}
    estado.vaiPara('menu')

    ultimo = glfw.get_time()
    while not glfw.window_should_close(estado.janela):
        agora = glfw.get_time()
        dt = min(agora - ultimo, 0.05)  # evita a bola atravessar coisas se a janela travar
        ultimo = agora

        glfw.poll_events()
        estado.telas[estado.tela].update(dt)

        render.comeca()
        estado.telas[estado.tela].render(render.programa)
        glfw.swap_buffers(estado.janela)

    glfw.terminate()

if __name__ == "__main__":
    main()
