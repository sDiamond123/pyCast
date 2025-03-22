import pygame
import math
import utils
import texture

class Map :
    EMPTY_TILE = 0
    #organization for loading maps
    PATH = "data/maps/"
    H_MAP = "/hmap.csv"
    F_MAP = "/fmap.csv"
    C_MAP = "/cmap.csv"
    COLOR = "/colors.csv"
    DATA = "/meta.csv"
    T_MAP = "/tmap.csv"
    TEXTS = "/texts.csv"
    META_W = 3
    META_H = 5
    TRANS = "x" # transparent color, also trans rights 
    has_ceil = True # true if has ceil, false use rolling skybox
    # array of tile colors
    palette = []
    text_palette = []
        
    # collision/height map
    map = []
    
    # tile map for ceil (if needed)
    ceil_map = []
    
    # tile map for floor
    floor_map = []

    text_map = []

    skybox = None
    skybox_phase = 0

    def __init__(self, map_name):
        # set up path to map directery
        map_name = self.PATH + map_name
        # get map meta data
        meta = utils.csv_load(map_name+self.DATA, self.META_W, self.META_H)
        map_w = meta[0][0]
        map_h = meta[0][1]
        map_p = meta[0][2]
        map_t = meta [4] [0]
        self.has_skybox = (meta[1][0].lower()) == "true"
        self.has_ceil = (meta[3][0].lower()) == "true"
        # load maps
        self.map = utils.csv_load(map_name + self.H_MAP, map_w, map_h)
        self.floor_map = utils.csv_load(map_name + self.F_MAP, map_w, map_h)
        self.text_map = utils.csv_load(map_name + self.T_MAP, map_w, map_h)
        if (self.has_ceil):
            self.ceil_map = utils.csv_load(map_name + self.C_MAP, map_w, map_h)
        if(self.has_skybox):
            self.skybox = meta[1][1]
            self.skybox_phase = utils.convert_csv_to_float(meta, 2)
        # load palette
        colors = utils.csv_load(map_name + self.COLOR, 3, map_p)
        self.palette = [None] * map_p
        for i in range(map_p):
            self.palette[i] = (colors[i][0], colors[i][1], colors[i][2])
        # load textures
        texts = utils.csv_load(map_name+self.TEXTS, 2, map_t)
        self.text_palette = [None] * map_t
        for i in range (map_t):
            if texts[i][1].strip().lower() == "false":
                # load simple texture
                self.text_palette[i] = texture.Texture(texts[i][0])
            else:
                # load animated texture
                self.text_palette[i] = texture.AnimatedTexture(texts[i][0])
            
        print("Successfully loaded map: " + map_name)
        
    def is_valid (self, x, y):
        return y >= 0 and y < len(self.map) and x >= 0 and x < len(self.map[int(y)])

    def is_empty (self, x, y):
        return self.get_height(x,y) == self.EMPTY_TILE
    
    def get_floor_text (self, x, y):
        return self.palette[self.floor_map[int(y)][int(x)]]
    
    def get_ceil_text (self, x, y):
        result = self.ceil_map[int(y)][int(x)]
        if (result != 'x'):
            return self.palette[result]
        return result
    
    def get_height(self, x, y):
        return self.map[int(y)][int(x)]
    
    def get_text(self, x, y, off):
        return self.text_palette[self.text_map[int(y)][int(x)]].get_slice(off)
    
    def get_skybox(self):
        return (self.skybox, self.skybox_phase)
    
    def rendermap(self, screen, Player, fill_w, fill_h, x0, y0, w, h, x_off = 0, y_off = 0):
            w = math.floor(w)
            h = math.floor(h)
            center_x = Player.x + x_off
            center_y = Player.y + y_off
            ang = Player.ang
            # fill map grid
            x0 += fill_w * w
            y0 += fill_h * h
            for dy in range(-fill_h, fill_h + 1):
                for dx in range(-fill_w, fill_w + 1):
                    x = center_x + dx
                    y = center_y + dy
                    cell = (x0 + dx * w, y0 + dy * h, w, h)
                    color = "black"
                    if self.is_valid(x,y):
                        if (self.is_empty(x,y)):
                            color = self.get_floor_text(x,y)
                    else:
                        color = "grey"
                    pygame.draw.rect(screen,color,cell)
            # draw grid lines
            for dy in range(-fill_h + 1, fill_h + 1):
                pygame.draw.line(screen, "black", (x0 - fill_w * w, y0 + dy * h ), (x0 + (fill_w + 1) * w, y0 + dy * h))
            for dx in range(-fill_w + 1, fill_w + 1):
                pygame.draw.line(screen, "black", (x0 + dx * w, y0 -fill_h * h ), (x0 + dx * w, y0 + (fill_h + 1) * h))
            # draw player
            point =  pygame.Vector2(x0+ w*(Player.x-int(center_x)), y0 + h*(Player.y-int(center_y)))
            pygame.draw.circle(screen, "green",point, w/4)
            pygame.draw.line(screen, "green", point, (point.x + w/2 * math.cos(ang), point.y + w/2 * math.sin(ang)), 2)