//fragment shader (usando glsl q roda na gpu)
// R03: define a cor de cada pixel
#version 330 core

uniform sampler2D tex;
uniform vec3 color;
uniform float alfa;   // 1 = opaco, 0 = invisivel (particulas somem aos poucos)
uniform float cinza;  // 0 = normal, 1 = cinza e escuro (tela de derrota)

in vec2 uv;
out vec4 fragColor;

void main(){
    // R06: cor da textura no ponto uv vezes a cor do objeto
    vec4 cor = texture(tex, uv) * vec4(color, 1);

    // desafio extra (efeito de shader): a cena vai ficando cinza na derrota
    float luz = dot(cor.rgb, vec3(0.299, 0.587, 0.114));  
    cor.rgb = mix(cor.rgb, vec3(luz), cinza);              
    cor.rgb = cor.rgb * (1.0 - 0.45 * cinza);   

    // desafio extra (particulas): alfa faz a particula sumir
    cor.a = cor.a * alfa;
    fragColor = cor;
}
