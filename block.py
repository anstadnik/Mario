from entity import Entity, Entity_T
import pygame as pg
from typing import Tuple


class Block(Entity):
    def __init__(self, pos: Tuple[int, int], entity: Entity_T,
            bl_size: Tuple[int, int] = None, xy: Tuple[int, int] = None):
        super().__init__(pos, entity, bl_size, xy)

    def recolor(self, color):
        self.image = self.orig_image.copy()
        self.image.fill(color, special_flags=pg.BLEND_ADD)

    def init_image(self):
        image = pg.image.load(self.entity.image_path).convert_alpha()
        self.image = pg.transform.scale(image, (self.ent_w, self.ent_h))
        self.orig_image = self.image.copy()
        self.rect = image.get_rect().move(self.x, self.y)
        return self

    def clean_sprite(self):
        self.orig_image = None
        self.image = None
        self.rect = None
