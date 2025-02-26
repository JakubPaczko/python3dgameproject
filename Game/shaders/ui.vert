#version 330
    // layout (location = 0) in vec2 in_uv_0;
    // in vec2 in_uv;
    in vec2 in_texcoord_0;
    in vec3 in_position;

    out vec2 uv_0;
    out vec3 fragPos;

    uniform mat4 m_proj;
    uniform mat4 m_model;

    // out vec2 uv;
    void main() {
        fragPos = in_position;
        uv_0 = in_texcoord_0;
        // m_proj;
        vec4 pos = m_proj * m_model * vec4(in_position, 0.0);
        gl_Position = pos;
        // gl_Position = vec4(in_vert, 0.0, 2.0);
        // uv = in_uv;
    }