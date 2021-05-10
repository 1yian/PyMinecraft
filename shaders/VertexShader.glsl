#version 330

layout(location = 0) in vec3 vertPos;
layout(location = 1) in vec3 texCoords;
layout(location = 2) in float diffuseValue; // shading value attribute

out vec3 texCoordsFrag;
out float diffuseValueFrag; // interpolated shading value

uniform mat4 mvpMatrix;

void main(void) {
	texCoordsFrag = texCoords;
	diffuseValueFrag = diffuseValue;
	gl_Position = mvpMatrix * vec4(vertPos, 1.0);
}