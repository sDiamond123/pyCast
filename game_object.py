import utils, math, pygame

class World_Sprite:
    META = "\meta.csv"
    MANIFEST = "\manifest.csv"
    META_W = 2
    META_H = 2

    def __init__(self, file):
        data = utils.csv_load(file + self.META, self.META_W, self.META_H)
        self.faces = data[0][0]
        w = data[0][1]
        manifest = utils.csv_load(file + self.MANIFEST, w, self.faces)
        self.sprites = [None] * self.faces
        for i in range (self.faces):
            self.sprites[i] = pygame.image.load(file + "\\" + manifest[i][0])
        self.ang_per_face = 2 * math.pi / self.faces
        self.offset = utils.convert_csv_to_float(data, 1)

    def get_face (self, ang):
        ang = utils.normalize_angle(ang + self.offset)
        index = int(ang/self.ang_per_face)
        return self.sprites[index]


class Game_Object:
    META_W = 2
    META_H = 7
    META = "\meta.csv"
    SPRITE_PATH = "\sprites"
    SPRITE_MANIFEST = "\manifest.csv"
    SPRITE_MAINIFEST_W = 4
    DEFAULT_STATE = "DEFAULT"

    x = 0
    y = 0
    w = 0
    h = 0
    z = 0
    ang = 0
    sprite = None
    name = "UNDEFINED"
    state = None
    health = 0
    
    def __init__ (self, x, y, ang, obj, sprites, state, health):
        

        self.x = x
        self.y = y
        self.ang = ang
        data = utils.csv_load(obj + self.META, self.META_W, self.META_H)
        self.name = data[0][0]
        self.health = health
        if state == self.DEFAULT_STATE:
            self.state = data[1][0]
        else:
            self.state = state
        self.h = utils.convert_csv_to_float(data, 2)
        self.w = utils.convert_csv_to_float(data, 3)
        self.z = utils.convert_csv_to_float(data, 4)
        # load in sprites if we don't already have them
        self.is_opaque = data[6][1] == 'True'
        sprite_count = data[6][0]
        if (sprite_count > 0):
            sprite_data = utils.csv_load(obj + self.SPRITE_PATH + self.SPRITE_MANIFEST, self.SPRITE_MAINIFEST_W, sprite_count)
            for i in range(sprite_count):
                key = self.__get_sprite_key__(sprite_data[i][0])
                if not key in sprites:
                    if sprite_data[i][1] == "simple":
                        sprites[key] = World_Sprite(obj + self.SPRITE_PATH + sprite_data[i][2])
                        print ("Successfully loaded sprite: " +key)
        self.sprites = sprites
        print("Successfully placed a " + self.name + " <" + self.state + ", " + str(self.health)+ " HP> at (" + str(x) + "," + str(y) + ")")


    def __get_sprite_key__(self, state):
        return self.name + " -> " + state
    
    def __get_raw_sprite__ (self, ang):
        return self.sprites[self.__get_sprite_key__(self.state)].get_face(ang)

    def get_sprite(self, w, h, ang):
        return pygame.transform.smoothscale(self.__get_raw_sprite__(self.ang - ang + math.pi), (w,h))