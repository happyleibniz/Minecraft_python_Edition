from pyglet.gl import *
from OpenGL.GL import GL_LIGHTING

window = pyglet.window.Window()


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Enable lighting
    glEnable(GL_LIGHTING)  # 2896
    glEnable(GL_LIGHT0)
