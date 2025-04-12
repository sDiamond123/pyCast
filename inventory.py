import utils, item, weapon
from log import LOG as log


class Inventory():
    def __init__ (self, file):
        data = utils.bottomless_csv_load(file)
        self.items = {}
        self.__load_inv__(data)
        self.current = 0

    def __load_inv__ (self, data):
        cur_item = None
        attr = ""
        in_attr = False
        i = 0
        for line in data:
            if "ITEM" in line:
                in_attr = False
                if "WEAPON" in line:
                    if "SCATTER" in line:
                        cur_item = weapon.Scatter_Gun(line[2], line[3])
                    elif "BASIC" in line:
                        cur_item = weapon.Weapon(line[2], line[3])
                elif "MAG" in line:
                    #item = weapon.Weapon(line[2], line[3])
                    pass
                else:
                    cur_item = item.Item(line[2], line[3])
                self.items[(cur_item.name, i)] = cur_item
                i+=1
                log.write(cur_item.name + " added to inventory")
            elif "FLAG" in line:
                in_attr = False
                if "EQUIPED" in line:
                    cur_item.is_equiped = True
            else:
                if (in_attr):
                    cur_item.attr[attr] = utils.convert_csv_to_float([line], 0)
                else:
                    attr = line[0]
                in_attr = not in_attr

    def get_equiped(self):
        for item in self.items:
            if self.items[item].is_equiped:
                self.equiped = self.items[item]
                if (self.equiped.need_to_load):
                    self.equiped.load()
                return self.items[item]
        return None
    
    def __get_current__(self):
        for item in self.items:
            if item[1] == self.current:
                if (self.equiped != None):
                    self.equiped.is_equiped = False
                self.equiped = self.items[item]
                self.equiped.is_equiped = True 
                if (self.equiped.need_to_load):
                    self.equiped.load()
                log.write("equiped: " + self.equiped.name)
                return self.items[item]
        return None
    
    def cycle_next(self):
        self.current += 1
        if self.current >= len(self.items):
            self.current = 0
        return self.__get_current__()

    def cycle_prev(self):
        self.current -= 1
        if self.current <0:
            self.current = len(self.items) - 1
        return self.__get_current__()