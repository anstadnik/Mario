import enum
import pygame as pg
from entity import Entity, Entity_T
from typing import Tuple
from glob import glob
import random

class Action(enum.Enum):
    WALK = enum.auto()
    ATTACK = enum.auto()
    DIE = enum.auto()
    HURT = enum.auto()
    IDLE = enum.auto()

    CASTING_SPELLS = enum.auto()
    IDLE_BLINK = enum.auto()

class Character(Entity):
    def __init__(self, pos, action_imgs):
        super().__init__()

        self.i = 0
        self.velocity = (0, 0)
        self.action = Action.IDLE

    def update(self, dt):
        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt
        screen_w, screen_h  = pg.display.get_surface().get_size()
        constrain = lambda n, nmax: max(min(n, nmax), 0)
        self.pos[0] = constrain(self.pos[0], screen_w-self.bl_w)
        self.pos[1] = constrain(self.pos[1], screen_h-self.bl_h)
        self.rect.move_ip(self.pos)

        self.i = self.i if self.im_id < len(self.images[self.action]) else 0
        self.image = self.images[self.action][i]

class NPC(Character, pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], entity: BL_T, action: Action, 
            bl_size: Tuple[int, int] = None, xy: Tuple[int, int] = None):
        super().__init__(pos, entity, bl_size, xy)

        self.images = {}
        if bl_size:
            self.init_sprite(bl_size, xy)

    def recolor(self, color):
        self.image = self.orig_image.copy()
        self.image.fill(color, special_flags=pg.BLEND_ADD)

    def init_image(self, tp: int = None):
        if tp is None:
            tp = random.randint(10) + 1
        for A in Action:
            filenames = glob(f'*{A.name.lower()}*.png')
            images = []
            for i in filenames:
                image = pg.image.load(self.entity.image_path).convert_alpha()
                images.append(pg.transform.scale(image, (self.ent_w,
                    self.ent_h)))
            self.images[A] = images
        self.rect = images[0].get_rect()
        return self
