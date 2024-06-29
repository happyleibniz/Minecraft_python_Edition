#version 330 core

in vec3 fragNormal;
in vec3 fragPosition;
in vec2 fragTexCoord;

out vec4 color;

uniform sampler2D texture1;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform bool isDisk;

void main()
{
    vec3 norm = normalize(fragNormal);
    vec3 lightDir = normalize(lightPos - fragPosition);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 reflectDir = reflect(-lightDir, norm);
    vec3 viewDir = normalize(viewPos - fragPosition);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);

    vec3 ambient = vec3(0.1);
    vec3 diffuse = diff * vec3(0.5);
    vec3 specular = spec * vec3(1.0);

    vec3 result = ambient + diffuse + specular;

    if(isDisk) {
        vec4 texColor = texture(texture1, fragTexCoord);
        color = vec4(result * texColor.rgb, texColor.a);
    } else {
        color = vec4(result, 1.0);
    }
}
