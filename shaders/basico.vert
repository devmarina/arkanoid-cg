//vertex shader
#version 330 core

uniform mat4 projMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;

layout(location = 0) in vec3 a_pos;

void main(){
    gl_Position = projMatrix * viewMatrix * modelMatrix * vec4(a_pos, 1);
}
