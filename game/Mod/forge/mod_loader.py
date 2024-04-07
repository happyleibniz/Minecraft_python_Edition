class ModLoader:
    def __init__(self, gl=None, sound=None, settings=None, player=None, gui=None, gc=None):
        self.gl = gl  # It should be the scene class
        self.sound = sound  # It should be all the sounds (game/sound/Sound.py)
        self.settings = settings  # It should be all the settings
        self.player = player
        self.gui = gui
        self.garbage_collector = gc
        print("initialized mod loader")

    def try_better(self):
        self.settings.MAX_FPS = 200
        self.settings.RENDER_DISTANCE = 16
        self.garbage_collector.collect()
