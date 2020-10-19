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

class Character(Entity):
    def __init__(self, pos: List[int], entity: ENTITY_T,
                 bl_size: Tuple[int, int] = None, xy: Tuple[int, int] = None,
                 n_img: int = 1):
        super().__init__(pos, entity, xy=xy)

        self.velocity = (0, 0)
        self.action = Action.IDLE
        self.n_img = n_img
        self.flip = False

        self._images = {}
        if bl_size:
            self.init_sprite(bl_size, xy)


    def update(self, dt, move=False):
        self.n_img += 1
        self.n_img = self.n_img if self.n_img < len(self._images[self.action]) else 0
        self._image = self._images[self.action][self.n_img]

        if move:
            x = self.xy[0] + self.velocity[0] * dt * 0.1
            # screen_w, _ = pg.display.get_surface().get_size()
            # if not 0 < x < screen_w - self.ent_size[0]:
            #     self.velocity[0] *= -1
            #     x += 2 * self.velocity[0] * dt * 0.1
            #     self.flip = self.velocity[0] < 0

            rect_x = self.rect.x
            offset = x - rect_x
            self.rect.move_ip(offset, 0)
            self.xy = x, self.xy[1]

    def change_velocity(self, new_velocity):
        self.velocity = new_velocity
        self.flip = self.velocity[0] < 0


class NPC(Character):
    def __init__(self, pos: List[int], entity: ENTITY_T,
                 bl_size: Tuple[int, int] = None, xy: Tuple[int, int] = None,
                 n_img: int = 1):
        super().__init__(pos, entity, bl_size, xy)
        r = random.randint(1, 2)
        self.velocity = [(-1) ** r, 0]
        self.flip = self.velocity[0] < 0
        self.action = Action.WALK

    def init_image(self, n_skin: int = None):
        if n_skin is None:
            n_skin = random.randint(1, 10)
        for A in Action:
            filenames = glob(
                self.entity.img_path.replace(
                    'N_SKIN', str(n_skin)).replace(
                    'ACTION', A.name.lower()))
            images = []
            if not filenames:
                print(self.entity, A.name)
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

    def process_events(self, event):
        pass
