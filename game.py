import pygame as pg

from helpers import BackToMenu, FinishGame
from entity import ENTITY_T
from block import Block
from level import Level


class Game():
    def __init__(self, level: Level):
        self.screen = pg.display.get_surface()
        self.sr_w, self.sr_h = self.screen.get_size()
        self.level = level.resize()
        self.clock = pg.time.Clock()
        self.bgr = pg.image.load(
            ENTITY_T.EMPTY.image_path).convert_alpha().get_at((0, 0))

    def play(self):
        while 42:
            self.__process_events()
            self.draw()

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
                    # raise BackToMenu
                    raise FinishGame
            elif event.type == pg.MOUSEMOTION:
                self.__hover(event)
            elif event.type == pg.MOUSEBUTTONUP:
                self.__select(event)

    def __select(self, event):
        pass

    def __hover(self, event):
        pass
