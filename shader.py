from OpenGL.GL import *

def compilaShader(caminho, tipo):
    with open(caminho, encoding="utf-8") as f:
        codigo = f.read()
    shader = glCreateShader(tipo)
    glShaderSource(shader, codigo)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader)) #so p mostrar a linha de erro no glsl
    return shader

# R03: compila o vertex shader e o fragment shader e liga os dois num programa
def criaPrograma(vertPath, fragPath):
    vs = compilaShader(vertPath, GL_VERTEX_SHADER)
    fs = compilaShader(fragPath, GL_FRAGMENT_SHADER)

    programa = glCreateProgram()
    glAttachShader(programa, vs)
    glAttachShader(programa, fs)
    glLinkProgram(programa)
    if not glGetProgramiv(programa, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(programa))

    glDeleteShader(vs)
    glDeleteShader(fs)
    return programa
