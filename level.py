import enum
import os
import pickle
from copy import copy
from typing import Tuple

import pygame as pg

from block import Block
from entity import ENTITY_T
from entity_factory import entity_factory


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
            entity, layer = entity_factory([x, self.h-1], ENTITY_T.GRASS, (self.bl_h, self.bl_w))
            self.sprites.add(entity, layer=layer)
            print(entity.xy)

    def update(self, dt):
        self.sprites.update(dt)

    def draw(self, screen):
        self.sprites.draw(screen)

    def resize(self, screen_w: int = None, screen_h: int = None):
        w, h = pg.display.get_surface().get_size()
        screen_w, screen_h = screen_w or w, screen_h or h,
        print(screen_w, screen_h)
        self.bl_w, self.bl_h = screen_w // self.w, screen_h // self.h
        print(self.bl_w, self.bl_h, self.w, self.h)
        new_sprites = pg.sprite.LayeredUpdates()
        for b in self.sprites.sprites():
            entity, layer = entity_factory(b.pos, b.entity, (self.bl_h, self.bl_w))
            new_sprites.add(entity, layer=layer)
            # __import__('ipdb').set_trace()
        self.sprites = new_sprites
        return self

    def add_sprite(self, pos: Tuple[int, int], entity_type: ENTITY_T):
        pos = pos[0] // self.bl_w, pos[1] // self.bl_h
        entity, layer = entity_factory(pos, entity_type, (self.bl_h, self.bl_w))
        self.sprites.add(entity, layer=layer)

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
