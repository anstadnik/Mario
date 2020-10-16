from entity import Entity, ENTITY_T
import pygame as pg
from typing import Tuple


class Block(Entity):
    def __init__(self, pos: Tuple[int, int], entity: ENTITY_T,
            bl_size: Tuple[int, int] = None, xy: Tuple[int, int] = None):
        super().__init__(pos, entity, bl_size, xy)

    def init_image(self):
        image = pg.image.load(self.entity.img_path).convert_alpha()
        self._image = pg.transform.scale(image, self.ent_size)
        self.rect = image.get_rect().move(*self.xy)
        return self
