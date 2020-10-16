import pygame as pg

from helpers import BackToMenu, FinishGame
from level import Level
from entity import ENTITY_T
from block import Block
from entity_factory import entity_factory
from ipdb import launch_ipdb_on_exception

FRAMERATE = 30

class ReturnLevel(Exception):
    pass


class Lvl_editor:
    def __init__(self, level: Level):
        self.screen = pg.display.get_surface()
        self.sr_w, self.sr_h = self.screen.get_size()
        palette_size = self.sr_w // (level.w + 1)
        self.level = level.resize(screen_w = self.sr_w - palette_size)
        self.clock = pg.time.Clock()
        self.bgr = pg.image.load(
            ENTITY_T.EMPTY.img_path).convert_alpha().get_at((0, 0))

        # Set up palette
        self.palette = pg.sprite.LayeredUpdates()
        bl_h, bl_w = level.bl_h, level.bl_w
        for y, entity in enumerate(ENTITY_T):
            entity, layer = entity_factory([0, y], entity, (bl_h, bl_w),
                    (self.sr_w-palette_size, y*bl_h))
            self.palette.add(entity, layer=layer)

        self.brush = ENTITY_T.EMPTY

    def edit(self):
        try:
            while 42:
                self.__process_events()
                self.update()
                self.draw()
        except ReturnLevel:
            return self.level

    def update(self):
        dt = self.clock.tick(FRAMERATE)
        self.level.update(dt)
        self.palette.update(dt)

    def draw(self):
        self.screen.fill(self.bgr)
        self.level.draw(self.screen)
        self.palette.draw(self.screen)
        pg.display.update()

    def __process_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise FinishGame
            elif event.type == pg.KEYDOWN:
                if event.unicode == 'q':
                    raise BackToMenu
                if event.unicode == 's':
                    # import pudb; pudb.set_trace()
                    self.level.save()
                    raise ReturnLevel
            elif event.type == pg.MOUSEMOTION:
                self.__hover(event)
            elif event.type == pg.MOUSEBUTTONUP:
                self.__select(event)

    def __select(self, event):
        hov = self.check_at_pos(event.pos)
        if event.button == 1:  # Left
            if event.pos[0] >= self.sr_w - 50:
                if hov in self.palette:
                    self.brush = hov.entity
            else:
                if hov in self.level.sprites:
                    hov.kill()
                self.level.add_sprite(event.pos, self.brush)
        elif event.button == 2:  # Middle
            pass
        elif event.button == 3:  # Right
            if hov in self.level.sprites:
                hov.kill()

    def __hover(self, event):
        hov = self.check_at_pos(event.pos)
        if hov in self.palette:
            pg.mouse.set_cursor(*pg.cursors.diamond)
        elif not hov:
            pg.mouse.set_cursor(*pg.cursors.arrow)

    def check_at_pos(self, pos) -> Block:
        for g in [self.level.sprites, self.palette]:
            sprites = g.get_sprites_at(pos)
            top_sprite, top_lvl = None, None
            for s in sprites:
                if not top_sprite or g.get_layer_of_sprite(s) > top_lvl:
                    top_sprite, top_lvl = s, g.get_layer_of_sprite(s)
            if top_sprite:
                return top_sprite
        return top_sprite
