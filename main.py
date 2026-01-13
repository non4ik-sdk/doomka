import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES, pg.NOFRAME, vsync=1)
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)

        self.fps_font = pg.font.SysFont('consolas', 26, bold=True)
        self.fps_color = pg.Color('white')
        self.fps_offset = 20  

        self.loading = False  
        self.new_game()

    def new_game(self):
        self.loading = True 
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        self.loading = False

    def update(self):

        if pg.mouse.get_visible() or not pg.event.get_grab():
            pg.mouse.set_visible(False)
            pg.event.set_grab(True)

        if not getattr(self, 'loading', False):
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()

        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

        if getattr(self, 'sound', None) and self.sound.music_loaded and not pg.mixer.music.get_busy():
            pg.mixer.music.play(-1)

    def draw(self):
        if not getattr(self, 'loading', False):
            self.object_renderer.draw()
            self.weapon.draw()

        fps_text = f"{self.clock.get_fps():.1f} FPS"
        fps_surf = self.fps_font.render(fps_text, True, self.fps_color)
        x = WIDTH - self.fps_offset - fps_surf.get_width()
        y = HEIGHT - self.fps_offset - fps_surf.get_height()
        self.screen.blit(fps_surf, (x, y))

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            if event.type == self.global_event:
                self.global_trigger = True

            if event.type in (pg.WINDOWFOCUSGAINED, pg.WINDOWENTER, pg.VIDEORESIZE):
                pg.mouse.set_visible(False)
                pg.event.set_grab(True)

            if not getattr(self, 'loading', False):
                self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    game.run()