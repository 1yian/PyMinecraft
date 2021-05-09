#version 330 // specify we are indeed using modern opengl

layout(location = 0) in vec3 vertex_position; // vertex position attribute
layout(location = 1) in vec3 tex_coords;

out vec3 local_position; // interpolated vertex position
out vec3 interpolated_tex_coords;

uniform mat4 mvpMatrix;

void main(void) {
	local_position = vertex_position;
	interpolated_tex_coords = tex_coords;
	gl_Position = mvpMatrix * vec4(vertex_position, 1.0); // set vertex position
}