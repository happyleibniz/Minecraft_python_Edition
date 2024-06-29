import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
import math
import random

class Sphere:
    def __init__(self, radius, slices, stacks, disk_radius):
        self.radius = radius
        self.slices = slices
        self.stacks = stacks
        self.disk_radius = disk_radius

        self.batch = pyglet.graphics.Batch()

        # Create vertex list for sphere
        self.create_sphere_vertices()

        # Create vertex list for disk
        self.create_disk_vertices()

    def create_sphere_vertices(self):
        vertices = []
        indices = []
        tex_coords = []

        # Generate vertices, indices, and texture coordinates for sphere
        for stack in range(self.stacks):
            theta_stack = stack * math.pi / self.stacks
            theta_stack_next = (stack + 1) * math.pi / self.stacks

            for slice in range(self.slices):
                phi_slice = slice * 2 * math.pi / self.slices
                phi_slice_next = (slice + 1) * 2 * math.pi / self.slices

                # Vertices
                vertex1 = (
                    self.radius * math.sin(theta_stack) * math.cos(phi_slice),
                    self.radius * math.cos(theta_stack),
                    self.radius * math.sin(theta_stack) * math.sin(phi_slice)
                )
                vertex2 = (
                    self.radius * math.sin(theta_stack) * math.cos(phi_slice_next),
                    self.radius * math.cos(theta_stack),
                    self.radius * math.sin(theta_stack) * math.sin(phi_slice_next)
                )
                vertex3 = (
                    self.radius * math.sin(theta_stack_next) * math.cos(phi_slice_next),
                    self.radius * math.cos(theta_stack_next),
                    self.radius * math.sin(theta_stack_next) * math.sin(phi_slice_next)
                )
                vertex4 = (
                    self.radius * math.sin(theta_stack_next) * math.cos(phi_slice),
                    self.radius * math.cos(theta_stack_next),
                    self.radius * math.sin(theta_stack_next) * math.sin(phi_slice)
                )

                vertices.extend(vertex1)
                vertices.extend(vertex2)
                vertices.extend(vertex3)
                vertices.extend(vertex4)

                # Texture coordinates
                tex_coords.extend([0, 0, 1, 0, 1, 1, 0, 1])

                # Indices
                index_offset = stack * self.slices * 4
                indices.extend([index_offset + slice * 4, index_offset + slice * 4 + 1, index_offset + slice * 4 + 2])
                indices.extend([index_offset + slice * 4, index_offset + slice * 4 + 2, index_offset + slice * 4 + 3])

        # Add vertices, indices, and texture coordinates to vertex list
        self.sphere_vertices = self.batch.add(
            len(vertices) // 3,
            GL_TRIANGLES,
            None,
            ('v3f/static', vertices),
            ('t2f/static', tex_coords)
        )

    def create_disk_vertices(self):
        vertices = []
        indices = []
        tex_coords = []

        # Generate vertices, indices, and texture coordinates for disk
        for stack in range(10):
            theta_stack = stack * math.pi / 10
            theta_stack_next = (stack + 1) * math.pi / 10

            for slice in range(20):
                phi_slice = slice * 2 * math.pi / 20
                phi_slice_next = (slice + 1) * 2 * math.pi / 20

                # Vertices
                vertex1 = (
                    self.disk_radius * math.sin(theta_stack) * math.cos(phi_slice),
                    0,
                    self.disk_radius * math.sin(theta_stack) * math.sin(phi_slice)
                )
                vertex2 = (
                    self.disk_radius * math.sin(theta_stack) * math.cos(phi_slice_next),
                    0,
                    self.disk_radius * math.sin(theta_stack) * math.sin(phi_slice_next)
                )
                vertex3 = (
                    self.disk_radius * math.sin(theta_stack_next) * math.cos(phi_slice_next),
                    0,
                    self.disk_radius * math.sin(theta_stack_next) * math.sin(phi_slice_next)
                )
                vertex4 = (
                    self.disk_radius * math.sin(theta_stack_next) * math.cos(phi_slice),
                    0,
                    self.disk_radius * math.sin(theta_stack_next) * math.sin(phi_slice)
                )

                vertices.extend(vertex1)
                vertices.extend(vertex2)
                vertices.extend(vertex3)
                vertices.extend(vertex4)

                # Texture coordinates
                tex_coords.extend([0, 0, 1, 0, 1, 1, 0, 1])

                # Indices
                index_offset = stack * 20 * 4
                indices.extend([index_offset + slice * 4, index_offset + slice * 4 + 1, index_offset + slice * 4 + 2])
                indices.extend([index_offset + slice * 4, index_offset + slice * 4 + 2, index_offset + slice * 4 + 3])

        # Add vertices, indices, and texture coordinates to vertex list
        self.disk_vertices = self.batch.add(
            len(vertices) // 3,
            GL_TRIANGLES,
            None,
            ('v3f/static', vertices),
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
        self.sphere = Sphere(1.0, 40, 40, 1.5)

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
        self.camera_pitch = max(min(self.camera_pitch, 89), -89)  # Clamp the pitch to avoid gimbal lock

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
