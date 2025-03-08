import utils
import pygame

class World_Sprite:
    META = "\meta.csv"
    MANIFEST = "\manifest.csv"
    META_W = 2
    META_H = 8

    sprites = []
    faces = 0
    def __init__(self, file):
        data = utils.csv_load(file + self.META, self.META_W, self.META_H)
        self.faces = data[0][0]
        w = data[0][1]
        manifest = utils.csv_load(file + self.MANIFEST, w, self.faces)
        self.sprites = [None] * self.faces
        for i in range (self.faces):
            self.sprites[i] = pygame.image.load(file + "\\" + manifest[i][0])


class Game_Object:
    META_W = 2
    META_H = 6
    META = "\meta.csv"
    x = 0
    y = 0
    ang = 0
    sprite = None
    name = "UNDEFINED"
    
    def __init__ (self, x, y, ang, obj):
        self.x = x
        self.y = y
        self.ang = ang
        data = utils.csv_load(obj + self.META, self.META_W, self.META_H)
        self.name = data[0][0]
