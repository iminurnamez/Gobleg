import pygame as pg

from .. import prepare
from ..components.animation import Animation, Task


class Hourglass(object):
    def __init__(self, topleft):
        self.done = False
        self.topleft = topleft
        self.top_sand = prepare.GFX["sand-top"]
        self.bottom_sand = prepare.GFX["sand-bottom"]
        self.stream = prepare.GFX["sand-stream"]
        self.top_height = self.top_sand.get_height()
        self.bottom_height = 0
        self.stream_height = 0
        self.top_top = 77
        self.bottom_top = 273
        self.stream_top = 153
        self.stream_height = 0
        self.glass = prepare.GFX["glass"]
        self.image = pg.Surface(self.glass.get_size()).convert_alpha()
        self.animations = pg.sprite.Group()
        self.start_clock(180000)
        
    def start_clock(self, timespan):
        ani = Animation(stream_height=120, duration=100,
                                transition="linear", round_values=True)
        ani2 = Animation(bottom_top=205, duration=timespan,
                                  transition="out_cubic", round_values=True)
        ani3 = Animation(top_height=0, duration=timespan,
                                  transition="in_cubic", round_values=True)
        ani4 = Animation(top_top=154, duration=timespan,
                                  transition="in_cubic", round_values=True)
        ani5 = Animation(stream_top=205, duration=1000,
                                  delay=timespan-1000, transition="linear",
                                  round_values=True)
        end = Task(self.stop_timer, timespan)
        for a in (ani, ani2, ani3, ani4, ani5):
            a.start(self)
            self.animations.add(a)
        self.animations.add(end)
        
    def stop_timer(self):
        self.done = True
        
    def update(self, dt):
        self.animations.update(dt)
        self.make_image()
        
    def make_image(self):
        self.image.fill((0,0,0,0))
        w, h = self.top_sand.get_size()
        top = h - self.top_height 
        ts_rect = pg.Rect(0, top, w, self.top_height) 
        top_sand = self.top_sand.subsurface(ts_rect)
        bw, bh = self.bottom_sand.get_size()
        bs_rect = pg.Rect(0, 0, bw, bh)
        b_sand = self.bottom_sand.subsurface(bs_rect)
        sw, sh = self.stream.get_size()
        s_rect = pg.Rect(0, 0, sw, self.stream_height)
        s_sand = self.stream.subsurface(s_rect)
        self.image.blit(s_sand, (0, self.stream_top))
        self.image.blit(top_sand, (0, self.top_top))
        self.image.blit(b_sand, (0, self.bottom_top))
        self.image.blit(self.glass, (0, 0))
        
    def draw(self, surface):
        surface.blit(self.image, self.topleft)
        
        
        
        
        