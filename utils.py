import map
import math

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
    after_decimal /= (10**math.ceil(math.log(after_decimal, 10)))
    return before_decimal + after_decimal

def nomralize_angle (ang):
    ang %= math.pi * 2
    if (ang < 0):
        ang += math.pi * 2
    return ang