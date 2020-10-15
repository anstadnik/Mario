import pygame as pg

from helpers import BackToMenu, FinishGame
from level import Level
from entity import Entity_T
from block import Block


class ReturnLevel(Exception):
    pass


class Lvl_editor:
    def __init__(self, level: Level):
        self.screen = pg.display.get_surface()
        self.sr_w, self.sr_h = self.screen.get_size()
        self.level = level.resize(screen_w = self.sr_w - 50)
        self.bgr = pg.image.load(
            Entity_T.EMPTY.image_path).convert_alpha().get_at((0, 0))

        # Set up palette
        self.palette = pg.sprite.LayeredUpdates()
        bl_h, bl_w = level.bl_h, level.bl_w
        for y, entity in enumerate(Entity_T):
            self.palette.add(
                Block((0, y), entity, (bl_h, bl_w), xy=(self.sr_w-50, y*bl_h)), layer=2)

        self.brush = Entity_T.EMPTY
        self.prev_hov = None

    def edit(self):
        try:
            while 42:
                self.__process_events()
                self.draw()
        except ReturnLevel:
            return self.level

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
        if hov and hov != self.prev_hov:
            if hov in self.palette:
                pg.mouse.set_cursor(*pg.cursors.diamond)
            hov.recolor(pg.Color(100, 100, 100))
        if hov != self.prev_hov:
            if self.prev_hov:
                self.prev_hov.recolor(pg.Color(0, 0, 0))
            self.prev_hov = hov
        if not hov:
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
