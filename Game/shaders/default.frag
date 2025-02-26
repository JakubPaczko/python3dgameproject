#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light{
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;

vec4 Posterize(in vec4 inputColor){
    float gamma = 0.3f;
    float numColors = 5.0f;
  

    vec3 c = inputColor.rgb;
    c = pow(c, vec3(gamma, gamma, gamma));
    c = c * numColors;
    c = floor(c);
    c = c / numColors;
    c = pow(c, vec3(1.0/gamma));
  
    return vec4(c, inputColor.a);
}

vec4 cellShade(in vec4 inputColor){
    float gamma = 0.3f;
    int numColors = 3;
    int x = 255 / numColors;

    vec3 c = vec3(
        int(inputColor.x * 255) - (int(inputColor.x * 255) % x),
        int(inputColor.y * 255) - (int(inputColor.x * 255) % x),
        int(inputColor.z * 255) - (int(inputColor.x * 255) % x)
        );
  
    return vec4(c / 255, inputColor.a);
}

vec3 getLight(vec3 color){
    vec3 Normal = normalize(normal);
    vec3 ambient = light.Ia;

    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.Is;
    
    return color * (ambient + diffuse+ specular);
}

void main(){
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = cellShade(vec4(color, 1.0)).xyz;
    color = getLight(color);
    // color = getLight(cellShade( vec4(color, 1.0) ).rgb );
    // fragColor = Posterize(vec4(color, 0.5));
    fragColor = vec4(color, 1.0);
} 