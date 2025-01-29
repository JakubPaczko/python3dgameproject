#version 450

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;

out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    // Extract camera right and up vectors from the view matrix
    vec3 right = normalize(vec3(m_view[0].x, m_view[1].x, m_view[2].x));  // Camera right (X-axis)
    vec3 up    = normalize(vec3(m_view[0].y, m_view[1].y, m_view[2].y));  // Camera up (Y-axis)

    // Extract scaling from m_model (length of basis vectors)
    vec3 scale = vec3(
        length(m_model[0].xyz),  // Scale X
        length(m_model[1].xyz),  // Scale Y
        length(m_model[2].xyz)   // Scale Z
    );

    // Billboard position: Keep object at its world position but align it to the camera
    vec3 billboard_pos = vec3(m_model[3].xyz); // Extract world position from model matrix

    // Apply scale to vertex positions before using right/up
    vec3 world_position = billboard_pos + (in_position.x * scale.x * right) + (in_position.y * scale.y * up);

    // Transform to clip space
    gl_Position = m_proj * m_view * vec4(world_position, 1.0);

    // Pass through values
    uv_0 = in_texcoord_0;
    normal = normalize(m_model * vec4(in_normal, 0.0)).xyz;
    fragPos = world_position;
}