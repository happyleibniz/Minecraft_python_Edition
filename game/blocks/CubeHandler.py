from OpenGL.GL import *
import numpy as np
from functions import roundPos, cube_vertices, adjacent
from game.blocks.Cube import Cube


class CubeHandler:
    top_color = ('c3f', (1.0,) * 12)
    ns_color = ('c3f', (0.8,) * 12)
    ew_color = ('c3f', (0.6,) * 12)
    bottom_color = ('c3f', (0.5,) * 12)

    def __init__(self, batch, block, opaque, alpha_textures, gl):
        self.batch, self.block, self.alpha_textures, self.opaque = batch, block, alpha_textures, opaque
        self.cubes = {}
        self.transparent = gl.transparent
        self.gl = gl
        self.fluids = {}
        self.collidable = {}
        vertex_shader_source = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

out vec3 Normal;
out vec3 FragPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    FragPos = vec3(model * vec4(aPos, 1.0));
    Normal = mat3(transpose(inverse(model))) * aNormal;  
    gl_Position = projection * view * vec4(FragPos, 1.0);
}
"""
        self.vertex_shader = self.compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
        fragment_shader_source = """
#version 330 core
out vec4 FragColor;

in vec3 Normal;
in vec3 FragPos;

uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform vec3 objectColor;

void main()
{
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * lightColor;
    
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;  
    
    vec3 result = (ambient + diffuse + specular) * objectColor;
    FragColor = vec4(result, 1.0);
}
"""
        self.fragment_shader = self.compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)
        self.shader_program = self.create_shader_program(self.vertex_shader, self.fragment_shader)

        '''self.top_color = ('c3f', (0.1,) * 12)
        self.ns_color = ('c3f', (0.1,) * 12)
        self.ew_color = ('c3f', (0.1,) * 12)
        self.bottom_color = ('c3f', (0.1,) * 12)'''

        self.color = True

    def hitTest(self, p, vec, dist=4):
        m = 8
        x, y, z = p
        dx, dy, dz = vec
        dx /= m
        dy /= m
        dz /= m
        prev = None
        for i in range(dist * m):
            key = roundPos((x, y, z))
            if key in self.cubes and key not in self.fluids:
                return key, prev
            prev = key
            x, y, z = x + dx, y + dy, z + dz
        return None, None
    
    def create_shader_program(self,vertex_shader, fragment_shader):
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)
        if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
            error = glGetProgramInfoLog(program).decode()
            print(f"Program link failed: {error}")
        return program
    
    def compile_shader(self,source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
            error = glGetShaderInfoLog(shader)
            print(f"Shader compile failed: {error}")
        return shader

    def show(self, v, t, i, clrC=None):
        # # After creating the shader program
        # print("Shader Program ID:", self.shader_program)
        #
        # # Before using the shader program
        # if glIsProgram(self.shader_program):
        #     glUseProgram(self.shader_program)
        # else:
        #     print("Error: Shader program is not valid.")
        #
        # # Update vertex attribute pointers and enable them
        # rotation = 0
        # scale = 0
        # for position in list(self.cubes.keys()):
        #     glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, v)
        #     glEnableVertexAttribArray(0)
        #     # Set uniforms (example: transformation matrices)
        #     glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "model"), 1, GL_FALSE, self.get_model_matrix(position=position,rotation=0,scale=0))
        #
        #     # Draw the cube
        #     glDrawArrays(GL_TRIANGLES, 0, len(v) / 3)
        #     model_matrix = self.get_model_matrix(position, rotation, scale)
        #     model_matrix_loc = glGetUniformLocation(self.shader_program, "model")
        #     glUniformMatrix4fv(model_matrix_loc, 1, GL_FALSE, model_matrix)
        if not clrC:
            if self.color:
                if i == "left" or i == "front":
                    clr = self.ns_color
                if i == "right" or i == "back":
                    clr = self.ew_color
                if i == "bottom":
                    clr = self.bottom_color
                if i == "top":
                    clr = self.top_color
        else:
            clr = clrC[i]

        return self.opaque.add(4, GL_QUADS, t, ('v3f', v), ('t2f', (0, 0, 1, 0, 1, 1, 0, 1)), clr)

    def updateCube(self, cube, customColor=None):
        shown = any(cube.shown.values())
        if shown:
            if (cube.name != 'water' and cube.name != 'lava') and cube.p not in self.collidable:
                self.collidable[cube.p] = cube
        else:
            if cube.p in self.collidable:
                del self.collidable[cube.p]
            return

        show = self.show
        v = cube_vertices(cube.p)
        f = 'left', 'right', 'bottom', 'top', 'back', 'front'
        for i in (0, 1, 2, 3, 4, 5):
            if cube.shown[f[i]] and not cube.faces[f[i]]:
                cube.faces[f[i]] = show(v[i], cube.t[i], f[i], clrC=customColor)
            elif customColor:
                if cube.color[f[i]] != customColor[f[i]]:
                    if cube.shown[f[i]]:
                        cube.faces[f[i]].delete()
                        cube.faces[f[i]] = show(v[i], cube.t[i], f[i], clrC=customColor)
                    cube.color[f[i]] = customColor[f[i]]

    def set_adj(self, cube, adj, state):
        x, y, z = cube.p
        X, Y, Z = adj
        d = X - x, Y - y, Z - z
        f = 'left', 'right', 'bottom', 'top', 'back', 'front'
        for i in (0, 1, 2):
            if d[i]:
                j = i + i
                a, b = [f[j + 1], f[j]][::d[i]]
                cube.shown[a] = state
                if not state and cube.faces[a]:
                    cube.faces[a].delete()
                    face = cube.faces[a]
                    cube.faces[a] = None

    def add(self, p, t, now=False):
        if p in self.cubes:
            return
        cube = self.cubes[p] = Cube(t, p, self.block[t],
                                    'alpha' if t in self.alpha_textures else 'blend' if (t == 'water' or t == "lava")
                                    else 'solid')

        for adj in adjacent(*cube.p):
            if adj not in self.cubes:
                self.set_adj(cube, adj, True)
            else:
                a, b = cube.type, self.cubes[adj].type
                if a == b and (a == 'solid' or b == 'blend'):
                    self.set_adj(self.cubes[adj], cube.p, False)
                elif a != 'blend' and b != 'solid':
                    self.set_adj(self.cubes[adj], cube.p, False)
                    self.set_adj(cube, adj, True)
                if now:
                    self.updateCube(self.cubes[adj])

        if now:
            self.updateCube(cube)

    def translate(self,x, y, z):
        return np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])

    def rotate_x(self,angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [1, 0,  0, 0],
            [0, c, -s, 0],
            [0, s,  c, 0],
            [0, 0,  0, 1]
        ])

    def rotate_y(self,angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [ c, 0, s, 0],
            [ 0, 1, 0, 0],
            [-s, 0, c, 0],
            [ 0, 0, 0, 1]
        ])

    def scale(self,sx, sy, sz):
        return np.array([
            [sx,  0,  0, 0],
            [ 0, sy,  0, 0],
            [ 0,  0, sz, 0],
            [ 0,  0,  0, 1]
        ])
    
    def get_model_matrix(self,position, rotation, scale):
        translation_matrix = self.translate(*position)
        rotation_matrix_x = self.rotate_x(rotation[0])
        rotation_matrix_y = self.rotate_y(rotation[1])
        scaling_matrix = self.scale(*scale)
        
        # Combine transformations
        model_matrix = np.dot(translation_matrix, np.dot(rotation_matrix_x, rotation_matrix_y))
        model_matrix = np.dot(model_matrix, scaling_matrix)
        return model_matrix

    def remove(self, p):
        if p not in self.cubes:
            return
        if self.cubes[p].name == "bedrock":
            return
        if p in self.fluids:
            self.fluids.pop(p)
        cube = self.cubes.pop(p)

        for side, face in cube.faces.items():
            if face:
                face.delete()
            cube.shown[side] = False
        self.updateCube(cube)

        for adj in adjacent(*cube.p):
            if adj in self.cubes:
                self.set_adj(self.cubes[adj], cube.p, True)
                self.updateCube(self.cubes[adj])
