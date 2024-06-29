import datetime
import logging
import gc
import math
import os
import pickle
import sys
from random import randint
import pygame.time
import pyglet
from OpenGL.GL import *
from OpenGL.raw.GLU import gluOrtho2D
from functions import drawInfoLabel, getElpsTime, translateSeed
from game.GUI.Button import Button
from game.GUI.Editarea import Editarea
from game.GUI.GUI import GUI
from game.GUI.Sliderbox import Sliderbox
from game.entity.Player import Player
from game.sound.BlockSound import BlockSound
from game.sound.Sound import Sound
from game.Scene import Scene
from game.world.Biomes import getBiomeByTemp
from game.world.worldGenerator import worldGenerator
from settings import *
import settings
from game.Mod.forge import mod_loader

log_filename = './logs/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
logging.basicConfig(
    filename=log_filename,
    filemode='w+',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

lang_choose = ["en", "zh"]

pyglet.options['debug_gl'] = False


def log_deb(msg):
    logging.debug(msg)
    print(msg)

def choose_langs():
    global lang_choose, mainFunction
    with open("gui/lang.mclanguage", "w") as mclanguagefile:
        if settings.lang_type == "en":
            mclanguagefile.write("zh")
        else:
            mclanguagefile.write("en")
    pygame.quit()
    print(os.getcwd())
    os.system("run.bat")
    sys.exit()


def respawn():
    log_deb("respawning...")
    pause()
    log_deb("setting player health point...")
    player.hp = 20
    player.playerDead = False
    log_deb("setting player position...")
    player.position = scene.startPlayerPos
    player.lastPlayerPosOnGround = scene.startPlayerPos


def saveWorld(worldGen, save_path):
    blocks = worldGen.blocks
    try:
        logging.info("Saving chunks for level 'Default'")
        with open(save_path + "/world.dat", "wb") as world_data_file:
            pickle.dump(blocks, world_data_file, protocol=pickle.HIGHEST_PROTOCOL)
    except FileNotFoundError as error_msg:
        logging.warning(f"WARNING: {error_msg}")
        print(f"WARNING: {error_msg} please check the log file")
    print("Successfully saved world ")


def quit_to_menu():
    log_deb("quitting to menu...")
    global PAUSE, IN_MENU, mainFunction
    log_deb("saving world...")
    saveWorld(scene.worldGen, "saves/Current_world")
    tex = gui.GUI_TEXTURES["options_background"]
    tex2 = gui.GUI_TEXTURES["black"]
    for scene_x in range(0, scene.WIDTH, tex.width):
        for scene_y in range(0, scene.HEIGHT, tex.height):
            tex.blit(scene_x, scene_y)
            tex2.blit(scene_x, scene_y)
    drawInfoLabel(scene, translations["quit.mainmenu"], xx=scene.WIDTH // 2, yy=scene.HEIGHT // 2,
                  style=[('', '')], size=12, anchor_x='center')
    pygame.display.flip()
    # clock.tick(MAX_FPS)

    PAUSE = True
    IN_MENU = True

    sound.initMusic(False)
    log_deb("playing musics...")
    sound.musicPlayer.play()
    sound.musicPlayer.set_volume(sound.volume)
    log_deb("resetting scene...")
    scene.resetScene()
    scene.initScene()

    player.position = [0, -90, 0]
    player.hp = -1
    player.playerDead = False

    gc.collect()
    mainFunction = draw_main_menu


def show_settings():
    global mainFunction
    mainFunction = draw_settings_menu


def edit_panorama():
    global mainFunction
    mainFunction = draw_panorama_menu


def draw_command_function():
    global mainFunction
    mainFunction = draw_command


def close_settings():
    global mainFunction
    mainFunction = draw_main_menu


def start_new_game():
    log_deb("starting new game, hang on tight!")
    global mainFunction
    if not os.path.exists("saves/Current_world"):
        os.makedirs("saves/Current_world")
    
    sound.musicPlayer.stop()
    sound.initMusic(True)
    scene.worldGen = worldGenerator(scene, translateSeed(seedEditArea.text))
    mainFunction = gen_world


def pause():
    log_deb("pausing")
    global PAUSE, mainFunction
    PAUSE = not PAUSE
    scene.allowEvents["movePlayer"] = True
    scene.allowEvents["keyboardAndMouse"] = True
    mainFunction = pause_menu


def death_screen():
    global PAUSE, mainFunction
    PAUSE = not PAUSE
    scene.allowEvents["movePlayer"] = True
    scene.allowEvents["keyboardAndMouse"] = True
    mainFunction = draw_death_screen


def draw_command(mc):
    scene.set2d()
    mp = pygame.mouse.get_pos()
    _keys = pygame.key.get_pressed()
    commandEditArea.x = scene.WIDTH // 2 - (commandEditArea.bg.width // 2)
    commandEditArea.y = scene.HEIGHT // 2 - (commandEditArea.bg.height // 2)
    commandEditArea.update(mp, mc, _keys)
    pygame.display.flip()
    # clock.tick(MAX_FPS)


def draw_panorama_menu(mc):
    def cpt_16x():
        log_deb("changing panorama...")
        with open("assets/Minecraft/panorama.txt", "w") as f:
            f.write(fr"assets/Minecraft/textures/gui/title/background/16x/")
            f.close()
        print("done")

    def cpt_17x():
        log_deb("changing panorama...")
        with open("assets/Minecraft/panorama.txt", "w") as f:
            f.write(fr"assets/Minecraft/textures/gui/title/background/17x/")
            f.close()
        print("done")

    def cpt_120x():
        log_deb("changing panorama...")
        with open("assets/Minecraft/panorama.txt", "w") as f:
            f.write(fr"assets/Minecraft/textures/gui/title/background/120x/")
            f.close()
        print("done")

    def rp():
        log_deb("changing panorama...")
        with open("assets/Minecraft/panorama.txt", "w") as f:
            f.write("gui/bg/")
            f.close()
        print("done")

    scene.set2d()
    tex = gui.GUI_TEXTURES["options_background"]
    tex2 = gui.GUI_TEXTURES["black"]
    for ix in range(0, scene.WIDTH, tex.width):
        for iy in range(0, scene.HEIGHT, tex.height):
            tex.blit(ix, iy)
            tex2.blit(ix, iy)
    mp = pygame.mouse.get_pos()
    Pa1Button = Button(scene, "Mc 1.6.x Panorama", 0, 0, text_x=scene.WIDTH // 7)
    Pa1Button.setEvent(cpt_16x)
    Pa1Button.x = scene.WIDTH // 7 - (Pa1Button.button.width // 3.5)
    Pa1Button.y = scene.HEIGHT // 3 - (Pa1Button.button.height // 4) - 125
    Pa1Button.update(mp, mc)
    Pa2Button = Button(scene, "Mc 1.7.x Panorama", 0, 0, text_x=scene.WIDTH // 7)
    Pa2Button.setEvent(cpt_17x)
    Pa2Button.x = scene.WIDTH // 7 - (Pa2Button.button.width // 3.5)
    Pa2Button.y = scene.HEIGHT // 2.4 - (Pa2Button.button.height // 4) - 125
    Pa2Button.update(mp, mc)
    Pa3Button = Button(scene, "Mc 1.20.x Panorama", 0, 0, text_x=scene.WIDTH // 7)
    Pa3Button.setEvent(cpt_120x)
    Pa3Button.x = scene.WIDTH // 7 - (Pa3Button.button.width // 3.5)
    Pa3Button.y = scene.HEIGHT // 2 - (Pa3Button.button.height // 4) - 125
    Pa3Button.update(mp, mc)
    rstButton = Button(scene, "Reset Panorama", 0, 0)
    rstButton.setEvent(rp)
    rstButton.x = scene.WIDTH // 2 - (rstButton.button.width // 2)
    rstButton.y = scene.HEIGHT // 2 - (rstButton.button.height // 2) + 130
    rstButton.update(mp, mc)
    closeSettingsButton.x = scene.WIDTH // 2 - (closeSettingsButton.button.width // 2)
    closeSettingsButton.y = scene.HEIGHT // 2 - (closeSettingsButton.button.height // 2) + 180
    closeSettingsButton.update(mp, mc)
    pygame.display.flip()
    # clock.tick(MAX_FPS)


def draw_settings_menu(mc):
    scene.set2d()

    tex = gui.GUI_TEXTURES["options_background"]
    tex2 = gui.GUI_TEXTURES["black"]
    for ix in range(0, scene.WIDTH, tex.width):
        for iy in range(0, scene.HEIGHT, tex.height):
            tex.blit(ix, iy)
            tex2.blit(ix, iy)
    mp = pygame.mouse.get_pos()

    # Volume slider box
    soundVolumeSliderBox.x = scene.WIDTH // 2 - (soundVolumeSliderBox.bg.width // 2) - 170
    soundVolumeSliderBox.y = scene.HEIGHT // 2 - (soundVolumeSliderBox.bg.height // 2) - 180
    soundVolumeSliderBox.update(mp)
    #

    # Seed edit area
    seedEditArea.x = scene.WIDTH // 2 - (seedEditArea.bg.width // 2) - 170
    seedEditArea.y = scene.HEIGHT // 2 - (seedEditArea.bg.height // 2) - 130
    seedEditArea.update(mp, mc, keys)
    #
    editPanoramaButton = Button(scene, translations['ed.pano'], 0, 0, text_x=scene.WIDTH // 2 - (400 // 2))
    editPanoramaButton.setEvent(edit_panorama)
    editPanoramaButton.x = scene.WIDTH // 2 - (editPanoramaButton.button.width // 2) - 170
    editPanoramaButton.y = scene.HEIGHT // 2 - (editPanoramaButton.button.height // 2) - 80
    editPanoramaButton.update(mp, mc)

    # Close
    closeSettingsButton.x = scene.WIDTH // 2 - (closeSettingsButton.button.width // 2)
    closeSettingsButton.y = scene.HEIGHT // 2 - (closeSettingsButton.button.height // 2) + 160
    closeSettingsButton.update(mp, mc)
    # language button
    lang_button = Button(scene, translations["gui.lang"], 0, 0, text_x=scene.WIDTH // 2 - (400 // 2))
    lang_button.setEvent(choose_langs)
    lang_button.x = scene.WIDTH // 2 - (lang_button.button.width // 2) - 170
    lang_button.y = scene.HEIGHT // 2 - (lang_button.button.height // 2) - 30
    lang_button.update(mp, mc)
    #

    sound.musicPlayer.set_volume(soundVolumeSliderBox.val / 100)
    sound.volume = soundVolumeSliderBox.val / 100

    pygame.display.flip()
    # clock.tick(MAX_FPS)


def draw_death_screen(mc):
    scene.set2d()
    bg = gui.GUI_TEXTURES["red"]
    bg.width = scene.WIDTH
    bg.height = scene.HEIGHT
    bg.blit(0, 0)

    mp = pygame.mouse.get_pos()

    drawInfoLabel(scene, translations["player dead"], xx=scene.WIDTH // 2,
                  yy=scene.HEIGHT - scene.HEIGHT // 4, style=[('', '')],
                  size=34, anchor_x='center')

    # Back to Game button
    respawnButton.x = scene.WIDTH // 2 - (respawnButton.button.width // 2)
    respawnButton.y = scene.HEIGHT // 2 - (respawnButton.button.height // 2) - 50
    respawnButton.update(mp, mc)
    #

    # Quit to title button
    quitWorldButton.text = translations["death.titlescreen"]
    quitWorldButton.x = scene.WIDTH // 2 - (quitButton.button.width // 2)
    quitWorldButton.y = scene.HEIGHT // 2 - (quitButton.button.height // 2)
    quitWorldButton.update(mp, mc)
    #

    pygame.display.flip()
    # clock.tick(MAX_FPS)


def pause_menu(mc):
    scene.set2d()
    bg = gui.GUI_TEXTURES["black"]
    bg.width = scene.WIDTH
    bg.height = scene.HEIGHT
    bg.blit(0, 0)

    mp = pygame.mouse.get_pos()

    drawInfoLabel(scene, translations["game.menu"], xx=scene.WIDTH // 2, yy=scene.HEIGHT - scene.HEIGHT // 4,
                  style=[('', '')],
                  size=12, anchor_x='center')

    # Back to Game button
    resumeButton.x = scene.WIDTH // 2 - (resumeButton.button.width // 2)
    resumeButton.y = scene.HEIGHT // 2 - (resumeButton.button.height // 2) - 50
    resumeButton.update(mp, mc)
    #

    # Quit to title button
    quitWorldButton.text = translations["quit.title"]
    quitWorldButton.x = scene.WIDTH // 2 - (quitButton.button.width // 2)
    quitWorldButton.y = scene.HEIGHT // 2 - (quitButton.button.height // 2)
    quitWorldButton.update(mp, mc)
    #

    pygame.display.flip()
    # clock.tick(MAX_FPS)


def gen_world(mc):
    global IN_MENU, PAUSE, resizeEvent
    chunk_cnt = 220

    tex = gui.GUI_TEXTURES["options_background"]
    tex2 = gui.GUI_TEXTURES["black"]
    for ix in range(0, scene.WIDTH, tex.width):
        for iy in range(0, scene.HEIGHT, tex.height):
            tex.blit(ix, iy)
            tex2.blit(ix, iy)

    scene.genWorld()
    if scene.worldGen.start - len(scene.worldGen.queue) > chunk_cnt:
        scene.genTime = 16
        IN_MENU = False
        PAUSE = False

    proc = round((scene.worldGen.start - len(scene.worldGen.queue)) * 100 / chunk_cnt)
    drawInfoLabel(scene, translations["load.world"], xx=scene.WIDTH // 2, yy=scene.HEIGHT // 2, style=[('', '')],
                  size=12, anchor_x='center')
    drawInfoLabel(scene, translations["gen.terrain"] + f" {proc}%...", xx=scene.WIDTH // 2, yy=scene.HEIGHT // 2 - 39,
                  style=[('', '')], size=12, anchor_x='center')

    pygame.display.flip()
    # clock.tick(MAX_FPS)


def draw_main_menu(mc):
    global mainMenuRotation, IN_MENU, PAUSE
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.7, 1, 1))
    glFogf(GL_FOG_START, 0)
    glFogf(GL_FOG_END, 1000)

    scene.set3d()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    glRotatef(mainMenuRotation[0], 1, 0, 0)
    glRotatef(mainMenuRotation[1], 0, 1, 0)
    glTranslatef(0, 0, 0)

    scene.draw()
    scene.drawPanorama()

    glPopMatrix()
    scene.set2d()
    mp = pygame.mouse.get_pos()

    tex = gui.GUI_TEXTURES["game_logo"]
    tex.blit(scene.WIDTH // 2 - (tex.width // 2), scene.HEIGHT - tex.height - (scene.HEIGHT // 15))

    drawInfoLabel(scene, f"Minecraft {MC_VERSION}", xx=10, yy=10, style=[('', '')], size=12)

    # Single player button
    singleplayer_button.x = scene.WIDTH // 2 - (singleplayer_button.button.width // 2)
    singleplayer_button.y = scene.HEIGHT // 2 - (singleplayer_button.button.height // 2) - 25
    singleplayer_button.update(mp, mc)
    #

    # Options button
    optionsButton = Button(scene, translations["options"], 0, 0, button=gui.GUI_TEXTURES["button_bg_half"],
                           button_hovered=gui.GUI_TEXTURES["button_bg_hover_half"],
                           text_x=scene.WIDTH // 2 - (200 // 2))
    optionsButton.setEvent(show_settings)
    optionsButton.x = scene.WIDTH // 2 - (optionsButton.button.width // 2) - 100
    optionsButton.y = scene.HEIGHT // 2 - (optionsButton.button.height // 2) + 125
    optionsButton.update(mp, mc)
    #

    # Quit button
    quitButton_ = Button(scene, translations["quit_game"], 0, 0, button=gui.GUI_TEXTURES["button_bg_half"],
                         button_hovered=gui.GUI_TEXTURES["button_bg_hover_half"],
                         text_x=scene.WIDTH // 2 - (200 // 2) + 200)
    quitButton_.setEvent(sys.exit)
    quitButton_.x = scene.WIDTH // 2 - (quitButton_.button.width // 2) + 100
    quitButton_.y = scene.HEIGHT // 2 - (quitButton_.button.height // 2) + 125
    quitButton_.update(mp, mc)
    # lang_bb
    lang_bb.x = scene.WIDTH // 2 - (optionsButton.button.width // 2) - 140
    lang_bb.y = scene.HEIGHT // 2 - (lang_bb.button.height // 2) + 125
    lang_bb.update(mp, mc)

    # Splash
    glPushMatrix()
    glTranslatef((scene.WIDTH // 2 + (tex.width // 2)) - 90, scene.HEIGHT - tex.height - (scene.HEIGHT // 15) + 15, 0.0)
    glRotatef(20.0, 0.0, 0.0, 1.0)
    var8 = 1.8 - abs(math.sin((getElpsTime() % 1000) / 1000.0 * math.pi * 2.0) * 0.1)
    var8 = var8 * 100.0 / ((24 * 12) + 32)
    drawInfoLabel(scene, splash, xx=1, yy=1, style=[('', '')], scale=var8, size=30, anchor_x='center',
                  label_color=(255, 255, 0), shadow_color=(63, 63, 0))
    glPopMatrix()
    #

    pygame.display.flip()
    # clock.tick(MAX_FPS)
    mainMenuRotation[0] = 0
    # if mainMenuRotation[0] < 75:
    #     mainMenuRotation[2] = False
    # if mainMenuRotation[0] > 25:
    #     mainMenuRotation[2] = True

    # if mainMenuRotation[2]:
    #     mainMenuRotation[0] -= 0.08
    # else:
    #     mainMenuRotation[0] += 0.08
    mainMenuRotation[1] += 0.035
    pyglet.gl.glViewport(0, 0, WIDTH, HEIGHT)
    # gc.collect()


if settings.DEBUG:
    log_deb(f"PyOpenGL version: {OpenGL.__version__}")
    log_deb(f"PyOpenGL platform: {OpenGL.platform}")
    log_deb(f"PyOpenGL extensions: {OpenGL.GL.glGetString(OpenGL.GL.GL_EXTENSIONS)}", )
    log_deb(f"PyOpenGL renderer: {OpenGL.GL.glGetString(OpenGL.GL.GL_RENDERER)}")
    log_deb(f"PyOpenGL vendor: {OpenGL.GL.glGetString(OpenGL.GL.GL_VENDOR)}")
    log_deb(f"PyOpenGL GL version: {OpenGL.GL.glGetString(OpenGL.GL.GL_VERSION)}")
    log_deb(f"Pygame Version:{pygame.version.ver}")
    log_deb(f"Pygame array interface:{pygame.get_array_interface}")
    log_deb(f"Pygame display driver:{pygame.display.get_driver()}")
    log_deb(f"Pygame display info:{pygame.display.Info()}")
    log_deb(f"Pyglet version:{pyglet.version}", )
    log_deb(f"Pyglet platform:{pyglet.compat_platform}")
    log_deb(f"Pyglet display driver:{pyglet.canvas.get_display()}")
    log_deb(f"Pyglet display info:{pyglet.canvas.get_display().get_default_screen()}")
    log_deb(f"Python Version:{sys.version}")
    log_deb(f"Python Platform:{sys.platform}")
    log_deb(f"Python Path:{sys.path}")
    log_deb(f"Python Executable:{sys.executable}")
    log_deb(f"PID process: {os.getpid()}")
    log_deb(f"PATH : {os.get_exec_path()}")

logging.info("Loading the game...")

resizeEvent = False
LAST_SAVED_RESOLUTION = [WIDTH, HEIGHT]
pygame.mixer.pre_init(44100, 16, 2, 4096)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE, vsync=1)

# Loading screen
glClearColor(1, 1, 1, 1)

glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glLoadIdentity()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, WIDTH, 0, HEIGHT)

logo = pyglet.resource.image("gui/mojang_studios.jpg")
logo.blit(WIDTH // 2 - (logo.width // 2), HEIGHT // 2 - (logo.height // 2))
pygame.display.flip()
#

sound = Sound()
scene = Scene()
gui = GUI(scene)
blockSound = BlockSound(scene)
player = Player(gl=scene)

player.position = [0, -9000, 0]

scene.blockSound = blockSound
scene.gui = gui
scene.sound = sound
scene.player = player

scene.deathScreen = death_screen
scene.initScene()
ModLoader = mod_loader.ModLoader(gl=scene, sound=sound, settings=settings, player=player, gui=gui, gc=gc)
ModLoader.try_better()
logging.info("setting player: happyleibniz")
logging.info("Loading sounds...")
sound.BLOCKS_SOUND["pickUp"] = pygame.mixer.Sound("sounds/pick.mp3")

print("Loading step sounds...")
sound.BLOCKS_SOUND["step"] = {}
for e, i in enumerate(os.listdir("sounds/step/")):
    soundName = i.split(".")[0][:-1]
    soundNum = i.split(".")[0][-1]

    if soundName not in sound.BLOCKS_SOUND["step"]:
        sound.BLOCKS_SOUND["step"][soundName] = []

    sound.BLOCKS_SOUND["step"][soundName].append(pygame.mixer.Sound("sounds/step/" + i))
    print("Successful loaded", soundName, "#" + soundNum, "sound!")

print("Loading dig sounds...")
sound.BLOCKS_SOUND["dig"] = {}
for e, i in enumerate(os.listdir("sounds/dig/")):
    soundName = i.split(".")[0][:-1]
    soundNum = i.split(".")[0][-1]

    if soundName not in sound.BLOCKS_SOUND["dig"]:
        sound.BLOCKS_SOUND["dig"][soundName] = []

    sound.BLOCKS_SOUND["dig"][soundName].append(pygame.mixer.Sound("sounds/dig/" + i))
    print("Successful loaded", soundName, "#" + soundNum, "sound!")

print("Loading explode sounds...")
sound.BLOCKS_SOUND["explode"] = []
for e, i in enumerate(os.listdir("sounds/expl"
                                 "ode/")):
    soundName = i.split(".")[0][:-1]
    soundNum = i.split(".")[0][-1]

    sound.BLOCKS_SOUND["explode"].append(pygame.mixer.Sound("sounds/explode/" + i))
    print("Successful loaded", soundName, "#" + soundNum, "sound!")

print("Loading damage sounds...")
sound.SOUNDS["damage"] = {}
for e, i in enumerate(os.listdir("sounds/damage/")):
    soundName = i.split(".")[0][:-1]
    soundNum = i.split(".")[0][-1]

    if soundName not in sound.SOUNDS["damage"]:
        sound.SOUNDS["damage"][soundName] = []

    sound.SOUNDS["damage"][soundName].append(pygame.mixer.Sound("sounds/damage/" + i))
    print("Successful loaded", soundName, "#" + soundNum, "sound!")

print("Loading GUI sounds...")
sound.SOUNDS["GUI"] = {}
for e, i in enumerate(os.listdir("sounds/gui/")):
    soundName = i.split(".")[0][:-1]
    soundNum = i.split(".")[0][-1]

    if soundName not in sound.SOUNDS["GUI"]:
        sound.SOUNDS["GUI"][soundName] = []

    sound.SOUNDS["GUI"][soundName].append(pygame.mixer.Sound("sounds/gui/" + i))
    print("Successful loaded", soundName, "#" + soundNum, "sound!")

print("Loading menu music...")
for e, i in enumerate(os.listdir("sounds/music/menu")):
    sound.MENU_MUSIC.append("sounds/music/menu/" + i)
    print("Successful loaded", i, "music!")

print("Loading game music...")
for e, i in enumerate(os.listdir("sounds/music/game")):
    sound.MUSIC.append("sounds/music/game/" + i)
    print("Successful loaded", i, "music!")
sound.initMusic(False)

print("Music loaded successful!")

print("Loading GUI textures...")
gui.GUI_TEXTURES = {
    "crafting_table": pyglet.resource.image("gui/crafting_table.png"),
    "inventory_window": pyglet.resource.image("gui/inventory_window.png"),
    "crosshair": pyglet.resource.image("gui/crosshair.png"),
    "inventory": pyglet.resource.image("gui/inventory.png"),
    "sel_inventory": pyglet.resource.image("gui/sel_inventory.png"),
    "fullheart": pyglet.resource.image("gui/fullheart.png"),
    "halfheart": pyglet.resource.image("gui/halfheart.png"),
    "heartbg": pyglet.resource.image("gui/heartbg.png"),
    "game_logo": pyglet.resource.image("gui/game_logo.png"),
    "button_bg": pyglet.resource.image("gui/gui_elements/button_bg.png"),
    "button_bg_half": pyglet.resource.image("gui/gui_elements/button_bg_half.png"),
    "button_bg_hover": pyglet.resource.image("gui/gui_elements/button_bg_hover.png"),
    "button_bg_hover_half": pyglet.resource.image("gui/gui_elements/button_bg_hover_half.png"),
    "edit_bg": pyglet.resource.image("gui/gui_elements/edit_bg.png"),
    "options_background": pyglet.resource.image("gui/gui_elements/options_background.png"),
    "black": pyglet.resource.image("gui/gui_elements/black.png"),
    "red": pyglet.resource.image("gui/gui_elements/red.png"),
    "selected": pyglet.resource.image("gui/gui_elements/selected.png"),
    "slider": pyglet.resource.image("gui/gui_elements/slider.png"),
    "language": pyglet.resource.image("gui/language_h.png"),
    "language_hover": pyglet.resource.image("gui/language_nh.png"),
}

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
this_ = [
    'crafting_table', "inventory_window", "inventory", "sel_inventory",
    "fullheart", "halfheart", "heartbg", "button_bg",
    "button_bg_hover", "edit_bg", "selected", "slider", "language",
    "language_hover", "button_bg_half", "button_bg_hover_half"
]
this__ = [
    "options_background", "black", "red"
]
this___ = [
    "game_logo",
]
for i in this_:
    texture = gui.GUI_TEXTURES[i]
    texture.width *= 2
    texture.height *= 2
for i in this__:
    texture = gui.GUI_TEXTURES[i]
    texture.width *= 6
    texture.height *= 6
for i in this___:
    texture = gui.GUI_TEXTURES[i]
    texture.width /= 2
    texture.height /= 2
gui.addGuiElement("crosshair", (scene.WIDTH // 2 - 9, scene.HEIGHT // 2 - 9))

player.inventory.initWindow()

showInfoLabel = False

print("Loading splashes...")
splfile = open("gui/splashes.txt", "r", errors='replace')
splash = (splfile.read().split("\n"))
splash = splash[randint(0, len(splash) - 1)]
splfile.close()

sound.musicPlayer.play()
sound.musicPlayer.set_volume(sound.volume)

# Main menu buttons
singleplayer_button = Button(scene, translations["singleplayer"], 0, 0)

quitButton = Button(scene, translations["quit_game"], 0, 0)
lang_bb = Button(scene, "", 0, 0, button=gui.GUI_TEXTURES['language'],
                 button_hovered=gui.GUI_TEXTURES['language_hover'])
singleplayer_button.setEvent(start_new_game)
quitButton.setEvent(exit)

#

# Settings objects
closeSettingsButton = Button(scene, "Close", 0, 0)
soundVolumeSliderBox = Sliderbox(scene, translations["sound.volume"], 100, 0, 0)
seedEditArea = Editarea(scene, translations["World.Seed"], 0, 0)
commandEditArea = Editarea(scene, "Commands input here", 0, 0)


def process_command(command):
    if command.strip() == "/clear":
        commandEditArea.text = ""
    elif command.strip() == "/exit":
        exit()


commandEditArea.setEvent(process_command)
closeSettingsButton.setEvent(close_settings)
#

# Pause menu buttons
resumeButton = Button(scene, translations["backgame"], 0, 0)
quitWorldButton = Button(scene, translations["gui.qtt"], 0, 0)

resumeButton.setEvent(pause)
quitWorldButton.setEvent(quit_to_menu)
#

# Death screen buttons
respawnButton = Button(scene, translations["respawn"], 0, 0)
respawnButton.setEvent(respawn)
#

print("Loading complete!")
mainMenuRotation = [50, 180, True]

mainFunction = draw_main_menu

while True:
    pyglet.options['debug_gl'] = False
    pygame.display.set_caption(f"Minecraft {MC_VERSION} {clock.get_fps()}")
    if scene.allowEvents["keyboardAndMouse"] and not PAUSE:
        if pygame.mouse.get_pressed(3)[0]:
            player.mouseEvent(1)
    mbclicked = None
    keys = []

    for event in pygame.event.get():

        if event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_rel()
            player.rotation[0] += y
            player.rotation[1] += x
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            keys.append(event.key)
            if event.key == pygame.K_F11:
                if scene.WIDTH != monitor.current_w or scene.HEIGHT != monitor.current_h:
                    LAST_SAVED_RESOLUTION = [scene.WIDTH, scene.HEIGHT]

                    WIDTH = monitor.current_w
                    HEIGHT = monitor.current_h
                    screen = pygame.display.set_mode((monitor.current_w, monitor.current_h),
                                                     pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE
                                                     | pygame.FULLSCREEN, vsync=1)
                    scene.resizeCGL(WIDTH, HEIGHT)
                    resizeEvent = True
                else:
                    WIDTH = LAST_SAVED_RESOLUTION[0]
                    HEIGHT = LAST_SAVED_RESOLUTION[1]
                    screen = pygame.display.set_mode((WIDTH, HEIGHT),
                                                     pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE, vsync=1)
                    scene.resizeCGL(WIDTH, HEIGHT)
                    resizeEvent = True
        if event.type == pygame.VIDEORESIZE:
            WIDTH = event.w
            HEIGHT = event.h
            scene.resizeCGL(WIDTH, HEIGHT)
            resizeEvent = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mbclicked = event.button
        if not IN_MENU:
            if scene.allowEvents["keyboardAndMouse"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause()
                    if event.key == pygame.K_e:
                        player.inventory.showWindow()
                    if event.key == pygame.K_1:
                        player.inventory.activeInventory = 0
                    if event.key == pygame.K_2:
                        player.inventory.activeInventory = 1
                    if event.key == pygame.K_3:
                        player.inventory.activeInventory = 2
                    if event.key == pygame.K_4:
                        player.inventory.activeInventory = 3
                    if event.key == pygame.K_5:
                        player.inventory.activeInventory = 4
                    if event.key == pygame.K_6:
                        player.inventory.activeInventory = 5
                    if event.key == pygame.K_7:
                        player.inventory.activeInventory = 6
                    if event.key == pygame.K_8:
                        player.inventory.activeInventory = 7
                    if event.key == pygame.K_9:
                        player.inventory.activeInventory = 8
                    if event.key == pygame.K_F3:
                        showInfoLabel = not showInfoLabel
                    if event.key == pygame.K_t and not IN_MENU:
                        draw_command_function()
                    if event.key == pygame.K_F5:
                        player.cameraType += 1
                        if player.cameraType > 3:
                            player.cameraType = 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.mouseEvent(event.button)
                    if event.button == 4:
                        player.inventory.activeInventory -= 1
                        if player.inventory.activeInventory < 0:
                            player.inventory.activeInventory = 8
                        if player.inventory.inventory[player.inventory.activeInventory][1]:
                            gui.showText(player.inventory.inventory[player.inventory.activeInventory][0])
                    elif event.button == 5:
                        player.inventory.activeInventory += 1
                        if player.inventory.activeInventory > 8:
                            player.inventory.activeInventory = 0
                        if player.inventory.inventory[player.inventory.activeInventory][1]:
                            gui.showText(player.inventory.inventory[player.inventory.activeInventory][0])
                else:
                    if pygame.mouse.get_pressed(3)[0]:
                        player.mouseEvent(1)
                    else:
                        player.mouseEvent(-1)
            # clock.tick(MAX_FPS)
    if scene.allowEvents["grabMouse"]:
        pygame.mouse.set_visible(PAUSE)
    else:
        pygame.mouse.set_visible(True)

    if IN_MENU:
        mainFunction(mbclicked)

    if not PAUSE:
        sound.playMusic()

        if scene.allowEvents["showCrosshair"]:
            gui.shows["crosshair"][1] = (scene.WIDTH // 2 - 9, scene.HEIGHT // 2 - 9)
        else:
            gui.shows["crosshair"][1] = (-100, -100)
        if scene.allowEvents["grabMouse"] and pygame.mouse.get_focused():
            pygame.mouse.set_pos((scene.WIDTH // 2, scene.HEIGHT // 2))
        scene.updateScene()

        player.inventory.draw()
        gui.update()

        if showInfoLabel:
            drawInfoLabel(scene, f"Minecraft {MC_VERSION} ({MC_VERSION}/vanilla)\n"
                                 f"s fps\n"
                                 f"XYZ: {round(player.x(), 3)} / {round(player.y(), 5)} / {round(player.z(), 3)}\n"
                                 f"Block: {round(player.x())} / {round(player.y())} / {round(player.z())}\n"
                                 f"Facing: {player.rotation[1]} / {player.rotation[0]}\n"
                                 f"Biome: {getBiomeByTemp(scene.worldGen.perlinBiomes(player.x(), player.z()) * 3)}\n"
                                 f"Looking at: {scene.lookingAt}\n"
                                 f"Count of chunks: {scene.worldGen.start - len(scene.worldGen.queue)} "
                                 f"({scene.worldGen.start})",
                          shadow=False, label_color=(224, 224, 224), xx=3,yy=100)
        pygame.display.flip()
        # clock.tick(MAX_FPS)
    elif PAUSE and not IN_MENU:
        scene.allowEvents["movePlayer"] = False
        scene.allowEvents["keyboardAndMouse"] = False
        if scene.allowEvents["showCrosshair"]:
            gui.shows["crosshair"][1] = (scene.WIDTH // 2 - 9, scene.HEIGHT // 2 - 9)
        else:
            gui.shows["crosshair"][1] = (-100, -100)
        scene.updateScene()

        player.inventory.draw()
        gui.update()

        mainFunction(mbclicked)
        # clock.tick(MAX_FPS)
