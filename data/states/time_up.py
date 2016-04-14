import pygame as pg

from .. import tools, prepare
from ..components.labels import Label
from ..components.animation import Animation, Task


SCORES = {
        3: 1,
        4: 1,
        5: 2,
        6: 3,
        7: 5}


class TimeUp(tools._State):
    def __init__(self):
        super(TimeUp, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        self.animations = pg.sprite.Group()
        self.board = self.persist["board"]
        self.words = self.board.word_labels
        self.make_labels()
        self.score_labels = pg.sprite.Group()
        self.total_score = 0
        self.total_score_label = Label(
                "{}".format(self.total_score),
                {"center": prepare.SCREEN_RECT.center},
                font_path=prepare.FONTS["weblysleekuisb"],
                font_size=256, text_color=(24, 191, 247))                
        
    def make_labels(self):
        self.labels = pg.sprite.Group()
        label = Label("Time's Up!", {"midtop": (prepare.SCREEN_RECT.centerx, -50)},
                self.labels, font_path=prepare.FONTS["weblysleekuisb"],
                font_size=128, text_color=pg.Color(24, 191, 247))
        task = Task(label.set_text, 4000, args=("",))
        ani = Animation(centery=prepare.SCREEN_RECT.centery,
                                 duration=2000, transition="out_bounce",
                                 round_values=True)
        task2 = Task(self.score_words, 4500)
        ani.start(label.rect)
        self.animations.add(task, ani, task2)
        
    def score_words(self):
        delay = 0
        start_color = (61, 64, 255)
        final_color = (24, 191, 247)
        cx, cy = prepare.SCREEN_RECT.center
        style = {"font_path": prepare.FONTS["weblysleekuisb"],
                     "font_size": 96, "text_color": start_color}
        
        timespan = 500
        for w in self.words:
            score = self.score_word(w.text)
            
            label = Label("{}".format(score), {"center": w.rect.center}, **style)
            label.r, label.g, label.b = start_color
            label.x_pos, label.y_pos = label.rect.center
            ani = Animation(x_pos=cx, y_pos=cy, duration=timespan, delay=delay,
                                     transition="in_out_cubic", round_values=True)
            ani_red = Animation(r=final_color[0], duration=timespan, delay=delay, transition="linear", round_values=True)
            ani_green = Animation(g=final_color[1], duration=timespan, delay=delay, transition="linear", round_values=True)
            ani_blue = Animation(b=final_color[2], duration=timespan, delay=delay, transition="linear", round_values=True)
            task = Task(self.score_labels.add, delay, args=(label,))
            task2 = Task(self.score_labels.remove, timespan + delay, args=(label,)) 
            task3 = Task(self.add_to_score, timespan + delay, args=(score,))
            task4 = Task(w.kill, delay)
            ani.start(label)
            ani_red.start(label)
            ani_green.start(label)
            ani_blue.start(label)
            self.animations.add(ani, task, task2, task3, task4, ani_red, ani_green, ani_blue)
            delay += 300
        leave = Task(self.leave_state, delay + timespan + 2000)
        self.animations.add(leave)

    def leave_state(self):
        self.done = True
        self.next = "HIGH_SCORES"
        self.persist["score"] = self.total_score
        
    def score_word(self, word):
        if len(word) >= 8:
            return 11
        else:
            return SCORES[len(word)]
            
    def add_to_score(self, score):
        self.total_score += score
        self.total_score_label.set_text("{}".format(self.total_score))
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
                
    def update(self, dt):
        self.animations.update(dt)
        for label in self.score_labels:
            label.text_color = label.r, label.g, label.b
            label.set_text(label.text)
            label.rect.center = label.x_pos, label.y_pos

    def draw(self, surface):
        surface.fill(pg.Color("dodgerblue"))
        self.board.draw(surface)
        self.labels.draw(surface)
        if self.total_score:
            self.total_score_label.draw(surface)
        self.score_labels.draw(surface)
        