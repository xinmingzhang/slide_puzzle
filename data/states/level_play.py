import random
import pygame as pg

from .. import tools
from ..components.level_state import LEVEL_STATES, StateMachine
from ..prepare import  BOARD_RECT, GFX,CHARACTERS,game_font


class Tile(pg.sprite.Sprite):
    def __init__(self, image, rect, num, d, *groups):
        super(Tile, self).__init__(*groups)
        self.image = image
        self.rect = rect
        self.rect.move_ip(60,160)
        self.id = num
        self.pos_right = False
        pg.draw.rect(self.image,(255,0,0),(0,0,480/d,480/d),2)




class LevelPlay(tools._State):
    def __init__(self):
        super(LevelPlay, self).__init__()

    def startup(self, persist):
        self.persist = persist
        self.init()

    def init(self):
        self.bg = GFX['bg']
        self.labels = pg.sprite.Group()
        self.animations = pg.sprite.Group()
        self.board = pg.sprite.Group()
        self.state = StateMachine()
        try:
            self.character = self.persist['character']
            del self.persist['character']
        except:
            self.character = random.choice(list(CHARACTERS.keys()))

        self.surface = game_font.render(self.character,True,(0,0,0),(225,225,225,125))

        try:
            self.d = self.persist['d']
        except:
            self.d = 4
        n = 480/self.d
        for i in range(self.d):
            for j in range(self.d):
                rect = pg.Rect(i*n,j*n,n,n)
                Tile(self.surface.subsurface(rect), rect, i*self.d+j,self.d,self.board)

        try:
            self.hard_mode = self.persist['hard']
            del self.persist['hard']
            
        except:
            self.hard_mode = False

        player_set_state = LEVEL_STATES['player_set'](self.d, self.board, self.animations, self.labels)
        computer_set_state = LEVEL_STATES['computer_set'](self.d, self.animations, self.labels)
        player_play_state = LEVEL_STATES['player_play'](self.d, self.animations, self.labels)
        game_over_state = LEVEL_STATES['game_over'](self.d, self.animations, self.labels)

        self.state.add_state(player_set_state)
        self.state.add_state(computer_set_state)
        self.state.add_state(player_play_state)
        self.state.add_state(game_over_state)

        self.state.set_state('player_set')

    def get_event(self, event):
        self.state.get_event(event)
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                self.init()
            if event.key == pg.K_x:
                self.done = True
                self.next = 'MODE'
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            else:
                pass


    def update(self, dt):
        self.state.check()
        self.board.update()
        self.animations.update(dt)
        self.labels.update(dt)


    def draw(self, surface):
        surface.blit(self.bg,(0,0))
        self.board.draw(surface)
        pg.draw.rect(surface,(255,0,0),BOARD_RECT,3)
        self.labels.draw(surface)
        if self.hard_mode == True:
            for sprite in self.board.spritedict:               
                if (sprite.id // self.d * 480/self.d + 60, sprite.id % self.d * 480/self.d  + 160) != sprite.rect.topleft:
                    rect = sprite.rect.inflate(-2,-2)
                    pg.draw.rect(surface,(255,255,255),rect)
