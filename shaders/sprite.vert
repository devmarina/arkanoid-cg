//vertex shader
// R03: vertex shader, posicao final = projecao * view * model * vertice (R04, R05)
#version 330 core

uniform mat4 projMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;

// R02: atributos que vem do VBO (0 = posicao, 1 = uv)
layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec2 a_uv;

out vec2 uv;

void main(){
    uv = a_uv;
    gl_Position = projMatrix * viewMatrix * modelMatrix * vec4(a_pos, 1);
}
