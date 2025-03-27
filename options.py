from utils import Ptr as Ptr

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
        print("Config loaded (" + file + ")")

    def save_config(self):
        config = open(self.CONFIG, "w")
        for i in range(len(self.boilerplate)):
            config.write(self.boilerplate[i])
            config.write(str(self.contents[self.boilerplate[i]]) + "\n")
        config.close()
        print("Config updated")

CONFIG = __Options__()