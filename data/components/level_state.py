import random
import pygame as pg
from .animation import Animation, Task
from .labels import Blinker, Label
from ..prepare import SCREEN_SIZE, BOARD_RECT, GFX,FONTS,SFX


class State:
    def __init__(self, name, d, animations, labels):
        self.name = name
        self.d = d
        self.animations = animations
        self.labels = labels
        self.persist = {}

    def do_actions(self):
        pass

    def get_event(self,event):
        pass
    
    def check_conditions(self):
        pass

    def entry_actions(self, persist):
        self.persist = persist

    def exit_actions(self):
        return self.persist


class StateMachine:
    def __init__(self):

        self.states = {}
        self.active_state = None

    def add_state(self, state):

        self.states[state.name] = state

    def get_event(self,event):
        self.active_state.get_event(event)

    def check(self):

        if self.active_state is None:
            return

        self.active_state.do_actions()

        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name):

        if self.active_state is not None:
            persist = self.active_state.exit_actions()
        else:
            persist = {}


        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions(persist)

class PlayerSet(State):
    def __init__(self, d, board, animations, labels):
        super(PlayerSet,self).__init__('player_set',d, animations, labels)
        self.fragment_rect = None
        self.check_point = (60, 20)
        self.rect = None
        self.sprite_rect = None
        self.board = board

    def entry_actions(self, persist):
        midbottom = (SCREEN_SIZE[0]/2,SCREEN_SIZE[1]-20)
        frequency = 500
        prompt = Blinker("Click one tile to start", {"midbottom": midbottom},
                         frequency,text_color='black', font_size = 40,font_path = FONTS['ALGER'])
        task = Task(self.labels.add, args=(prompt,))
        self.animations.add(task)
        self.choose_sprite = None


    def check_conditions(self):
        if self.sprite_rect != None and self.sprite_rect.collidepoint(self.check_point):
            return 'computer_set'

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.sprite_rect = self.move_tile(*event.pos)
            self.persist['rect'] = self.rect


    def move_tile(self,x,y):
        for sprite in self.board.spritedict:
            if sprite.rect.collidepoint(x,y):
                self.rect = sprite.rect.copy()
                self.choose_sprite = sprite
                if self.d == 3:
                    self.choose_sprite.image =pg.transform.smoothscale(self.choose_sprite.image,(120,120))
                ani = Animation(x = 60, y = 20, duration = 100)
                ani.start(self.choose_sprite.rect)
                self.animations.add(ani)
                return sprite.rect

    def exit_actions(self):
        self.labels.empty()
        self.animations.empty()
        self.persist['rect']= self.rect
        self.persist['sprite'] = self.choose_sprite
        self.persist['board'] = self.board
        return self.persist

class ComputerSet(State):
    def __init__(self, d,animations, labels):
        super(ComputerSet,self).__init__('computer_set', d,animations, labels)
        self.shuffle = 100
        self.count = 0

    def entry_actions(self, persist):
        self.persist = persist
        self.board = self.persist['board']
        midbottom = (SCREEN_SIZE[0]/2,SCREEN_SIZE[1]-60)
        label = Label('Creating new puzzle   ',{"midbottom": midbottom}, self.labels, text_color='black', font_size = 40,font_path = FONTS['ALGER'])
        frequency0 = 300
        frequency1 = 600
        frequency2 = 1200      
        prompt0 = Blinker("                                            .  ", {"midbottom": midbottom},
                         frequency0, text_color='black', font_size = 40,font_path = FONTS['ALGER'])
        prompt1 = Blinker("                                            .. ", {"midbottom": midbottom},
                         frequency1,text_color='black', font_size = 40,font_path = FONTS['ALGER'])
        prompt2 = Blinker("                                            ...", {"midbottom": midbottom},
                         frequency2,text_color='black', font_size = 40,font_path = FONTS['ALGER'])
        task = Task(self.labels.add, args=(prompt0,prompt1,prompt2))
        self.animations.add(task)
        self.persist = persist
        self.rect = self.persist['rect'].copy()
        self.move_sprite = None
        self.loop = True
        self.move_offset = (0,0)


    def do_actions(self):
        center = self.rect.center
        if self.loop and self.count < self.shuffle:
            offset = random.choice([(480/self.d, 0),(-480/self.d, 0), (0, 480/self.d), (0, -480/self.d)])
            check_rect = self.rect.move(offset)
            check_rect.clamp_ip(BOARD_RECT)
            for sprite in self.board.spritedict:
                if check_rect.center == sprite.rect.center:
                    self.move_sprite = sprite
                    self.move_offset = offset
                    ani = Animation(x=self.rect.x, y=self.rect.y, duration = 100)
                    ani.start(sprite.rect)
                    self.animations.add(ani)
                    self.loop = False
                    break


        elif self.move_sprite != None and self.move_sprite.rect.center == center:
            self.rect.move_ip(self.move_offset)
            self.rect.clamp_ip(BOARD_RECT)
            self.count += 1
            self.move_sprite = None
            self.move_offset = (0,0)
            self.loop = True

    def check_conditions(self):
        if self.count >= self.shuffle:
            return 'player_play'

    def exit_actions(self):
        self.labels.empty()
        self.animations.empty()
        self.persist['rect'] = self.rect
        self.persist['board'] = self.board
        return self.persist

class PlayerPlay(State):
    def __init__(self, d, animations, labels):
        super(PlayerPlay,self).__init__('player_play',d, animations, labels)
        self.move = True
        self.collective_silde = False
        


    def entry_actions(self, persist):
        self.persist = persist
        self.rect = self.persist['rect'].copy()
        self.board = self.persist['board']
        self.move_offset = (0,0)
        self.check_group = self.board.copy()


    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            sound = SFX['move']
            if event.key in (pg.K_a, pg.K_LEFT):
                sound.play()
                self.move_offset = (480/self.d,0)

            elif event.key in (pg.K_d, pg.K_RIGHT):
                sound.play()
                self.move_offset = (-480/self.d,0)

            elif event.key in (pg.K_w, pg.K_UP):
                sound.play()
                self.move_offset = (0,480/self.d)

            elif event.key in (pg.K_s, pg.K_DOWN):
                sound.play()
                self.move_offset = (0,-480/self.d)

            elif event.key == pg.K_SPACE:
                self.collective_silde = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                self.collective_silde = False

    def do_actions(self):
        check_rect = self.rect.move(self.move_offset)
        check_rect.clamp_ip(BOARD_RECT)

        for sprite in self.check_group.spritedict:
            if check_rect.center == sprite.rect.center:
                a = self.rect.x
                b = self.rect.y
                sprite.rect.center = check_rect.center
                self.check_group.update()
                self.rect.move_ip(self.move_offset)
                self.rect.clamp_ip(BOARD_RECT)
                if not self.collective_silde:
                    self.move_offset = (0,0)
                for animation_sprite in self.board.spritedict:
                    if animation_sprite.id == sprite.id:
                        ani = Animation(x=a, y=b, duration=100)
                        ani.start(animation_sprite.rect)
                        self.animations.add(ani)


    def check_conditions(self):
        n= 0
        for sprite in self.board.spritedict:
            if (sprite.id // self.d * 480/self.d + 60, sprite.id % self.d * 480/self.d  + 160) == sprite.rect.topleft:
                n += 1
        if n == self.d * self.d -1:
            return 'game_over'

    def exit_actions(self):
        self.labels.empty()
        self.animations.empty()
        self.persist['rect'] = self.rect
        self.persist['board'] = self.board
        return self.persist


class GameOver(State):
    def __init__(self, d, animations, labels):
        super(GameOver, self).__init__('game_over',  d, animations, labels)


    def entry_actions(self, persist):
        self.persist = persist
        self.board = self.persist['board']
        self.moving_sprite = self.persist['sprite']
        self.rect = self.persist['rect'].copy()
        if self.d == 3:
            self.moving_sprite.image = pg.transform.smoothscale(self.moving_sprite.image,(160,160))
        ani = Animation(x=self.rect.x, y=self.rect.y, duration=100)
        ani.start(self.moving_sprite.rect)
        self.animations.add(ani)
        self.played = False

    def  check_conditions(self):
        n = 0
        for sprite in self.board.spritedict:
            if (sprite.id // self.d * 480 / self.d + 60,
                sprite.id % self.d * 480 / self.d + 160) == sprite.rect.topleft:
                n += 1
        if n == self.d * self.d and not self.played:
            sound = SFX['victory']
            sound.play()
            victory = pg.sprite.Sprite()
            victory.image = GFX['victory']
            victory.rect = pg.Rect(600,220,600,360)
            self.labels.add(victory)
            ani = Animation(x=0, y=220, duration=1000, transition="in_out_elastic")
            ani.start(victory.rect)
            victory.update()
            self.animations.add(ani)
            self.played = True


LEVEL_STATES={'player_set':PlayerSet,
              'computer_set':ComputerSet,
              'player_play':PlayerPlay,
              'game_over':GameOver}
