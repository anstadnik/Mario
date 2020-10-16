import enum
import pygame as pg
from entity import Entity, ENTITY_T
from typing import Tuple, List
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
    def __init__(self, pos: List[int], entity: ENTITY_T,
                 bl_size: Tuple[int, int] = None, xy: Tuple[int, int] = None,
                 n_img: int = 1):
        super().__init__(pos, entity, xy=xy)

        self.velocity = [0, 0]
        self.action = Action.IDLE
        self.n_img = n_img

        self._images = {}
        if bl_size:
            self.init_sprite(bl_size, xy)

    def update(self, dt):
        screen_size = pg.display.get_surface().get_size()
        def constrain(n, nmax): return max(min(n, nmax), 0)
        border = [screen_size[i]-self.ent_size[i] for i in range(2)]
        xy = [constrain(self.xy[i] + self.velocity[i] * dt, border[i])
                for i in range(2)]
        offset = [self.xy[i] - xy[i] for i in range(2)]
        self.xy = xy
        self.rect.move_ip(*offset)

        self.n_img += 1
        self.n_img = self.n_img if self.n_img < len(self._images[self.action]) else 0
        self._image = self._images[self.action][self.n_img]


class NPC(Character):
    def __init__(self, pos: List[int], entity: ENTITY_T,
                 bl_size: Tuple[int, int] = None, xy: Tuple[int, int] = None,
                 n_img: int = 1):
        super().__init__(pos, entity, bl_size, xy)

    def init_image(self, n_skin: int = None):
        if n_skin is None:
            n_skin = random.randint(1, 10)
        for A in Action:
            filenames = glob(
                self.entity.img_path.replace(
                    'N_SKIN', str(n_skin)).replace(
                    'ACTION', self.action.name.lower()))
            images = []
            for image_path in sorted(filenames):
                image = pg.image.load(image_path).convert_alpha()
                images.append(pg.transform.scale(image, self.ent_size))
            self._images[A] = images
        self._image = self._images[self.action][self.n_img] 
        self.rect = self._image.get_rect().move(*self.xy)
        return self


class Player(Character, pg.sprite.Sprite):
    def init_image(self, n_skin: int = None):
        if n_skin is None:
            n_skin = random.randint(1, 3)
        for A in Action:
            filenames = glob(
                self.entity.img_path.replace(
                    'N_SKIN', str(n_skin)).replace(
                    'ACTION', self.action.name.capitalize()))
            images = []
            for image_path in sorted(filenames):
                image = pg.image.load(image_path).convert_alpha()
                images.append(pg.transform.scale(image, self.ent_size))
            self._images[A] = images
        self._image = self._images[self.action][self.n_img] 
        self.rect = self._image.get_rect().move(*self.xy)
        return self
