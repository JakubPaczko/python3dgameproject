#version 330
    // uniform sampler2D Texture;
    // in vec2 uv;
    out vec4 fragColor;
    uniform sampler2D u_texture_0;
    
    in vec2 uv_0;
    in vec3 fragPos;

    void main() {
        // fragColor = vec4(uv_0, 1.0, 1.0);
        vec3 color = texture(u_texture_0, uv_0).rgb;
        fragColor = vec4(color, 1.0);
    }