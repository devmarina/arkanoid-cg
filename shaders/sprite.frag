//fragment shader (usando glsl q roda na gpu)
#version 330 core

uniform sampler2D tex;
uniform vec3 color;
uniform float alfa;   // 1 = opaco, 0 = invisivel (particulas somem aos poucos)
uniform float cinza;  // 0 = normal, 1 = cinza e escuro (tela de derrota)

in vec2 uv;
out vec4 fragColor;

void main(){
    vec4 cor = texture(tex, uv) * vec4(color, 1);

    float luz = dot(cor.rgb, vec3(0.299, 0.587, 0.114));  // brilho que o olho enxerga
    cor.rgb = mix(cor.rgb, vec3(luz), cinza);              // mistura a cor com o cinza
    cor.rgb = cor.rgb * (1.0 - 0.45 * cinza);              // escurece um pouco

    cor.a = cor.a * alfa;
    fragColor = cor;
}
