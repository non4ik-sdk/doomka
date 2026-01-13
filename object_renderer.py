import pygame as pg
from settings import *
from utils import resource_path
from concurrent.futures import ThreadPoolExecutor

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.wall_textures = self.load_wall_textures_threading()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0

        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.blood_alpha = 0
        self.blood_fade_speed = 3

        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

        # --- ASCII health bar settings
        self.max_health = self.game.player.health
        self.bar_length = 45
        self.char_width = 10   
        self.char_height = 28  
        self.char_spacing = 1   
        self.health_color = pg.Color(220, 60, 60) 
        self.lost_color = pg.Color(60, 60, 60)    

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health_bar()
        self.draw_blood_effect()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health_bar(self):
        health = max(0, self.game.player.health)
        filled = int((health / self.max_health) * self.bar_length)
        empty = self.bar_length - filled

        x = 20
        y = HEIGHT - 20 - self.char_height 

        for i in range(filled):
            pg.draw.rect(self.screen, self.health_color, (x, y, self.char_width, self.char_height))
            x += self.char_width + self.char_spacing

        for i in range(empty):
            pg.draw.rect(self.screen, self.lost_color, (x, y, self.char_width, self.char_height))
            x += self.char_width + self.char_spacing

    def player_damage(self):
        self.blood_alpha = 180

    def draw_blood_effect(self):
        if self.blood_alpha > 0:
            self.blood_alpha = max(0, self.blood_alpha - self.blood_fade_speed)
            self.blood_screen.set_alpha(self.blood_alpha)
            self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        objects = sorted(
            self.game.raycasting.objects_to_render,
            key=lambda t: t[0],
            reverse=True
        )
        for depth, image, pos in objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        full_path = resource_path(path)
        texture = pg.image.load(full_path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures_threading(self):
        paths = {
            1: 'resources/textures/1.png',
            2: 'resources/textures/2.png',
            3: 'resources/textures/3.png',
            4: 'resources/textures/4.png',
            5: 'resources/textures/5.png',
        }

        textures = {}

        def load_item(key_path):
            key, path = key_path
            return key, self.get_texture(path)

        with ThreadPoolExecutor(max_workers=len(paths)) as executor:
            for key, texture in executor.map(load_item, paths.items()):
                textures[key] = texture

        return textures