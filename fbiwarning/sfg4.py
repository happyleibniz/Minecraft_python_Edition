import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

class Sphere:
    def __init__(self, radius, slices, stacks):
        self.radius = radius
        self.slices = slices
        self.stacks = stacks

    def draw(self):
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
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
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (GLfloat * 4)(0.8, 0.1, 0.1, 1.0))

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

    def update(self, dt):
        if self.keys[key.W]:
            self.camera_z += self.camera_speed
        if self.keys[key.S]:
            self.camera_z -= self.camera_speed
        if self.keys[key.A]:
            self.camera_x += self.camera_speed
        if self.keys[key.D]:
            self.camera_x -= self.camera_speed
        if self.keys[key.UP]:
            self.camera_y -= self.camera_speed
        if self.keys[key.DOWN]:
            self.camera_y += self.camera_speed
        if self.keys[key.SPACE]:
            self.camera_y -= self.camera_speed

    def on_deactivate(self):
        self.set_exclusive_mouse(False)

    def on_activate(self):
        self.set_exclusive_mouse(True)

if __name__ == '__main__':
    window = Window(800, 600)
    pyglet.clock.schedule_interval(window.update, 1/60.0)  # Update at 60Hz
    pyglet.app.run()
