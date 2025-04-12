import pygame
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

    PT_LOWER = 0
    PT_UPPER = 1
    PT_PRINT_LOWER = 2
    PT_PRINT_UPPER = 4

    PRINT_TABLE = {pygame.K_SPACE: {PT_LOWER : ' ', PT_UPPER : ' ', PT_PRINT_LOWER : 'SPACE', PT_PRINT_UPPER : 'SPACE'}, 
                   pygame.K_BACKSPACE : {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'BCK_SP', PT_PRINT_UPPER : 'BCK_SP'}, 
                   pygame.K_DELETE: {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'DEL', PT_PRINT_UPPER : 'DEL'},
                   pygame.K_UP : {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'UP', PT_PRINT_UPPER : 'UP'},
                   pygame.K_DOWN : {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'DOWN', PT_PRINT_UPPER : 'DOWN'},
                   pygame.K_LEFT : {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'LEFT', PT_PRINT_UPPER : 'LEFT'},
                   pygame.K_RIGHT : {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'RIGHT', PT_PRINT_UPPER : 'RIGHT'},
                   pygame.K_CAPSLOCK : {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'CAPS', PT_PRINT_UPPER : 'CAPS'},
                   pygame.K_TAB : {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'TAB', PT_PRINT_UPPER : 'TAB'},
                   pygame.K_ESCAPE : {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'ESC', PT_PRINT_UPPER : 'ESC'},
                   pygame.K_LSHIFT : {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'SHIFT', PT_PRINT_UPPER : 'SHIFT'},
                   pygame.K_LCTRL : {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'CTRL', PT_PRINT_UPPER : 'CTRL'},
                   pygame.K_LALT : {PT_LOWER : '', PT_UPPER : '', PT_PRINT_LOWER : 'ALT', PT_PRINT_UPPER : 'ALT'},
                   ord('\r') : {PT_LOWER : ' \n ', PT_UPPER : ' \n ', PT_PRINT_LOWER : 'ENTER', PT_PRINT_UPPER : 'ENTER'},
                   ord('\n') : {PT_LOWER : ' \n ', PT_UPPER : ' \n ', PT_PRINT_LOWER : 'ENTER', PT_PRINT_UPPER : 'ENTER'},
                   ord("`") : {PT_LOWER : '`', PT_UPPER : '~', PT_PRINT_LOWER : '`', PT_PRINT_UPPER : '~'},
                   ord("1") : {PT_LOWER : '1', PT_UPPER : '!', PT_PRINT_LOWER : '1', PT_PRINT_UPPER : '!'},
                   ord("2") : {PT_LOWER : '2', PT_UPPER : '@', PT_PRINT_LOWER : '2', PT_PRINT_UPPER : '@'},
                   ord("3") : {PT_LOWER : '3', PT_UPPER : '#', PT_PRINT_LOWER : '3', PT_PRINT_UPPER : '#'},
                   ord("4") : {PT_LOWER : '4', PT_UPPER : '$', PT_PRINT_LOWER : '4', PT_PRINT_UPPER : '$'},
                   ord("5") : {PT_LOWER : '5', PT_UPPER : '%', PT_PRINT_LOWER : '5', PT_PRINT_UPPER : '%'},
                   ord("6") : {PT_LOWER : '6', PT_UPPER : '^', PT_PRINT_LOWER : '6', PT_PRINT_UPPER : '^'},
                   ord("7") : {PT_LOWER : '7', PT_UPPER : '&', PT_PRINT_LOWER : '7', PT_PRINT_UPPER : '&'},
                   ord("8") : {PT_LOWER : '8', PT_UPPER : '*', PT_PRINT_LOWER : '8', PT_PRINT_UPPER : '*'},
                   ord("9") : {PT_LOWER : '9', PT_UPPER : '(', PT_PRINT_LOWER : '9', PT_PRINT_UPPER : '('},
                   ord("0") : {PT_LOWER : '0', PT_UPPER : ')', PT_PRINT_LOWER : '0', PT_PRINT_UPPER : ')'},
                   ord("-") : {PT_LOWER : '-', PT_UPPER : '_', PT_PRINT_LOWER : '-', PT_PRINT_UPPER : '_'},
                   ord("=") : {PT_LOWER : '=', PT_UPPER : '+', PT_PRINT_LOWER : '=', PT_PRINT_UPPER : '+'},
                   ord('[') : {PT_LOWER : '[', PT_UPPER : '{', PT_PRINT_LOWER : '[', PT_PRINT_UPPER : '{'},
                   ord(']') : {PT_LOWER : ']', PT_UPPER : '}', PT_PRINT_LOWER : '[', PT_PRINT_UPPER : '}'},
                   ord('\\') : {PT_LOWER : '\\', PT_UPPER : ' | ', PT_PRINT_LOWER : '\\', PT_PRINT_UPPER : '|'},
                   ord(';') : {PT_LOWER : ';', PT_UPPER : ':', PT_PRINT_LOWER : ';', PT_PRINT_UPPER : ':'},
                   ord('\'') : {PT_LOWER : '\'', PT_UPPER : '\"', PT_PRINT_LOWER : '\'', PT_PRINT_UPPER : '\"'},
                   ord(',') : {PT_LOWER : ',', PT_UPPER : '<', PT_PRINT_LOWER : ',', PT_PRINT_UPPER : '<'},
                   ord('.') : {PT_LOWER : '.', PT_UPPER : '>', PT_PRINT_LOWER : '.', PT_PRINT_UPPER : '>'},
                   ord('/') : {PT_LOWER : '/', PT_UPPER : '?', PT_PRINT_LOWER : '/', PT_PRINT_UPPER : '?'},}
    for i in range (ord('a'), ord('z')):
        PRINT_TABLE[i] = {PT_LOWER : chr(i), PT_UPPER : chr(i - 32), PT_PRINT_LOWER : chr(i), PT_PRINT_UPPER : chr(i-32)}


class __Terminal__():
    POLL_KP = 0
    POLL_ENT = 1
    POLL_DEL = 2
    POLL_TXT = 3
    POLL_ARROWS = 4
    P_UP = 0
    P_DOWN = 1
    P_LEFT = 2
    P_RIGHT = 3
    P_NONE = -1

    def __init__ (self):
        self.old = {}
        for key in Key.PRINT_TABLE:
            self.old[key] = False
        self.caps_lock = False

    def poll_keys(self, keys, get_sanatized = False):
        out = ""
        hit = False
        if keys[pygame.K_CAPSLOCK] and not self.old[pygame.K_CAPSLOCK]:
            self.caps_lock = not self.caps_lock
        is_caps = self.caps_lock
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            is_caps = True
        elif (keys[ord('\r')] and not self.old[ord('\r')]) or (keys[ord('\n')] and not self.old[ord('\n')]):
            self.old = keys
            return (True, True,True,"", self.P_NONE)
        if (keys[pygame.K_BACKSPACE] and not self.old[pygame.K_BACKSPACE])  or (keys[pygame.K_DELETE] and not self.old[pygame.K_DELETE]):
            self.old = keys
            return (True, False, True, "", self.P_NONE)
        
        a_pressed = self.P_NONE
        if (keys[pygame.K_UP] and not self.old[pygame.K_UP]):
            a_pressed = self.P_UP
        elif (keys[pygame.K_DOWN] and not self.old[pygame.K_DOWN]):
            a_pressed = self.P_DOWN
        elif (keys[pygame.K_LEFT] and not self.old[pygame.K_LEFT]):
            a_pressed = self.P_LEFT
        elif (keys[pygame.K_RIGHT] and not self.old[pygame.K_RIGHT]):
            a_pressed = self.P_RIGHT
            
        for key in Key.PRINT_TABLE:
            if keys[key] and not self.old[key]:
                hit = True
                mod = Key.PT_LOWER
                if is_caps:
                    if get_sanatized:
                        mod = Key.PT_PRINT_UPPER
                    else:
                        mod = Key.PT_UPPER
                elif get_sanatized:
                    mod = Key.PT_PRINT_LOWER 
                out += Key.PRINT_TABLE[key][mod]
        self.old = keys
        return (hit, False,False, out,a_pressed)

CONFIG = __Options__()
TERM = __Terminal__()