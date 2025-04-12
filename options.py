from utils import Ptr as Ptr
from log import LOG as log

class __Options__ ():
    CONFIG = "data/config/config.txt"
    DEFAULT = "data/config/profiles/default.txt"
    NASA = "data/config/profiles/nasa.txt"
    HIGH = "data/config/profiles/good.txt"
    MED = "data/config/profiles/medium.txt"
    LOW = "data/config/profiles/bad.txt"
    POTATO = "data/config/profiles/potato.txt"

    def __init__(self):
        self.contents = {}
        self.load_config()

    def __get_header__(self, config):
        bp=config.readline()
        self.boilerplate.append(bp)
        return bp
    
    def __update_ptr__ (self, header, item):
        if header in self.contents:
            self.contents[header].value = item
        else:
            self.contents[header] = Ptr(item)

    def load_config(self):
        self.load_custom(self.CONFIG)

    def load_custom(self, file):
        config = open(file, "r")
        self.boilerplate = []
        header = self.__get_header__(config)
        self.PROF_NAME = header
        item = ((config.readline()).strip())
        self.__update_ptr__(header, item)
        header = self.__get_header__(config)
        self.WINDOW_NAME = header
        item= config.readline().strip()
        self.contents[header] = item
        header = self.__get_header__(config)
        self.ICON = header
        item  = config.readline()[:-1]
        self.contents[header] = item
        header = self.__get_header__(config)
        self.FULLSCREEN = header
        item = "true" == (config.readline().strip().lower())
        self.contents[header] = item
        header = self.__get_header__(config)
        self.W = header
        item = int(config.readline())
        self.contents[header] = item
        header = self.__get_header__(config)
        self.H = header
        item = int(config.readline())
        self.contents[header] = item
        header = self.__get_header__(config)
        self.FPS = header
        item = int(config.readline())
        self.__update_ptr__(header, item)
        header = self.__get_header__(config)
        self.I_W = header
        item = int(config.readline())
        self.contents[header] = item
        header = self.__get_header__(config)
        self.I_H = header
        item= int(config.readline())
        self.contents[header] = item
        header = self.__get_header__(config)
        self.X_SENSE = header
        item = int(config.readline())
        self.__update_ptr__(header, item)
        header = self.__get_header__(config)
        self.Y_SENSE = header
        item = int(config.readline())
        self.__update_ptr__(header, item)
        header = self.__get_header__(config)
        self.FOV = header
        item = int(config.readline())
        self.__update_ptr__(header, item)
        header = self.__get_header__(config)
        self.RAYS = header
        item = (int(config.readline()))
        self.__update_ptr__(header, item)
        header = self.__get_header__(config)
        self.DRAW_DIST = header
        item = (int(config.readline()))
        self.__update_ptr__(header, item)
        config.close()
        log.write("Config loaded (" + file + ")")

    def save_config(self):
        config = open(self.CONFIG, "w")
        for i in range(len(self.boilerplate)):
            config.write(self.boilerplate[i])
            config.write(str(self.contents[self.boilerplate[i]]) + "\n")
        config.close()
        log.write("Config updated")


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
    binds = open("data/config/key_binds.txt", "r")
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
    SHOOT = get_key(binds)
    RELOAD = get_key(binds)
    CYCLE_NEXT = get_key(binds)
    CYCLE_PREV = get_key(binds)
    M_ZOOM_IN = get_key(binds)
    M_ZOOM_OUT = get_key(binds)
    INTERACT = get_key(binds)
    MAP = get_key(binds)
    PAUSE = get_key(binds)
    UI = get_key(binds)
    binds.close()
    log.write("Successfully loaded key binds")

CONFIG = __Options__()