import pyglet
from pyglet.gl import *
import numpy as np

# Set up window and OpenGL context
window = pyglet.window.Window(width=800, height=600, resizable=True)
glClearColor(1, 1, 1, 1)  # Set background color to white
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Define vertex and color data for a simple black hole
vertices = [0, 0, 0]  # Center of the black hole
colors = [0, 0, 0, 1]  # Black color
num_segments = 100
scale = 2.0  # Increase the scale of the black hole
for i in range(num_segments + 1):
    angle = 2.0 * np.pi * i / num_segments
    x = scale * 0.5 * np.cos(angle)
    y = scale * 0.5 * np.sin(angle)
    vertices.extend([x, y, 0])
    # Append black color for each vertex
    colors.extend([0, 0, 0, 1])  # Black color

# Convert data to OpenGL arrays
vertices_gl = (GLfloat * len(vertices))(*vertices)
colors_gl = (GLfloat * len(colors))(*colors)

@window.event
def on_draw():
    window.clear()
    glLoadIdentity()
    glTranslatef(0, 0, -10)  # Move the camera back further along the z-axis
    glRotatef(45, 1, 0, 0)  # Rotate around the x-axis
    glRotatef(45, 0, 1, 0)  # Rotate around the y-axis

    # Draw black hole
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices_gl)
    glColorPointer(4, GL_FLOAT, 0, colors_gl)
    glDrawArrays(GL_TRIANGLE_FAN, 0, len(vertices) // 3)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)

def update(dt):
    pass

# Schedule update function
pyglet.clock.schedule(update)

# Run the application
pyglet.app.run()
