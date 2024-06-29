import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
import math

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

    def draw(self):
        glColor3f(0.0, 0.0, 0.0)  # Set color to black
        self.sphere_vertices.draw(GL_TRIANGLES)
        glColor3f(1.0, 0.5, 0.0)  # Set color to orange for the disk
        self.disk_vertices.draw(GL_TRIANGLES)

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
        light_position = (GLfloat * 4)(1.0, 1.0, 1.0, 0.0)

        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        # Set material properties
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (GLfloat * 4)(0.0, 0.0, 0.0, 1.0))  # Set to black

        # Set the background color (RGB values between 0 and 1)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        pyglet.gl.glClearColor(0.5, 0.5, 0.5, 1)
        # Camera position and orientation
        self.camera_x = 0
        self.camera_y = 0
        self.camera_z = -5
        self.camera_speed = 0.1
        self.camera_pitch = 0
        self.camera_yaw = 0
        self.mouse_sensitivity = 0.1

        # Mouse visibility and focus
        self.set_exclusive_mouse(True)

        # Setup event handlers
        self.push_handlers(self.on_key_press, self.on_key_release, self.on_mouse_motion)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        glRotatef(self.camera_pitch, 1, 0, 0)
        glRotatef(self.camera_yaw, 0, 1, 0)
        glTranslatef(self.camera_x, self.camera_y, self.camera_z)
        self.sphere.draw()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65, width / float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        return pyglet.event.EVENT_HANDLED

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.close()

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.camera_yaw += dx * self.mouse_sensitivity
        self.camera_pitch -= dy * self.mouse_sensitivity
        self.camera_pitch = max(min(self.camera_pitch, 89), -89)
        # Clamp the pitch to avoid gimbal lock

    def update(self, dt):
        forward_x = math.cos(math.radians(self.camera_yaw))
        forward_z = math.sin(math.radians(self.camera_yaw))
        right_x = math.cos(math.radians(self.camera_yaw + 90))
        right_z = math.sin(math.radians(self.camera_yaw + 90))

        if self.keys[key.W]:
            self.camera_x += right_x * self.camera_speed
            self.camera_z += right_z * self.camera_speed

        if self.keys[key.S]:
            self.camera_x -= right_x * self.camera_speed
            self.camera_z -= right_z * self.camera_speed

        if self.keys[key.A]:
            self.camera_x += forward_x * self.camera_speed
            self.camera_z += forward_z * self.camera_speed
        if self.keys[key.D]:
            self.camera_x -= forward_x * self.camera_speed
            self.camera_z -= forward_z * self.camera_speed
        if self.keys[key.SPACE]:
            self.camera_y -= self.camera_speed
        if self.keys[key.LSHIFT]:
            self.camera_y += self.camera_speed

    def on_deactivate(self):
        self.set_exclusive_mouse(False)

    def on_activate(self):
        self.set_exclusive_mouse(True)

if __name__ == '__main__':
    window = Window(800, 600)
    pyglet.clock.schedule_interval(window.update, 1 / 60.0)  # Update at 60Hz
    pyglet.app.run()
