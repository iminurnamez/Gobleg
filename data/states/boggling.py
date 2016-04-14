from random import choice

import pygame as pg

from .. import tools, prepare
from ..components.board import BoggleBoard, SET2
from ..components.labels import TextBox
from ..components.hourglass import Hourglass



class Boggling(tools._State):
    def __init__(self):
        super(Boggling, self).__init__()
        self.new_round()
        self.start_color = (61, 64, 255)
        self.final_color = (30, 144, 255)
        self.round_length = 180000
        
        
    def new_round(self):
        self.board = BoggleBoard((384, 70), SET2)
        self.make_textbox()
        self.hourglass = Hourglass((950, 175))
        self.color_time= 0
        
    def startup(self, persist):
        self.persistent = persist
        self.new_round()
        x = choice(("a", "b"))
        song = prepare.MUSIC["puzzle-1-{}".format(x)]
        pg.mixer.music.load(song)
        pg.mixer.music.play(-1)
        
    def make_textbox(self):
        self.textbox_rect = pg.Rect(0, 0, 600, 120)
        self.textbox_rect.midtop = (prepare.SCREEN_RECT.centerx, 600)                
        font = pg.font.Font(prepare.FONTS["weblysleekuisb"], 80)
        click_sounds = [prepare.SFX["key{}".format(x)] for x in range(1, 7)]
        self.textbox_style = {                    
                "color": None,
                "font": font,
                "font_color": pg.Color(255, 204, 0),
                "active_color": None,
                "outline_color": None,
                "click_sounds": click_sounds}
        self.textbox = TextBox(self.textbox_rect, **self.textbox_style)    
              
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        self.textbox.get_event(event, pg.mouse.get_pos())
        
    def update(self, dt):
        self.color_time += dt
        self.textbox.update()
        if not self.textbox.active:
            word = self.textbox.final
            self.textbox.buffer = []
            self.textbox.active = True
            self.board.check_word(word)
        self.hourglass.update(dt)
        if self.hourglass.done:
            self.done = True
            self.next = "TIMEUP"
            pg.mixer.music.fadeout(5000)
            self.persist["board"] = self.board
        lerp_val = min(1, self.color_time / float(self.round_length))
        self.color = tools.lerp(self.start_color, self.final_color,
                                         lerp_val)
            
    def draw(self, surface):
        surface.fill(self.color)
        self.board.draw(surface)
        self.textbox.draw(surface)
        self.hourglass.draw(surface)
    