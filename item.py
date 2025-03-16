class Item():
    DESCRIPTION = "/description.txt"
    ICON = "/icon.*"
    
    def __init__ (self, name, path):
        d_data = open(path + self.DESCRIPTION)
        self.description = d_data.read()
        d_data.close()
        self.is_equiped = False
        self.name = name
        self.attr = {}
        self.need_to_load = False

class Load_Item (Item):
    def __init__ (self, name, path):
        super().__init__(name, path)
        self.need_to_load = True
    
    def load(self):
        self.need_to_load = False

