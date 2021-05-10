#version 330

out vec4 fragment_colour;

uniform sampler2DArray interpolatedTexturesArray;

in vec3 texCoordsFrag;
in float diffuseValueFrag;

void main(void) {
	fragment_colour = diffuseValueFrag * texture(interpolatedTexturesArray, texCoordsFrag);
}