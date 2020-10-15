import enum
import pickle
from copy import copy

import pygame as pg
from typing import Tuple

from entity import Entity_T
from block import Block
import os


class Level():
    def __init__(self, name, h=10, w=20, field=None):
        self.h = h
        self.w = w
        self.name = name

        # Init sprites
        self.sprites = pg.sprite.LayeredUpdates()

        screen_w, screen_h  = pg.display.get_surface().get_size()
        self.bl_h, self.bl_w = screen_h // self.h, screen_w // self.w
        for x in range(self.w):
            b = Block((x, self.h-1), Entity_T.GRASS)
            self.sprites.add(b.init_sprite((self.bl_h, self.bl_w)),
                    layer=b.entity.layer)

    def draw(self, screen):
        self.sprites.draw(screen)

    def resize(self, screen_w: int = None, screen_h: int = None):
        w, h = pg.display.get_surface().get_size()
        screen_w, screen_h = screen_w or w, screen_h or h,
        self.bl_h, self.bl_w = screen_h // self.h, screen_w // self.w
        new_sprites = pg.sprite.LayeredUpdates()
        for b in self.sprites.sprites():
            new_b = Block(b.pos, b.entity, bl_size=(self.bl_h, self.bl_w))
            new_sprites.add(new_b.init_sprite((self.bl_h, self.bl_w)),
                    layer=b.entity.layer)
        self.sprites = new_sprites
        return self


    def add_sprite(self, pos: Tuple[int, int], entity_type: Entity_T):
        pos = pos[0] // self.bl_w, pos[1] // self.bl_h
        b = Block(pos, entity_type, (self.bl_h, self.bl_w))
        self.sprites.add(b, layer=entity_type.layer)

    # def delete_sprite(self, sprite):

    #############
    #  Dumping  #
    #############

    @classmethod
    def load(cls, filename: str):
        with open(filename, 'rb') as f:
            level = pickle.load(f)
        screen_w, screen_h  = pg.display.get_surface().get_size()
        level.bl_h, level.bl_w = screen_h // level.h, screen_w // level.w
        new_sprites = pg.sprite.LayeredUpdates()
        for pos, entity in level.sprites:
            new_b = Block(pos, entity, bl_size=(level.bl_h, level.bl_w))
            new_sprites.add(new_b.init_sprite((level.bl_h, level.bl_w)),
                    layer=entity.layer)
        level.sprites = new_sprites
        return level

    def save(self):
        self.bl_w = None
        self.bl_h = None
        cleaned = copy(self)
        sprites = []
        for b in cleaned.sprites.sprites():
            sprites.append((b.pos, b.entity))
        cleaned.sprites = sprites
        with open(os.path.join('./levels', self.name + '.pickle'), 'wb') as f:
            pickle.dump(cleaned, f)
