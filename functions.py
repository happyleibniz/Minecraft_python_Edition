import os
import time
from random import randint

import pygame.display
import pyglet
from OpenGL.GL import *
from settings import *


def load_textures(self):
    print("Loading textures...")
    t = self.texture
    dirs = ['textures']
    while dirs:
        d = dirs.pop(0)
        textures = os.listdir(d)
        for file in textures:
            if os.path.isdir(d + '/' + file):
                dirs += [d + '/' + file]
            else:
                if ".png" not in file:
                    continue

                image = pyglet.image.load(d + '/' + file)
                if image.width == 1024 and image.height == 1024 or image.width == 512 and image.height == 512 or image.width == 256 and image.height == 256 or image.width == 128 and image.height == 128:
                    # Adjust loading method for 1024x textures
                    texture = image.get_texture()  # Example adjustment for higher resolution
                elif image.width == 8 and image.height == 8 or image.width == 16 and image.height == 16 or image.width == 32 and image.height == 32 or image.width == 64 and image.height == 64:
                    # Continue with the existing method for other resolutions
                    texture = image.get_mipmapped_texture()

                n = file.split('.')[0]
                self.texture_dir[n] = d
                self.texture[n] = pyglet.graphics.TextureGroup(texture)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

                print("Successful loaded", n, "texture!")
    done = []
    items = sorted(self.texture_dir.items(), key=lambda i: i[0])
    for n1, d in items:
        n = n1.split(' ')[0]
        if n in done:
            continue
        done += [n]
        if d.startswith('textures/blocks'):
            if d == 'textures/blocks':
                self.inventory_textures[n] = pyglet.resource.image(f"{d}/{n}.png")
                self.block[n] = t[n], t[n], t[n], t[n], t[n], t[n]
            elif d == 'textures/blocks/tbs':
                self.inventory_textures[n] = pyglet.resource.image(f"{d}/{n} s.png")
                self.block[n] = t[n + ' s'], t[n + ' s'], t[n + ' b'], t[n + ' t'], t[n + ' s'], t[n + ' s']
            elif d == 'textures/blocks/ts':
                self.inventory_textures[n] = pyglet.resource.image(f"{d}/{n} s.png")
                self.block[n] = t[n + ' s'], t[n + ' s'], t[n + ' t'], t[n + ' t'], t[n + ' s'], t[n + ' s']
            if n in self.inventory_textures:
                self.inventory_textures[n].width = 22
                self.inventory_textures[n].height = 22


def translateSeed(seed):
    res = ""
    if seed == "":
        seed = str(randint(998, 43433))
    for i in seed:
        res += str(ord(i))
    while len(res) < 10:
        res += res[:-1]
    return int(res[0:10])


def cube_vertices(pos, n=0.5):
    x, y, z = pos
    v = tuple((x + X, y + Y, z + Z) for X in (-n, n) for Y in (-n, n) for Z in (-n, n))
    return tuple(tuple(k for j in i for k in v[j]) for i in
                 ((0, 1, 3, 2), (5, 4, 6, 7), (0, 4, 5, 1), (3, 7, 6, 2), (4, 0, 2, 6), (1, 5, 7, 3)))


def flatten(lst): return sum(map(list, lst), [])


def roundPos(pos):
    x, y, z = pos
    return round(x), round(y), round(z)


def getSum(s):
    res = 0
    for i in s:
        res += int(i)

    return res


def adjacent(x, y, z):
    for p in ((x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1), (x, y, z + 1)): yield p


def drawInfoLabel(gl, text, xx=0, yy=0, style=None, size=15, anchor_x='left', anchor_y='baseline', opacity=1, rotate=0,
                  label_color=(255, 255, 255), shadow_color=(56, 56, 56), scale=0, shadow=True):
    if style is None:
        style = []
    y = -21
    ms = size / 6
    for i in text.split("\n"):
        ix = ms
        iy = gl.HEIGHT + y + yy - ms
        if xx:
            ix = xx + ms
        if yy:
            iy = yy - ms
        shadow_lbl = pyglet.text.Label(i,
                                       font_name='Minecraft Rus',
                                       color=(shadow_color[0], shadow_color[1], shadow_color[2], round(opacity * 255)),
                                       font_size=size,
                                       x=ix, y=iy,
                                       anchor_x=anchor_x,
                                       anchor_y=anchor_y)
        lbl = pyglet.text.Label(i,
                                font_name='Minecraft Rus',
                                color=(label_color[0], label_color[1], label_color[2], round(opacity * 255)),
                                font_size=size,
                                x=ix - ms, y=iy + ms,
                                anchor_x=anchor_x,
                                anchor_y=anchor_y)
        if not style:
            lbl.set_style("background_color", (69, 69, 69, 100))
        else:
            for st in style:
                lbl.set_style(st[0], st[1])
                shadow_lbl.set_style(st[0], st[1])
        if rotate:
            glRotatef(rotate, 0.0, 0.0, 1.0)
        if scale:
            glScalef(scale, scale, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        if shadow:
            shadow_lbl.draw()  # TODO:pyglet.gl.lib.GLException: b'invalid value'
            lbl.draw()
        if rotate:
            glRotatef(-rotate, 0.0, 0.0, 1.0)
        y -= 21


def getElpsTime():
    return time.perf_counter_ns() * 1000 / 1000000000


def checkHover(ox, oy, ow, oh, mx, my):
    if ox < mx < ox + ow and oy < my < oy + oh:
        return True
    return False
