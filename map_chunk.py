import map, utils, player, math
from log import LOG as log

MAX_CHUNKS = 128 # max number of unique chunks

CHUNK_PALETTE = [0] * MAX_CHUNKS

CHUNK_COUNT = 0
CHUNK_MAP = 1
CHUNK_NAME = 2
CHUNK_W = 16 # width of a chunk

DEFAULT_PALETTE = "data/maps/overworld/chunks.csv"

def load_chunk_palette (path):
    data = utils.bottomless_csv_load(path)
    for i in range(len(data)):
        CHUNK_PALETTE[i] = [0, None, data[i][0]]
    log.write("Loaded Chunks (" + path + ")")

load_chunk_palette(DEFAULT_PALETTE)

# down left good, right up bad

class M_Chunk():
    def __init__ (self, chunk_index, neighbors):
        self.id = chunk_index
        self.neighbors = neighbors
        CHUNK_PALETTE[chunk_index][CHUNK_COUNT] += 1
        if (CHUNK_PALETTE[chunk_index][CHUNK_MAP] == None):
            CHUNK_PALETTE[chunk_index][CHUNK_MAP] = map.Map(CHUNK_PALETTE[chunk_index][CHUNK_NAME])
        self.has_skybox = self.get_map().has_skybox
        self.has_ceil = self.get_map().has_ceil
        self.map = self.get_map().map
    
    def __str__(self):
        return self.name

    def destroy(self):
        CHUNK_PALETTE[self.id][CHUNK_COUNT] -= 1
        if (CHUNK_PALETTE[self.id][CHUNK_COUNT] <= 0):
            CHUNK_PALETTE[self.id][CHUNK_MAP] = None

    def in_chunk (self, p:player.Player):
        return p.x >=0 and p.x < CHUNK_W and p.y >=0 and p.y < CHUNK_W

    def __adjust_coor (self, x):
        out = [x, 1]
        if (x < 0):
            out[0] = x + CHUNK_W
            out[1] = 0
           #print (x, out[0])
        elif (x >= CHUNK_W):
            out[0] = x- CHUNK_W
            out[1] = 2
        return out

    def get_map (self):
        return CHUNK_PALETTE[self.id][CHUNK_MAP]

    def get_adjusted_coor (self, x, y):
        x_adj = self.__adjust_coor(x)
        y_adj = self.__adjust_coor(y)
        chunk = self.neighbors[y_adj[1]][x_adj[1]].get_map()
        #print(x,y,x_adj, y_adj)
        return [x_adj[0], y_adj[0], chunk]


    def is_valid (self, x, y):
        new_coor = self.get_adjusted_coor(x,y)
        if (new_coor[2] == None):
            return False
        return new_coor[2].is_valid(new_coor[0], new_coor[1])

    def is_empty (self, x, y):
        new_coor = self.get_adjusted_coor(x,y)
        if (new_coor[2] == None):
            return True
        return new_coor[2].is_empty(new_coor[0], new_coor[1])
    
    def get_floor_text (self, x, y):
        new_coor = self.get_adjusted_coor(x,y)
        if (new_coor[2] == None):
            return None
        return new_coor[2].get_floor_text(new_coor[0], new_coor[1])
    
    def get_ceil_text (self, x, y):
        new_coor = self.get_adjusted_coor(x,y)
        if (new_coor[2] == None):
            return None
        return new_coor[2].get_ceil_text(new_coor[0], new_coor[1])
    
    def get_height(self, x, y):
        new_coor = self.get_adjusted_coor(x,y)
        if (new_coor[2] == None):
            return 0
        return new_coor[2].get_height(new_coor[0], new_coor[1])
    
    def get_text(self, x, y, off):
        new_coor = self.get_adjusted_coor(x,y)
        if (new_coor[2] == None):
            return None
        return new_coor[2].get_text(new_coor[0], new_coor[1], off)
    
    def get_skybox(self):
        return self.get_map().get_skybox()
    
    def rendermap(self, screen, Player, fill_w, fill_h, x0, y0, w, h, x_off = 0, y_off = 0):
        self.get_map().rendermap(screen, Player, fill_w, fill_h, x0, y0, w, h, x_off, y_off)

class Overmap():
    EMPTY_CHUNK = 0
    SUPPORT_W = 3
    MID_VALUE = math.floor(SUPPORT_W/2)

    def __init__ (self):
        self.primary_x = 0
        self.primary_y = 0
        self.render_world = [[0] * self.SUPPORT_W for i in range(self.SUPPORT_W)]
        self.empty = M_Chunk(self.EMPTY_CHUNK, self.render_world)
        self.map_ptr = M_Wrapper(self.empty)

    def __update_m_ptr__ (self):
        self.map_ptr.update_map( self.render_world[self.MID_VALUE][self.MID_VALUE])
        return self.map_ptr

    def load (self, path, start_chunk_x, start_chunk_y):
        self.primary_x = start_chunk_x
        self.primary_y = start_chunk_y
        self.grid = utils.bottomless_csv_load(path)
        self.chunks = [MAX_CHUNKS]
        log.write(str((start_chunk_x, start_chunk_y)))
       
        for i in range ((self.SUPPORT_W)):
            for j in range((self.SUPPORT_W)):
                log.write("added: "+ str((i + self.primary_x - self.MID_VALUE, j + self.primary_y - self.MID_VALUE))+ " to " + str((i, j)))
                print(("added: "+ str((i + self.primary_x - self.MID_VALUE, j + self.primary_y - self.MID_VALUE))+ " to " + str((i, j))))
                self.render_world[j][i] = self.init_chunk(i + self.primary_x - self.MID_VALUE, j + self.primary_y - self.MID_VALUE)
        self.print_map()
        self.__update_m_ptr__()
        return self.map_ptr

    def init_chunk(self, x, y):
        if (y < 0 or y >= len(self.grid) or x < 0 or x >= len(self.grid[y])):
            return self.empty
        return M_Chunk(self.grid[y][x], self.render_world)

    def delete_group(self, x0, y0, dx, dy):
        for i in range(self.SUPPORT_W):
            print("deleted: " + str((x0 + i * dx, y0 + i * dy)))
            del_me = self.render_world[y0 + i * dy][x0 + i * dx]
            if (del_me != self.empty):
                del_me.destroy()

    def shift_group(self, dx, dy, targ_x, targ_y):
        for y in range (self.SUPPORT_W):
            for x in range(self.SUPPORT_W):
                if (x + dx >=0 and y + dy >= 0 and x + dx < self.SUPPORT_W and y + dy < self.SUPPORT_W):
                    print("shifted " + str((x,y)) + " to " + str((x+dx, y + dy)))
                    self.render_world[y + dy][x + dx] = self.render_world[y][x]

        for i in range (self.SUPPORT_W):
            if (targ_x >= 0):
                    print("added (x)" + str((targ_x,i)))
                    self.render_world[i][targ_x] = self.init_chunk(self.primary_x + i - self.MID_VALUE, self.primary_y)
            elif (targ_y >= 0):
                print("added (y)" + str((i, targ_y)))
                self.render_world[targ_y][i] = self.init_chunk(self.primary_x, self.primary_y + i -self.MID_VALUE)

    def print_map (self):
        print(str((self.primary_x, self.primary_y)))
        for y in range(self.SUPPORT_W):
            line = "["
            line += str(self.render_world[y][0].id)
            for x in range(1, self.SUPPORT_W):
                line += "," + str(self.render_world[y][x].id)
            print(line + "]")

    def update (self, p: player.Player):
        if not self.render_world[self.MID_VALUE][self.MID_VALUE].in_chunk(p):
            log.write(str((self.primary_x, self.primary_y)))
            if (p.x < 0):
                p.x += CHUNK_W
                self.primary_x -= 1
                #print("a")
                self.delete_group(0, self.SUPPORT_W - 1, 0, -1)
                self.shift_group(1, 0, 0 ,-1)
            elif (p.x >= CHUNK_W):
                p.x -= CHUNK_W
                self.primary_x += 1
                #print("b")
                self.delete_group(0, 0, 0, 1)
                self.shift_group(-1, 0,self.SUPPORT_W - 1, -1)
            if (p.y < 0):
                p.y += CHUNK_W
                self.primary_y -= 1
                #print("c")
                self.delete_group(self.SUPPORT_W - 1, 0, -1, 0)
                self.shift_group(0, 1, -1 ,0)
            elif (p.y >= CHUNK_W):
                p.y -= CHUNK_W
                self.primary_y += 1
                #print("d")
                self.delete_group(0, 0, 1, 0)
                self.shift_group(0, -1,-1, self.SUPPORT_W - 1)
            self.print_map()
            self.__update_m_ptr__()

class M_Wrapper(map.Map):
    def __init__(self, map):
        self.map = map
        self.has_skybox = map.has_skybox
        self.has_ceil = map.has_ceil
    
    def __str__(self):
        return str(self.map)

    def is_valid (self, x, y):
        return self.map.is_valid(x,y)

    def is_empty (self, x, y):
        return self.map.is_empty(x,y)
    
    def get_floor_text (self, x, y):
        return self.map.get_floor_text(x,y)
    
    def get_ceil_text (self, x, y):
        return self.map.get_ceil_text(x,y)
    
    def get_height(self, x, y):
        return self.map.get_height(x,y)
    
    def get_text(self, x, y, off):
        return self.map.get_text(x,y,off)
    
    def get_skybox(self):
        return self.map.get_skybox()
    
    def rendermap(self, screen, Player, fill_w, fill_h, x0, y0, w, h, x_off = 0, y_off = 0):
        self.map.rendermap(screen, Player, fill_w, fill_h, x0, y0, w, h, x_off, y_off)

    def update_map (self, new_map):
        self.map = new_map
        self.has_skybox = new_map.has_skybox
        self.has_ceil = new_map.has_ceil

OVER_MAP = Overmap()