import os
from random import choice, shuffle

import pygame as pg
from .. import tools, prepare
from ..components.labels import Label


def load_words():
    with open(os.path.join("resources", "words", "words.txt"), "r") as f:
        words = set(f.readlines())
    return set(w.strip() for w in words)

def get_neighbors(index, indices):
    offsets = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
    neighbors = []
    for off in offsets:
        if off != (0, 0):
            new_index = index[0] + off[0], index[1] + off[1]
            if new_index in indices:
                neighbors.append(new_index)
    return neighbors

WORDS = load_words()
INDICES = [(x, y) for x in range(4) for y in range(4)]    
NEIGHBORS = {i: set(get_neighbors(i, INDICES)) for i in INDICES}


SET1 = [
        "AACIOT",
        "AHMORS",
        "EGKLUY",
        "ABILTY",
        "ACDEMP",
        "EGINTV",
        "GILRUW",
        "ELPSTU",
        "DENOSW",
        "ACELRS",
        "ABJMOQ",
        "EEFHIY",
        "EHINPS",
        "DKNOTU",
        "ADENVZ",
        "BIFORX"]

SET2 = [
        "AAEEGN",
        "ELRTTY",
        "AOOTTW",
        "ABBJOO",
        "EHRTVW",
        "CIMOTU",
        "DISTTY",
        "EIOSST",
        "DELRVY",
        "ACHOPS",
        "HIMNQU",
        "EEINSU",
        "EEGHNW",
        "AFFKPS",
        "HLNNRZ",
        "DEILRX"]


class LetterCube(object):
    def __init__(self, letters):
        self.letters = letters

    def shake(self):
        self.letter = choice(self.letters)
        self.image = prepare.GFX["letter_{}".format(self.letter)]
        if self.letter == "Q":
            self.letter = "QU"
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class CubeSpot(object):
    def __init__(self, index, cube=None):
        tile_size = 128
        self.index = index
        self.neighbors = NEIGHBORS[self.index]
        self.cube = cube
        left = (self.index[0] * tile_size) + (self.index[0] * 2)
        top = (self.index[1] * tile_size) + (self.index[1] * 2)
        self.rect = pg.Rect(left, top, tile_size, tile_size)
        
    @property
    def letter(self):
        if self.cube:
            return self.cube.letter
        else:
            return None
        
    
class BoggleBoard(object):
    def __init__(self, topleft, letters_set):
        self.topleft = topleft
        indices = [(x, y) for x in range(4) for y in range(4)]
        self.grid = {indx: CubeSpot(indx) for indx in indices}
        self.cubes = [LetterCube(letters) for letters in letters_set]
        self.new_game()
        self.make_image()
        self.words = []
        self.word_labels = pg.sprite.Group()        
        self.word_style = {
                "text_color": pg.Color("antiquewhite"),
                "font_size": 24,
                "font_path": prepare.FONTS["weblysleekuisb"]}
        self.word_top = 10
        self.max_word_top = 650
        self.word_left = 10
        self.vert_word_space = 30
        self.horiz_word_space = 100
        self.round_over = False
        self.bell = prepare.SFX["typewriter-bell"]
        
    def check_word(self, word):
        if len(word) < 3:
            return False
        if word in self.words:
            return False
        chars = list(word)
        for i, ch in enumerate(chars):
            if ch.lower() == "q":
                head = chars[:i + 1]
                head[-1] = "qu"
                tail = chars[i + 2:]
                chars = head + tail
        if not all((c.lower() in self.letters for c in chars)):
            return False
        if word not in WORDS:
            return False
        starts = []
        for cube_spot in self.grid.values():
            l = cube_spot.letter.lower()  
            if l == chars[0]:
                starts.append(cube_spot)
        for start in starts:
            valid = self.dfs(NEIGHBORS, self.grid, start.index, word)
            if valid:
                self.bell.play()
                self.add_word(word)
                break
        else:
            return False
            
    def add_word(self, word):        
        self.words.append(word)
        Label(word, {"topleft": (self.word_left, self.word_top)}, self.word_labels, **self.word_style)
        self.word_top += self.vert_word_space
        if self.word_top > self.max_word_top:
            self.word_top = 10
            self.word_left += self.horiz_word_space
            
    def dfs(self, connections, graph, start, word):
        target = list(word)
        for i, ch in enumerate(target):
            if ch.lower() == "q":
                head = target[:i + 1]
                head[-1] = "qu"
                tail = target[i + 2:]
                target = head + tail
        levels = []
        for _ in range(len(target)):
            levels.append([])
        levels[0].append([(start, start)])
        searching = True
        for depth in range(len(target)):
            for path in levels[depth]:
                parents = [p[1] for p in path]
                neighbors = connections[path[-1][1]]
                valid = []
                for n in neighbors:
                    n_letter = graph[n].cube.letter.lower()
                    if n_letter == target[depth + 1] and n not in parents:
                        valid.append(n)
                for v in valid:
                    longer_path = path[:]
                    longer_path.append((path[-1][1], v)) 
                    levels[depth + 1].append(longer_path)
            if not levels[depth + 1]:
                return False
            if levels[-1]:
                return True                    

    def new_game(self):
        self.shuffle_cubes()
        self.letters = [cube.letter.lower() for cube in self.cubes]
        
    def shuffle_cubes(self):
        spots = list(self.grid.keys())
        shuffle(spots)
        for spot, cube in zip(spots, self.cubes):
            cube.shake()
            self.grid[spot].cube = cube 
        
    def make_image(self):
        surf = pg.Surface((512, 512)).convert_alpha()
        surf.fill((0,0,0,0))
        for c in self.grid.values():
            surf.blit(c.cube.image, c.rect)
        self.image = surf
        self.rect = surf.get_rect(topleft=self.topleft)

    def draw(self, surface):
        surface.blit(self.image, self.topleft)
        self.word_labels.draw(surface)


