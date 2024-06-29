import pyglet
from pyglet.gl import *
from math import pi, cos, sin


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

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        glTranslatef(0, 0, -5)
        self.sphere.draw()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65, width / float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        return pyglet.event.EVENT_HANDLED


if __name__ == '__main__':
    window = Window(800, 600)
    pyglet.app.run()
