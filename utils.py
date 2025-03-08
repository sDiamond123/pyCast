import map
import math
import pygame


class Mouse_Manager:
    COOL_DOWN = 500
    MOUSE_FACTOR = 1000

    sensetivity = (0,0)
    alive = False
    last = (0,0)
    size = (0,0)
    abs = (0,0)
    rel = (0,0)
    prev_toggle = 0
    hold_x = 0

    def __init__ (self, sensitivity, dimensions):
        self.alive = False
        self.sensetivity = (sensitivity[0]/self.MOUSE_FACTOR, sensitivity[1]/self.MOUSE_FACTOR)
        self.size = dimensions
        self.prev_toggle = 0
        self.hold_x = int(self.size[0]/2)
        self.abs = (self.size[0], self.size[1])

    def toggle(self):
        time = pygame.time.get_ticks()
        if (time - self.prev_toggle > self.COOL_DOWN):
            self.prev_toggle = time
            self.alive = not self.alive
            pygame.mouse.set_visible(not self.alive)
            pygame.event.set_grab(self.alive)

    def poll_delta(self):
        return self.last
    
    def poll_abs(self):
        return self.abs
    
    def poll_rel(self):
        return self.rel

    def update(self):
        raw = pygame.mouse.get_rel()
        self.abs = pygame.mouse.get_pos()
        self.rel = (self.abs[0]/self.size[0], self.abs[1]/self.size[1])
        self.last = (raw[0] * self.sensetivity[0], raw[1] * self.sensetivity[1])

class Key:
    def get_key (file):
        # get rid of explanation line
        file.readline()
        # get key
        out = file.readline().lower().strip()
        if (out.isnumeric()):
            # if given a number, assume it's an ascii key
            return int(out)
        # else convert to ascii
        return ord(out[0])

    #set up key binds
    binds = open("data\config\key_binds.txt", "r")
    FORWARD = get_key(binds)
    BACK = get_key(binds)
    S_LEFT = get_key(binds)
    S_RIGHT = get_key(binds)
    TURN_L = get_key(binds)
    TURN_R = get_key(binds)
    JUMP = get_key(binds)
    CROUCH = get_key(binds)
    FREE_LOOK = get_key(binds)
    EXIT = get_key(binds)
    binds.close()
    print("Successfully loaded key binds")

class Player:
    x = 0
    y = 0
    z = 0
    ang = 0

    def __init__(self, x, y, ang):
        self.x = x
        self.y = y
        self.ang = ang
        print("Player spawned at (" +str(x)+","+str(y)+") facing " +str(math.degrees(ang)) +" degrees")

    def move(self, Map, v_forward, v_side_to_side):
        new_x = self.x + v_forward * math.cos(self.ang) + v_side_to_side * math.cos(self.ang + math.pi/2)
        new_y = self.y + v_forward * math.sin(self.ang) + v_side_to_side * math.sin(self.ang + math.pi/2)
        if Map.is_empty (new_x, new_y):
            self.x = new_x
            self.y = new_y    

    def turn (self, theta):
        self.ang += theta
        self.ang %= 2 * math.pi
        if self.ang < 0:
            self.ang += 2 * math.pi

def csv_load(csv_file, w, h):
    csv = open(csv_file)
    out = [ [0]*w for i in range(h)]
    for i in range(h):
        as_split = csv.readline()
        as_split = as_split.split(",")
        for j in range(w):
            if (j >= len(as_split)):
                break
            entry = as_split[j].strip()
            if entry.isnumeric():
                out [i][j] = int(entry)
            else:
                out[i][j] = entry
    csv.close
    return out

def convert_csv_to_float(array, row):
    before_decimal = array[row][0]
    after_decimal = array[row][1]
    if after_decimal != 0:
        after_decimal /= (10**math.ceil(math.log(after_decimal, 10)))
    return before_decimal + after_decimal

def normalize_angle (ang):
    ang %= math.pi * 2
    if (ang < 0):
        ang += math.pi * 2
    return ang