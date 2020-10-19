import pygame as pg

from helpers import BackToMenu, FinishGame
from entity import ENTITY_T
from block import Block
from level import Level
import copy

FRAMERATE = 60

class Game():
    def __init__(self, level: Level):
        self.screen = pg.display.get_surface()
        self.sr_w, self.sr_h = self.screen.get_size()
        self.level = level.resize()
        self.blocks, self.objects, _, self.npc, self.players = map(
                pg.sprite.Group, self.level.get_sprites())
        self.clock = pg.time.Clock()
        self.bgr = pg.image.load(
            ENTITY_T.EMPTY.img_path).convert_alpha().get_at((0, 0))

    def play(self):
        while 42:
            self.__process_events()
            self.update()
            self.draw()

    def update(self):
        dt = self.clock.tick(FRAMERATE)
        collided_npc = pg.sprite.groupcollide(self.npc, self.blocks, False, False)
        for k, v in collided_npc.items():
            for v_ in v:
                r = v_.rect
                v_center_x = (r.x + r.w) / 2
                r = k.rect
                k_center_x = (r.x + r.w) / 2
                if (v_center_x - k_center_x) * k.velocity[0] > 0:
                    k.change_velocity((k.velocity[0] * -1, k.velocity[1]))
        self.npc.update(dt, move=True)
        self.players.update(dt, move=True)

    def draw(self):
        self.screen.fill(self.bgr)
        self.level.draw(self.screen)
        pg.display.update()

    def __process_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise FinishGame
            elif event.type == pg.KEYDOWN:
                if event.unicode == 'q':
                    raise BackToMenu
            for p in self.players:
                p.process_events(event)

    def __select(self, event):
        pass

    def __hover(self, event):
        pass
