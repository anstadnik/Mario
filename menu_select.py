import pygame as pg
from pygame.freetype import SysFont
from helpers import FinishGame
from entity import Entity_T
pg.init()


class Button(pg.sprite.Sprite):
    def __init__(self, h, w, x, y, color, text, font):
        super().__init__()
        self.image = pg.Surface([w, h])
        self.rect = self.image.get_rect().move(x, y)
        self.text = text
        self.text_rend = font.render(text, True, pg.Color('black'))
        self.color = None

        self.recolor(color)

    def recolor(self, color):
        if color != self.color:
            self.color = color
            self.image.fill(color)

            self.image.blit(self.text_rend, self.text_rend.get_rect(center=(
                self.image.get_width() // 2, self.image.get_height() // 2)))


def menu_select(texts):
    screen = pg.display.get_surface()
    font = pg.font.SysFont('jetbrainsmonoextraboldnerdfont', 20)
    background = pg.image.load(Entity_T.EMPTY.image_path).convert_alpha()
    background = background.get_at((0, 0))

    screen_width, screen_height = screen.get_size()
    w, h = screen_width-50, (screen_height-50)//len(texts)

    ys = range(25, 25+h*(len(texts)-1)+1, h)
    buttons = [Button(h-20, w, 25, y, pg.Color('white'), text, font)
               for y, text in zip(ys, texts)]
    buttons = pg.sprite.Group(*buttons)

    while 42:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise FinishGame

            elif event.type == pg.KEYDOWN:
                if event.unicode == 'q':
                    raise FinishGame

            elif event.type == pg.MOUSEMOTION:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        button.recolor(pg.Color('blue'))
                    else:
                        button.recolor(pg.Color('white'))

            elif event.type == pg.MOUSEBUTTONUP:
                clicked = [
                    s for s in buttons if s.rect.collidepoint(event.pos)]
                if not len(clicked):
                    continue

                assert len(clicked) == 1
                s = clicked[0]

                if event.button == 1:  # Left
                    return s.text
                # elif event.button == 2:  # Middle
                #     pass
                # elif event.button == 3:  # Right
                #     pass

            screen.fill(background)
            buttons.draw(screen)
            pg.display.update()
