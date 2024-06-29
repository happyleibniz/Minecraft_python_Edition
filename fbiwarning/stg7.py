import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
import math
import numpy as np

class Sphere:
    def __init__(self, radius, slices, stacks):
        self.radius = radius
        self.slices = slices
        self.stacks = stacks

    def draw(self):
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        glColor3f(0.0, 0.0, 0.0)  # Set color to black
        gluSphere(quad, self.radius, self.slices, self.stacks)
        gluDeleteQuadric(quad)

class Window(pyglet.window.Window):
    def __init__(self, width, height, title='Pyglet Sphere'):
        super().__init__(width, height, title)
        self.sphere = Sphere(1.0, 40, 40)

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

        # Black hole properties
        self.black_hole_center = (0, 0, 0)
        self.black_hole_radius = 2

        # Generate vertex array for batch rendering
        self.vertices = np.zeros((width * height * 3,), dtype=np.float32)
        self.indices = np.arange(width * height, dtype=np.uint32)
        self.vertex_list = pyglet.graphics.vertex_list_indexed(width * height, self.indices, ('v3f', self.vertices))

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        glRotatef(self.camera_pitch, 1, 0, 0)
        glRotatef(self.camera_yaw, 0, 1, 0)
        glTranslatef(self.camera_x, self.camera_y, self.camera_z)

        # Ray tracing and batch rendering
        index = 0
        for y in range(self.height):
            for x in range(self.width):
                ray_direction = self.calculate_ray_direction(x, y)
                intersection_point = self.ray_sphere_intersection(ray_direction)
                if intersection_point:
                    dist = self.distance(intersection_point, self.black_hole_center)
                    if dist < self.black_hole_radius:
                        # Apply distortion effect based on distance from the black hole
                        distortion_factor = 1.0 / (1 + (dist / self.black_hole_radius) ** 2)
                        self.vertices[index] = x
                        self.vertices[index + 1] = y
                        self.vertices[index + 2] = 0
                        index += 3

        # Update vertex array
        self.vertex_list.vertices = self.vertices
        self.vertex_list.draw(pyglet.gl.GL_POINTS)

    def calculate_ray_direction(self, x, y):
        # Convert pixel coordinates to world space
        ray_x = ((2.0 * x) / self.width - 1) * math.tan(math.radians(65) / 2) * (self.width / self.height)
        ray_y = (1 - (2.0 * y) / self.height) * math.tan(math.radians(65) / 2)
        ray_z = -1
        return (ray_x, ray_y, ray_z)

    def ray_sphere_intersection(self, ray_direction):
        # Calculate intersection point with the sphere
        sphere_center = self.black_hole_center
        sphere_radius = self.black_hole_radius

        # Ray-sphere intersection equation
        a = ray_direction[0] ** 2 + ray_direction[1] ** 2 + ray_direction[2] ** 2
        b = 2 * (ray_direction[0] * (self.camera_x - sphere_center[0]) +
                 ray_direction[1] * (self.camera_y - sphere_center[1]) +
                 ray_direction[2] * (self.camera_z - sphere_center[2]))
        c = (self.camera_x - sphere_center[0]) ** 2 + (self.camera_y - sphere_center[1]) ** 2 + \
            (self.camera_z - sphere_center[2]) ** 2 - sphere_radius ** 2

        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return None
        else:
            t = (-b - math.sqrt(discriminant)) / (2 * a)
            intersection_point = (self.camera_x + t * ray_direction[0],
                                  self.camera_y + t * ray_direction[1],
                                  self.camera_z + t * ray_direction[2])
            return intersection_point

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

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
    pyglet.clock.schedule_interval(window.update, 0)  # Update at 60Hz
    pyglet.app.run()
