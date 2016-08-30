import pygame as pg
from .. import tools
from ..prepare import GFX, SCREEN_RECT, FONTS, SFX,game_font,BOARD_RECT
from ..components.animation import Animation, Task
from ..components.labels import Label,TextBox,Blinker


class Custom(tools._State):
    def __init__(self):
        super(Custom, self).__init__()
        self.make_textbox()
        self.bg = GFX['bg']
        self.labels = pg.sprite.Group()
        self.animations = pg.sprite.Group()
        self.ascii_surface = pg.Surface((480,480)).convert_alpha()
        self.ascii_surface.fill((0,0,0,125))
        midbottom = (SCREEN_RECT.centerx, 80)
        label = Label('Accepts UCS-2 character', {"midbottom": midbottom}, \
                      self.labels, text_color='black', font_size=35,font_path=FONTS['ALGER'])

        prompt = Blinker("0001 to FFFF", {"midtop": (SCREEN_RECT.centerx, 100)},
                         500, text_color='black', font_size= 35, font_path=FONTS['ALGER'])

        task = Task(self.labels.add, args=(prompt,))
        self.animations.add(task)


    def startup(self, persist):
        self.persist = persist
        self.make_textbox()
        self.bg = GFX['bg']
        self.labels = pg.sprite.Group()
        self.animations = pg.sprite.Group()
        self.ascii_surface = pg.Surface((480,480)).convert_alpha()
        self.ascii_surface.fill((0,0,0,125))
        midbottom = (SCREEN_RECT.centerx, 80)
        label = Label('Accepts UCS-2 character', {"midbottom": midbottom}, \
                      self.labels, text_color='black', font_size=35,font_path=FONTS['ALGER'])

        prompt = Blinker("0001 to FFFF", {"midtop": (SCREEN_RECT.centerx, 100)},
                         500, text_color='black', font_size= 35, font_path=FONTS['ALGER'])

        task = Task(self.labels.add, args=(prompt,))
        self.animations.add(task)

    def make_textbox(self):
        self.textbox_rect = pg.Rect(0, 0, 200, 80)
        self.textbox_rect.midtop = (SCREEN_RECT.centerx, 680)
        self.textbox_style = {
            "color": (255,255,255),
            "font": pg.font.Font(FONTS['ALGER'],50),
            "font_color": pg.Color(0, 0, 0),
            "active_color": (255,255,255,125),
            "outline_color": (255,0,0),
            "click_sounds": [SFX["key{}".format(x)] for x in range(1, 7)]}
        self.textbox = TextBox(self.textbox_rect, **self.textbox_style)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_x:
                self.done = True
                self.next = 'MODE'
            elif event.key == pg.K_r:
                try:
                    self.persist['character'] = self.ascii
                except:
                    pass
                self.done = True
                self.next = 'PLAY'
        self.textbox.get_event(event, pg.mouse.get_pos())


    def draw(self,surface):
        surface.blit(self.bg,(0,0))
        surface.blit(self.ascii_surface,BOARD_RECT)
        pg.draw.rect(surface, (255, 0, 0), BOARD_RECT, 3)
        self.textbox.draw(surface)
        self.labels.draw(surface)

    def update(self, dt):
        self.textbox.update()
        self.labels.update(dt)
        self.animations.update(dt)
        if len(self.textbox.buffer)==4:
            self.textbox.active = False
        if not self.textbox.active:
            try:
                self.ascii = chr(int(eval('0x'+self.textbox.final)))
            except:
                pass
            self.textbox.buffer = []
            self.textbox.active = True
            try:
                self.ascii_surface = game_font.render(self.ascii, True, (0, 0, 0), (225, 225, 225, 125))
            except:
                pass
