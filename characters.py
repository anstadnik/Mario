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
    IDLE = enum.auto()

class Character(Entity):
    def __init__(self, pos: List[int], entity: ENTITY_T,
                 bl_size: Tuple[int, int] = None, xy: Tuple[int, int] = None):
        super().__init__(pos, entity, xy=xy)

        self.velocity = [0, 0]
        self._action = Action.IDLE
        self.n_img = 1
        self.looking_left = True
        self.alive = True

        self._images = {}
        if bl_size:
            self.init_sprite(bl_size, xy)


    def update(self, dt, alive=False):
        if not self.alive:
            return
        self.n_img += 1
        if self.n_img >= len(self._images[self._action]):
            if self._action == Action.DIE:
                self.alive = False
                self.n_img -= 1
                return
            elif self._action == Action.ATTACK:
                self.action = Action.WALK
            self.n_img = 0
        self._image = self._images[self._action][self.n_img]

        if alive:
            if self._action == Action.WALK:
                x = self.xy[0] + self.velocity[0] * dt * 0.1
                screen_w, _ = pg.display.get_surface().get_size()
                if not 0 < x < screen_w - self.ent_size[0]:
                    self.velocity[0] *= -1
                    x += 2 * self.velocity[0] * dt * 0.1
                    self.looking_left = self.velocity[0] < 0

                rect_x = self.rect.x
                offset = x - rect_x
                self.rect.move_ip(offset, 0)
                self.xy = x, self.xy[1]


    @property
    def image(self):
        image = super().image
        if self.looking_left:
            image = pg.transform.flip(image, True, False)
        return image

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action: Action):
        self.n_img = 0
        self._action = action



class NPC(Character):
    def __init__(self, pos: List[int], entity: ENTITY_T,
                 bl_size: Tuple[int, int] = None, xy: Tuple[int, int] = None,
                 n_img: int = 1):
        super().__init__(pos, entity, bl_size, xy)
        self.velocity = [0, 0]
        self.action = Action.IDLE

    def init_moving(self):
        r = random.randint(1, 2)
        self.velocity = [(-1) ** r, 0]
        self.looking_left = self.velocity[0] < 0
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
            for image_path in sorted(filenames):
                image = pg.image.load(image_path).convert_alpha()
                images.append(pg.transform.scale(image, self.ent_size))
            self._images[A] = images
        self._image = self._images[self._action][self.n_img] 
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
                    'ACTION', A.name.capitalize()))
            images = []
            for image_path in sorted(filenames):
                image = pg.image.load(image_path).convert_alpha()
                images.append(pg.transform.scale(image, self.ent_size))
            self._images[A] = images
        self._image = self._images[self._action][self.n_img] 
        self.rect = self._image.get_rect().move(*self.xy)
        return self

    def process_events(self, event):
        if not self.alive:
            return
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.velocity[0] = 1
                self.looking_left = False
                self.action = Action.WALK
            elif event.key == pg.K_LEFT:
                self.velocity[0] = -1
                self.looking_left = True
                self.action = Action.WALK
            elif event.key == pg.K_SPACE:
                self.velocity[0] = 0
                #  TODO: Fire a bullet <19-10-20, astadnik> #
                self.action = Action.ATTACK
        if event.type == pg.KEYUP:
            if event.key in (pg.K_RIGHT, pg.K_LEFT):
                self.velocity[0] = 0
                self.action = Action.IDLE
