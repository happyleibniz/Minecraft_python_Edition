import pyglet
import numpy as np
from pyglet.gl import *
class Sphere:
    def __init__(self, center, radius):
        self.center = np.array(center)
        self.radius = radius

    def intersect(self, ray_origin, ray_direction):
        oc = ray_origin - self.center
        a = np.dot(ray_direction, ray_direction)
        b = 2.0 * np.dot(oc, ray_direction)
        c = np.dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return -1
        else:
            return (-b - np.sqrt(discriminant)) / (2.0 * a)

class RayTracer:
    def __init__(self):
        self.spheres = []

    def add_sphere(self, sphere):
        self.spheres.append(sphere)

    def trace(self, ray_origin, ray_direction):
        closest_sphere = None
        closest_t = np.inf
        for sphere in self.spheres:
            t = sphere.intersect(ray_origin, ray_direction)
            if t > 0 and t < closest_t:
                closest_t = t
                closest_sphere = sphere
        return closest_sphere

class RayTracingWindow(pyglet.window.Window):
    def __init__(self, width, height, title='Ray Tracing'):
        super().__init__(width, height, title)
        self.tracer = RayTracer()
        self.tracer.add_sphere(Sphere([0, 0, 5], 1))
        self.tracer.add_sphere(Sphere([0, -1001, 0], 1000))
        self.image = self.trace_image(width, height)

    def trace_image(self, width, height):
        camera_pos = np.array([0, 0, 0])
        image = np.zeros((height, width, 3))
        fov = np.pi / 3
        aspect_ratio = width / height
        for i in range(height):
            for j in range(width):
                x = (2 * (j + 0.5) / width - 1) * aspect_ratio * np.tan(fov / 2)
                y = (1 - 2 * (i + 0.5) / height) * np.tan(fov / 2)
                direction = np.array([x, y, -1]) - camera_pos
                direction /= np.linalg.norm(direction)
                sphere = self.tracer.trace(camera_pos, direction)
                if sphere:
                    image[i, j] = [0, 255, 0]  # Green color for sphere hit
                else:
                    image[i, j] = [0, 0, 0]  # Black for no intersection
        return image

    def on_draw(self):
        self.clear()
        self.draw_image()

    def draw_image(self):
        glDrawPixels(self.image.shape[1], self.image.shape[0], GL_RGB, GL_UNSIGNED_BYTE, self.image)


if __name__ == '__main__':
    window = RayTracingWindow(800, 600, 'Ray Tracing')
    pyglet.app.run()
