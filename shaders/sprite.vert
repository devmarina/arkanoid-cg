//vertex shader
#version 330 core

uniform mat4 projMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec2 a_uv;

out vec2 uv;

void main(){
    uv = a_uv;
    gl_Position = projMatrix * viewMatrix * modelMatrix * vec4(a_pos, 1);
}
