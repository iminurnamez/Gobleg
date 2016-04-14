import pygame as pg
from .. import tools
from ..prepare import GFX, SCREEN_RECT, FONTS
from ..components.animation import Animation, Task
from ..components.labels import Blinker


class Icon(pg.sprite.Sprite):
    def __init__(self, image, topleft, *groups):
        super(Icon, self).__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=topleft)
        

class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.animations = pg.sprite.Group()
        self.labels = pg.sprite.Group()
        self.letters = pg.sprite.Group()
        imgs = [GFX["letter_{}".format(letter)] for letter in "GOBLEG"]
        delays = [x * 250 for x in (4, 1, 5, 3, 6, 2)]
        w, h = imgs[0].get_size()
        space = 20
        total_w = (w * len(imgs)) + (space * (len(imgs) - 1))
        left = SCREEN_RECT.centerx - (total_w // 2)
        top = SCREEN_RECT.centery - 100
        timespan = 1500
        for img, delay in zip(imgs, delays):
            icon = Icon(img, (left, -150), self.letters)
            left += w + space
            ani = Animation(top=top, duration=timespan, delay=delay, transition="out_bounce", round_values=True)
            ani.start(icon.rect)
            self.animations.add(ani)
        midbottom = (SCREEN_RECT.centerx, SCREEN_RECT.bottom - 10)
        font = FONTS["weblysleekuisb"]
        self.prompt = Blinker("Press any key to continue", {"midbottom": midbottom},
                                        500, text_color="antiquewhite", font_path=font,
                                        font_size=48)
        task = Task(self.labels.add, max(delays) + timespan, args=(self.prompt,))
        self.animations.add(task)
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type ==pg.KEYUP:
            if event.type == pg.K_ESCAPE:
                self.quit = True
            else:
                self.done = True
                self.next = "BOGGLING"
                
    def update(self, dt):
        self.animations.update(dt)
        self.labels.update(dt)
        
    def draw(self, surface):
        surface.fill((24, 191, 247))
        self.letters.draw(surface)
        self.labels.draw(surface)