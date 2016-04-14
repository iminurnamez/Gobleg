import os
import json

import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Blinker


class HighScoreScreen(tools._State):
    def __init__(self):
        super(HighScoreScreen, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        new_score = self.persist["score"]
        try:
            with open(os.path.join("resources", "high_scores.json"), "r") as f:
                scores = json.load(f)
        except:
            scores = []
        scores.append(new_score)
        scores.sort(reverse=True)
        scores = scores[:10]
        with open(os.path.join("resources", "high_scores.json"), "w") as out:
            json.dump(scores, out)
        self.make_labels(scores, new_score)
            
    def make_labels(self, scores, score):
        self.labels = pg.sprite.Group()
        self.blinkers = pg.sprite.Group()
        font = prepare.FONTS["weblysleekuisb"]
        
        mid = prepare.SCREEN_RECT.centerx
        top = 105
        Label("High Scores", {"midtop": (mid, -10)}, self.labels,
                 font_path=font, font_size=96, text_color=(24, 191, 247))
        self.prompt = Blinker("Press any key to continue", {"midbottom": (mid, prepare.SCREEN_RECT.bottom - 10)},
                                        500, self.labels, text_color="antiquewhite", font_path=font, font_size=48)
        highlighted = False
        for s in scores:
            if s == score and not highlighted:
                color = (24, 191, 247)
                highlighted = True
            else:
                color = (255, 204, 0)        
            Label("{}".format(s), {"midtop": (mid, top)}, self.labels, font_path=font,
                     font_size=56, text_color=color)
            top += 50
                    
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            else:
                self.done = True
                self.next = "BOGGLING"

    def update(self, dt):
        self.prompt.update(dt)
        
    def draw(self, surface):
        surface.fill(pg.Color("dodgerblue"))
        self.labels.draw(surface)
        self.prompt.draw(surface)