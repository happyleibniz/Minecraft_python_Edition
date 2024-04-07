import random
# import timeit
import pygame
from pyglet import font
import json

lang_type_file = open("gui/lang.mclanguage", "r")
lang_type = str(lang_type_file.read())
current_language = lang_type
print(current_language)


def load_language():
    with open(f"assets/Minecraft/languages/{current_language}.json", "r", encoding="utf-8") as file:
        return json.load(file)


translations = load_language()
if current_language == "zh":
    font.add_file('gui/MinecraftAE.ttf')
    mainFont = font.load('gui/MinecraftAE.ttf', 15)
elif current_language == "en":
    font.add_file('gui/main.ttf')
    mainFont = font.load('gui/main.ttf', 20)

pygame.init()

monitor = pygame.display.Info()
WIDTH = 927  # monitor.current_w
HEIGHT = 566  # monitor.current_h
MAX_FPS = 200
PAUSE = True
IN_MENU = True
MC_VERSION = "Pre Classic 0.43"
clock = pygame.time.Clock()
DEBUG = True
FOV = 100
RENDER_DISTANCE = 999

CHUNKS_RENDER_DISTANCE = 900
CHUNK_SIZE = (4, 60, 4)
