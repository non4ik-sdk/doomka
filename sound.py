import pygame as pg
from concurrent.futures import ThreadPoolExecutor
from utils import resource_path

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()

        self.path = 'resources/sound/'
        self.loaded = False
        self.music_loaded = False

        self.shotgun = None
        self.npc_pain = None
        self.npc_death = None
        self.npc_shot = None
        self.player_pain = None

        from threading import Thread
        Thread(target=self._load_sounds, daemon=True).start()

    def _load_sounds(self):
        sound_files = {
            'shotgun': 'shotgun.wav',
            'npc_pain': 'npc_pain.wav',
            'npc_death': 'npc_death.wav',
            'npc_shot': 'npc_attack.wav',
            'player_pain': 'player_pain.wav'
        }

        def load_sound(item):
            key, filename = item
            sound = pg.mixer.Sound(resource_path(self.path + filename))
            if key == 'npc_shot':
                sound.set_volume(0.05)
            return key, sound

        with ThreadPoolExecutor(max_workers=len(sound_files)) as executor:
            for key, sound in executor.map(load_sound, sound_files.items()):
                setattr(self, key, sound)

        # музыка загружается отдельно
        pg.mixer.music.load(resource_path(self.path + 'theme.mp3'))
        pg.mixer.music.set_volume(0.05)
        self.music_loaded = True

        self.loaded = True
