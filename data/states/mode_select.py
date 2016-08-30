import pygame as pg
from .. import tools
from ..prepare import GFX, SCREEN_SIZE, FONTS, SFX
from ..components.animation import Animation, Task
from ..components.labels import Button,ButtonGroup,Label


class ModeSelect(tools._State):
    def __init__(self):
        super(ModeSelect, self).__init__()



    def startup(self, persist):
        self.persist = persist
        self.bg = GFX['bg']
        self.buttons = ButtonGroup()
        self.labels = pg.sprite.Group()
        self.number = 0
        midbottom = (SCREEN_SIZE[0] / 2, 200)
        label = Label('Difficulty', {"midbottom": midbottom}, self.labels, text_color='black', font_size= 90,
                      font_path=FONTS['ALGER'])
        Button((0, 0), self.buttons, button_size=(200, 100), idle_image=GFX['help'], \
               hover_image=GFX['help_hover'],hover_sound= SFX['choose'],call=self.get_number, args = 1)
        Button((400, 0), self.buttons, button_size=(200, 100), idle_image=GFX['custom'], \
               hover_image=GFX['custom_hover'], hover_sound= SFX['choose'],call=self.get_number, args=2)
        Button((0, 200), self.buttons, button_size=(600, 200), idle_image=GFX['easy'], \
               hover_image= GFX['easy_hover'], hover_sound= SFX['choose'],call=self.get_number, args=3)

        Button((0, 400), self.buttons, button_size=(600, 200), idle_image=GFX['normal'], \
               hover_image=GFX['normal_hover'],hover_sound= SFX['choose'], call=self.get_number, args=4)
        Button((0, 600), self.buttons, button_size=(600, 200), idle_image=GFX['hard'], \
               hover_image=GFX['hard_hover'],hover_sound= SFX['choose'],call=self.get_number, args=5)

    def get_number(self,number):
        self.number = number


    def get_event(self, event):
        self.buttons.get_event(event)
        if event.type == pg.MOUSEBUTTONUP:
            if self.number == 1:
                self.done = True
                self.next = 'HELP'

            elif self.number == 2:
                self.done = True
                self.next = 'CUSTOM'
            elif self.number in (3,4):
                self.done = True
                self.persist['d'] = self.number
                self.next = 'PLAY'
            elif self.number == 5:
                self.done = True
                self.persist['d'] = 4
                self.persist['hard'] = True
                self.next = 'PLAY'

    def draw(self,surface):
        surface.blit(self.bg,(0,0))
        self.labels.draw(surface)
        self.buttons.draw(surface)

    def update(self,dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)


    def cleanup(self):
        self.done = False
        return self.persist