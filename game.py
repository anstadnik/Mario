import pygame as pg
from menu_select import menu_select

from helpers import BackToMenu, FinishGame
from entity import ENTITY_T
from block import Block
from characters import Action
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
        for s in self.npc:
            s.init_moving()
        self.clock = pg.time.Clock()
        self.bgr = pg.image.load(
            ENTITY_T.EMPTY.img_path).convert_alpha().get_at((0, 0))

    def play(self):
        while 42:
            self.process_events()
            self.update()
            self.draw()
            for p in self.players.sprites():
                if not p.alive:
                    menu_select(['You lost'])
                    raise BackToMenu
            for p in self.npc.sprites():
                if p.alive:
                    break
            else:
                menu_select(['You won'])
                raise BackToMenu

    def update(self):
        dt = self.clock.tick(FRAMERATE)
        self.check_npc_direction()
        self.check_npc_attack()
        if self.players.sprites() and self.players.sprites()[0].action == Action.ATTACK:
            self.check_players_attack()
        self.npc.update(dt, alive=True)
        self.players.update(dt, alive=True)

    def check_npc_direction(self):
        collided_npc = pg.sprite.groupcollide(
            self.npc, self.blocks, False, False)
        for k, v in collided_npc.items():
            for v_ in v:
                r = v_.rect
                v_center_x = (r.x + r.w) / 2
                r = k.rect
                k_center_x = (r.x + r.w) / 2
                if (v_center_x - k_center_x) * k.velocity[0] > 0:
                    k.velocity = (k.velocity[0] * -1, k.velocity[1])
                    k.looking_left = k.velocity[0] < 0

    def check_npc_attack(self):
        attacking_npc = pg.sprite.groupcollide(
            self.npc, self.players, False, False)
        for k, v in attacking_npc.items():
            for v_ in v:
                if k.alive and v_.alive and v_.action != Action.DIE:
                    k.action = Action.ATTACK
                    v_.action = Action.DIE

    def check_players_attack(self):
        for p in self.players:
            if p.alive:
                for n in self.npc:
                    if n.alive and n.action != Action.DIE:
                        dist = p.xy[0] - n.xy[0]
                        if ((dist * (1 if p.looking_left else -1)) > 0
                                and abs(dist) < 100):
                            n.action = Action.DIE

    def draw(self):
        self.screen.fill(self.bgr)
        self.level.draw(self.screen)
        pg.display.update()

    def process_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise FinishGame
            elif event.type == pg.KEYDOWN:
                if event.unicode == 'q':
                    raise BackToMenu
            for p in self.players:
                p.process_events(event)
