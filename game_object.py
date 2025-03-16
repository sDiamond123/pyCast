import utils, math, pygame, map

class World_Sprite:
    META = "/meta.csv"
    MANIFEST = "/manifest.csv"
    META_W = 2
    META_H = 2

    def __init__(self, file):
        data = utils.csv_load(file + self.META, self.META_W, self.META_H)
        self.faces = data[0][0]
        w = data[0][1]
        manifest = utils.csv_load(file + self.MANIFEST, w, self.faces)
        self.sprites = [None] * self.faces
        for i in range (self.faces):
            self.sprites[i] = pygame.image.load(file + "/" + manifest[i][0])
        self.ang_per_face = 2 * math.pi / self.faces
        self.offset = utils.convert_csv_to_float(data, 1)

    def get_face (self, ang):
        ang = utils.normalize_angle(ang + self.offset)
        index = int(ang/self.ang_per_face)
        return self.sprites[index]


class Game_Object:
    META_W = 2
    META_H = 8
    META = "/meta.csv"
    SPRITE_PATH = "/sprites"
    SPRITE_MANIFEST = "/manifest.csv"
    SPRITE_MAINIFEST_W = 4
    DEFAULT_STATE = "DEFAULT"
    ATTR_CODE = "ATTR"
    ATTRIBUTES = "/attributes.csv"

    w = 0
    h = 0
    sprite = None
    name = "UNDEFINED"
    state = None
    moving = False
    seeking = False
    b_type = ""
    target = None
    

    def __init__ (self, x, y, ang, obj, sprites, state, health):
        self.pos = utils.Obj_Vector(x,y,ang,health)
        data = utils.csv_load(obj + self.META, self.META_W, self.META_H)
        self.name = data[0][0]
        self.type = data[1][0]
        if state == self.DEFAULT_STATE:
            self.state = data[2][0]
        else:
            self.state = state
        self.h = utils.convert_csv_to_float(data, 3)
        self.w = utils.convert_csv_to_float(data, 4)
        self.pos.z = utils.convert_csv_to_float(data, 5)
        self.__raw_attr__ = utils.bottomless_csv_load(obj + self.ATTRIBUTES)
        self.load_state(self.state)
        # load in sprites if we don't already have them
        self.has_collision = data[6][1] == 'True'
        self.pos.no_clip = self.has_collision
        sprite_count = data[7][0]
        if (sprite_count > 0):
            sprite_data = utils.csv_load(obj + self.SPRITE_PATH + self.SPRITE_MANIFEST, self.SPRITE_MAINIFEST_W, sprite_count)
            for i in range(sprite_count):
                key = self.__get_sprite_key__(sprite_data[i][0])
                if not key in sprites:
                    if sprite_data[i][1] == "simple":
                        sprites[key] = World_Sprite(obj + self.SPRITE_PATH + sprite_data[i][2])
                        #print ("Successfully loaded sprite: " +key)
        self.sprites = sprites
        print("Successfully placed a " + self.name + " <" + self.state + ", " + str(self.health())+ " HP> at " + str(self.pos))
        print("\tattr: " +  str(self.attr))

    def x(self):
        return self.pos.x
    
    def y(self):
        return self.pos.y
    
    def z(self):
        return self.pos.z

    def ang(self):
        return self.pos.ang
    
    def health(self):
        return self.pos.health
    
    def change_health(self, delta):
        self.pos.health += delta
    
    def load_state(self, state):
        self.attr =  {"d_p" : 0, "d_o" : 0,  "d_s" : 0, "v_forward" : 0, "v_side" : 0, "ang_v" : 0}
        in_state = False
        in_att = False
        att = ""
        for line in self.__raw_attr__:
            if len(line) == 2 and line[0] == "ATTR":
                if in_state:
                    return True
                elif line [1].strip() == state:
                    in_state = True
            elif in_state:
                if (line[0] == "PROFILE"):
                    if "move" in line:
                        self.moving = True
                    else:
                        self.moving = False
                    if "seek" in line:
                        self.seeking = True
                        self.moving = True
                    else:
                        self.seeking = False
                    if "basic" in line:
                        self.b_type = "basic"
                    if self.seeking and "player" in line:
                        self.target = "player"
                else:
                    if in_att:
                        self.attr[att]= utils.convert_csv_to_float([line], 0)
                    else:
                        att = line[0]
                    in_att = not in_att
        return False

    def __dist__ (self, other: utils.Obj_Vector):
        return math.dist((other.x, other.y), (self.pos.x, self.pos.y))

    def check_collision_player (self, other : utils.Obj_Vector):
        return self.__dist__(other) < self.w
    
    def check_collision_object (self, other):
        if (self.name == other.name and self.x() == other.x() and self.y() == other.y() and self.ang() == other.ang() and self.health() == other.health()):
            return False
        return self.__dist__(other.pos) < self.w + other.w
    
    def check_map_collision (self, map: map.Map):
        return not(self.x() >= 0 and self.y() >= 0 and self.y() < len(map.map) and self.x ()< len(map.map[int(self.y())]) and map.is_empty(int(self.x()), int(self.y())))

    def __get_sprite_key__(self, state):
        return self.name + " -> " + state
    
    def __get_raw_sprite__ (self, ang):
        return self.sprites[self.__get_sprite_key__(self.state)].get_face(ang)

    def get_sprite(self, w, h, ang):
        return pygame.transform.smoothscale(self.__get_raw_sprite__(self.ang() - ang + math.pi), (w,h))
    
    def __turn__ (self, ang):
        self.pos.turn(ang)

    def __move__ (self,map, forward, side):
        self.pos.move_with_minimum(map, forward,side, self.w)

    def update(self, player, objects, map: map.Map):
        if (self.check_map_collision(map)):
            self.pos.health = 0
        else:
            if (self.moving):
                if (self.seeking):
                    if self.b_type == "basic" and self.target == "player":
                        diff = self.pos.ang - utils.get_angle(self.x(), self.y(), player.x, player.y)
                        if diff < -self.attr["ang_v"]:
                            self.__turn__(self.attr["ang_v"])
                        elif diff > self.attr["ang_v"]:
                            self.__turn__(-self.attr["ang_v"])
                        else:
                            self.__turn__(-diff)
                        dist = self.__dist__(player)
                        if (dist > self.attr["v_forward"]):
                            dist = self.attr["v_forward"]
                        self.__move__(map, dist, 0) 

                else:
                    if (self.attr["v_forward"] != 0 or self.attr["v_side"] != 0):
                        self.__move__(map, self.attr["v_forward"], self.attr["v_side"])
                    if (self.attr["ang_v"] != 0):
                        self.__turn__(self.attr["ang_v"])


class Projectile(Game_Object):
    def update(self, player, objects, map: map.Map):
        super().update(player,objects, map)
        if self.check_collision_player(player):
            print(self.name + " hit player for " + str(self.attr["d_p"]) + " dmg with " + str(self.attr["d_s"]) + " decay")
            self.change_health(-self.attr["d_s"])
            player.health -= self.attr["d_p"]
        for obj in objects:
            if self.health() < 0:
                break
            if (self.check_collision_object(obj)):
                self.change_health(-self.attr["d_s"])
                obj.change_health(-self.attr["d_o"])
                print(self.name + " hit obj " + obj.name + " for " + str(self.attr["d_o"]) + " dmg with " + str(self.attr["d_s"]) + " decay")
       

def spawn_objs (x, y, ang, obj, sprites, state, health):
    attr = utils.csv_load(obj + "/meta.csv", 2, 2) [1][0]
    if attr == "PROJECTILE":
        return Projectile(x,y,ang,obj,sprites,state,health)
    else:
        return Game_Object(x,y,ang,obj,sprites,state,health)