#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;


out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

vec3 FloatRounding(vec3 pos, int digits){
    vec3 outpos = vec3(0, 0, 0);

    outpos.x = float(int(pos.x * digits)) * float(digits);
    outpos.y = float(int(pos.y * digits)) * float(digits);
    outpos.z = float(int(pos.z * digits)) * float(digits);

    return outpos;
}

vec4 snap(vec4 vertex, vec2 resolution)
{
    vec4 snappedPos = vertex;
    snappedPos.xyz = vertex.xyz / vertex.w; // convert to normalised device coordinates (NDC)
    snappedPos.xy = floor(resolution * snappedPos.xy) / resolution; // snap the vertex to the lower-resolution grid
    snappedPos.xyz *= vertex.w; // convert back to projection-space
    return snappedPos;
}

vec4 roundToDecimal(vec4 v, int decimalPlaces) {
    float factor = pow(10.0, float(decimalPlaces));
    return round(v * factor) / factor;
}

void main(){
    uv_0 = in_texcoord_0;
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
    fragPos = vec3(m_model * vec4(in_position, 1.0));
    
    float largeValue = 1e20;
    float smallValue = 1e-5;
    float p_Issue = (largeValue + smallValue) - largeValue;

    vec4 pos = m_proj * m_view * m_model * vec4(in_position, 1.0);
    // vec3 new_pos = vec3(pox.x/pos.w, pos.y/pos.w, pos.z/pos.w)
    // gl_Position = vec4(pos.x * p_Issue, pos.y * p_Issue, pos.z * p_Issue, pos.w);
    gl_Position = snap(pos, vec2(320/2, 200/2));
}