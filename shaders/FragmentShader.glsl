#version 330 // specify we are indeed using modern opengl

out vec4 fragment_colour; // output of our shader

uniform sampler2DArray texture_array_sampler;

in vec3 local_position;  // interpolated vertex position
in vec3 interpolated_tex_coords;

void main(void) {
	fragment_colour = texture(texture_array_sampler, interpolated_tex_coords); // set the output colour based on the vertex position
}