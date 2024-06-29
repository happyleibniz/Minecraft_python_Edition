import pyglet
from pyglet.gl import *

window = pyglet.window.Window()


# Define a function to draw a sphere
def draw_sphere(radius, slices, stacks):
    qobj = gluNewQuadric()
    gluQuadricNormals(qobj, GLU_SMOOTH)
    gluQuadricTexture(qobj, GL_TRUE)
    gluSphere(qobj, radius, slices, stacks)
    gluDeleteQuadric(qobj)


# Define a function to draw the scene
def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set up perspective projection
    gluPerspective(45, (window.width / window.height), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)  # Move the scene back a bit to see it

    # Draw a black hole (sphere)
    glColor3f(0.0, 0.0, 0.0)
    draw_sphere(0.2, 20, 20)

    # Draw the plasma disk
    glColor3f(1.0, 0.0, 0.0)  # Red color for the disk
    glBegin(GL_QUADS)
    glVertex3f(-1, -1, 0)
    glVertex3f(1, -1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(-1, 1, 0)
    glEnd()


# Define the update function (not necessary for a static scene)
def update(dt):
    pass


# Set up the OpenGL state
glClearColor(0.0, 0.0, 0.0, 1.0)
glEnable(GL_DEPTH_TEST)


# Set up the Pyglet event loop
@window.event
def on_draw():
    window.clear()
    draw_scene()


# Run the Pyglet event loop
pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()
