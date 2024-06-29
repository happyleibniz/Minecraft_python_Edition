import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
import math
import ctypes
import pyglet.gl as gl


class Shader_error(Exception):
    def __init__(self, message):
        self.message = message


def create_shader(target, source_path):
    # read shader source

    source_file = open(source_path, "rb")
    source = source_file.read()
    source_file.close()

    source_length = ctypes.c_int(len(source) + 1)
    source_buffer = ctypes.create_string_buffer(source)

    buffer_pointer = ctypes.cast(
        ctypes.pointer(ctypes.pointer(source_buffer)),
        ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))

    # compile shader

    gl.glShaderSource(target, 1, buffer_pointer, ctypes.byref(source_length))
    gl.glCompileShader(target)

    # handle potential errors

    log_length = gl.GLint(0)
    gl.glGetShaderiv(target, gl.GL_INFO_LOG_LENGTH, ctypes.byref(log_length))

    log_buffer = ctypes.create_string_buffer(log_length.value)
    gl.glGetShaderInfoLog(target, log_length, None, log_buffer)

    if log_length.value > 1:
        raise Shader_error(str(log_buffer.value))


class Shader:
    def __init__(self, vert_path, frag_path):
        self.program = gl.glCreateProgram()

        # create vertex shader

        self.vert_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        create_shader(self.vert_shader, vert_path)
        gl.glAttachShader(self.program, self.vert_shader)

        # create fragment shader

        self.frag_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        create_shader(self.frag_shader, frag_path)
        gl.glAttachShader(self.program, self.frag_shader)

        # link program and clean up

        gl.glLinkProgram(self.program)

        gl.glDeleteShader(self.vert_shader)
        gl.glDeleteShader(self.frag_shader)

    def __del__(self):
        gl.glDeleteProgram(self.program)

    def find_uniform(self, name):
        return gl.glGetUniformLocation(self.program, ctypes.create_string_buffer(name))

    def uniform_matrix(self, location, matrix):
        gl.glUniformMatrix4fv(location, 1, gl.GL_FALSE, (gl.GLfloat * 16)(*sum(matrix.data, [])))

    def use(self):
        gl.glUseProgram(self.program)


class Sphere:
    def __init__(self, radius, slices, stacks, disk_radius, disk_thickness):
        self.radius = radius
        self.slices = slices
        self.stacks = stacks
        self.disk_radius = disk_radius
        self.disk_thickness = disk_thickness

        self.batch = pyglet.graphics.Batch()

        # Create vertex list for sphere
        self.create_sphere_vertices()

        # Create vertex list for disk
        self.create_disk_vertices()

        self.program = Shader("vertex_shader.glsl", "fragment_shader.glsl")
        self.shader_sampler_location = self.program.find_uniform(b"texture_array_sampler")
        self.program.use()

    def create_sphere_vertices(self):
        vertices = []
        normals = []
        tex_coords = []
        indices = []

        for stack in range(self.stacks + 1):
            theta = stack * math.pi / self.stacks
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)

            for slice in range(self.slices + 1):
                phi = slice * 2 * math.pi / self.slices
                sin_phi = math.sin(phi)
                cos_phi = math.cos(phi)

                x = cos_phi * sin_theta
                y = cos_theta
                z = sin_phi * sin_theta
                u = 1 - (slice / self.slices)
                v = 1 - (stack / self.stacks)

                normals.extend([x, y, z])
                tex_coords.extend([u, v])
                vertices.extend([self.radius * x, self.radius * y, self.radius * z])

        for stack in range(self.stacks):
            for slice in range(self.slices):
                first = (stack * (self.slices + 1)) + slice
                second = first + self.slices + 1

                indices.extend([first, second, first + 1])
                indices.extend([second, second + 1, first + 1])

        self.sphere_vertices = self.batch.add_indexed(
            len(vertices) // 3,
            GL_TRIANGLES,
            None,
            indices,
            ('v3f/static', vertices),
            ('n3f/static', normals),
            ('t2f/static', tex_coords)
        )

    def create_disk_vertices(self):
        vertices = []
        normals = []
        tex_coords = []
        indices = []

        num_segments = 100
        twist_factor = 5  # Factor to create the whirlpool effect

        # Top face of the disk
        for i in range(num_segments + 1):
            theta = 2.0 * math.pi * i / num_segments
            x = self.disk_radius * math.cos(theta)
            z = self.disk_radius * math.sin(theta)

            vertices.extend([x, self.disk_thickness / 2.0, z])
            normals.extend([0.0, 1.0, 0.0])

            # Creating a whirlpool effect in the texture coordinates
            u = (0.5 + (x / self.disk_radius) * 0.5) + (math.sin(twist_factor * theta) * 0.1)
            v = (0.5 + (z / self.disk_radius) * 0.5) + (math.cos(twist_factor * theta) * 0.1)
            tex_coords.extend([u, v])

        # Bottom face of the disk
        for i in range(num_segments + 1):
            theta = 2.0 * math.pi * i / num_segments
            x = self.disk_radius * math.cos(theta)
            z = self.disk_radius * math.sin(theta)

            vertices.extend([x, -self.disk_thickness / 2.0, z])
            normals.extend([0.0, -1.0, 0.0])

            # Creating a whirlpool effect in the texture coordinates
            u = (0.5 + (x / self.disk_radius) * 0.5) + (math.sin(twist_factor * theta) * 0.1)
            v = (0.5 + (z / self.disk_radius) * 0.5) + (math.cos(twist_factor * theta) * 0.1)
            tex_coords.extend([u, v])

        # Top face indices
        for i in range(1, num_segments):
            indices.extend([0, i, i + 1])

        # Bottom face indices
        offset = num_segments + 1
        for i in range(1, num_segments):
            indices.extend([offset, offset + i + 1, offset + i])

        # Side faces
        side_indices = []
        for i in range(num_segments):
            next_i = (i + 1) % num_segments
            top_curr = i
            top_next = next_i
            bottom_curr = i + num_segments + 1
            bottom_next = next_i + num_segments + 1

            side_indices.extend([top_curr, bottom_curr, bottom_next])
            side_indices.extend([top_curr, bottom_next, top_next])

        indices.extend(side_indices)

        self.disk_vertices = self.batch.add_indexed(
            len(vertices) // 3,
            GL_TRIANGLES,
            None,
            indices,
            ('v3f/static', vertices),
            ('n3f/static', normals),
            ('t2f/static', tex_coords)
        )

    def draw(self, view_matrix, projection_matrix):
        glUseProgram(self.program)

        model_matrix = pyglet.math.Mat4()
        glUniformMatrix4fv(self.model_location, 1, GL_TRUE, model_matrix)
        glUniformMatrix4fv(self.view_location, 1, GL_TRUE, view_matrix)
        glUniformMatrix4fv(self.projection_location, 1, GL_TRUE, projection_matrix)

        glUniform3f(self.light_pos_location, 1.0, 1.0, 1.0)
        glUniform3f(self.view_pos_location, 0.0, 0.0, -5.0)

        # Draw sphere
        glUniform1i(self.is_disk_location, GL_FALSE)
        self.sphere_vertices.draw(GL_TRIANGLES)

        # Draw disk
        glUniform1i(self.is_disk_location, GL_TRUE)
        self.disk_vertices.draw(GL_TRIANGLES)

        glUseProgram(0)


class Window(pyglet.window.Window):
    def __init__(self, width, height, title='Pyglet Sphere'):
        super().__init__(width, height, title)
        self.sphere = Sphere(3.83, 40, 40, 15, 0.15)
        # gargantua 150000000 / 20000000 -> 1:75000000
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)

        # Set light properties
        light_ambient = (GLfloat * 4)(0.5, 0.5, 0.5, 1.0)
        light_diffuse = (GLfloat * 4)(1.0, 1.0, 1.0, 1.0)
        light_specular = (GLfloat * 4)(1.0, 1.0, 1.0, 1.0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

        # Set material properties
        mat_specular = (GLfloat * 4)(1.0, 1.0, 1.0, 1.0)
        mat_shininess = (GLfloat * 1)(50.0)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

        self.projection = pyglet.math.Mat4().perspective_projection(65, width / height, 0.1, 1000)

    def on_draw(self):
        self.clear()
        view = pyglet.math.Mat4().look_at(0, 0, -5, 0, 0, 0, 0, 1, 0)
        self.sphere.draw(view, self.projection)

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        self.projection = pyglet.math.Mat4().perspective_projection(65, width / height, 0.1, 1000)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.close()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            angle_y = dx * 0.5
            angle_x = dy * 0.5
            self.sphere.rotate(angle_x, angle_y)


if __name__ == '__main__':
    window = Window(800, 600)
    pyglet.app.run()
