import os
import pickle
from enum import Enum
from game import Game

import pygame as pg

from helpers import BackToMenu, FinishGame
from level import Level
from level_editor import Lvl_editor
from menu_select import menu_select


class Menu():
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.levels = {}
        screen = pg.display.set_mode((self.width, self.height))
        self.load_lvls()

    def run(self):
        try:
            self.loop()
        except FinishGame:
            pass
        pg.display.quit()

    def loop(self):
        while 42:
            try:
                ret = start_screen()
                # ret = 'Play'
                ret = 'Level editor'

                if ret == 'Play':
                    # level = self.pick_lvl()
                    level = list(self.levels.values())[0]
                    Game(level).play()
                elif ret == 'Level editor':
                    level = self.pick_lvl(add_new=True)
                    # level = Level('Custom_lvl_1')
                    level = Lvl_editor(level).edit()
                    self.levels[level.name] = level
                else:
                    break
            except BackToMenu:
                pass

    def load_lvls(self, path='levels'):
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.isdir(path):
            raise RuntimeError('Wrong path provided, it should be a directory')
        _, _, files = next(os.walk(path))
        for f in files:
            try:
                level = Level.load(os.path.join(path, f))
                self.levels[level.name] = level
            except (ValueError, ModuleNotFoundError, EOFError):
                pass


    def pick_lvl(self, add_new=False):
        names = list(self.levels.keys())
        if add_new:
            names.append('Create level')
        name = menu_select(names)
        if name == 'Create level':
            i = 1
            while (lvl_name := f'Custom_lvl_{i}') in names:
                i += 1
            return Level(lvl_name)
        for l in self.levels.values():
            if l.name == name:
                return l


def start_screen():
    texts = ['Play', 'Level editor', 'Quit']
    return menu_select(texts)
