import item, utils, math, random, game_object

class Magazine():
    def __init__ (self, name, size, total_rounds, rounds_loaded, max_rounds):
        self.name = name
        self.in_mag = utils.Partial(size, current=rounds_loaded)
        self.in_inv = utils.Partial(max_rounds, current=total_rounds)
        

    def fire(self):
        if (self.in_mag.current > 0):
            self.in_mag.update(-1)
    
    def reload(self):
        if self.in_inv.current > self.in_mag.max:
            self.in_inv.update(- self.in_mag.max)
            self.in_mag.update(abs = self.in_mag.max)
        else:
            self.in_mag.update(abs = self.in_inv.current)
            self.in_inv.update(abs = 0)


class Weapon(item.Load_Item):
    PROJECTILE = "data/objects/fire_ball"
    PROJECTILE_HEALTH = 10
    PROJECTILE_STATE = "CAST"
    DEV_FACTOR = 100
    META = "/meta.csv"
    OFFSET = 0.3

    def __init__ (self, name, path):
        super().__init__(name,path)
        data = utils.bottomless_csv_load(path + self.META)
        self.fire_rate = data[1][0]
        self.reload_rate = data[2][0]
        self.max_dev = data[3][0]/self.DEV_FACTOR
        self.attr["mag_size"] = data[4][0]
        self.shoot_timer = utils.Timed_Toggle(self.fire_rate)
        self.shoot_toggle = False
        self.reload_timer = None
        self.in_reload = False
    
    def load(self):
        self.magazine = Magazine(self.name, self.attr["mag_size"], self.attr["current_ammo"], self.attr["in_gun"], self.attr["max_ammo"])
        super().load()

    def reload(self):
        if not self.in_reload:
            self.magazine.in_mag.update(abs = -1)
            self.reload_timer = utils.Timed_Toggle(self.reload_rate)
            self.in_reload = True

    def update(self):
        if self.shoot_toggle:
            if(self.shoot_timer.update()):
                self.shoot_toggle = False
        if self.in_reload:
            if (self.reload_timer.update()):
                
                self.magazine.reload()
                self.reload_timer = None
                self.in_reload = False


    def __actual_shot__ (self,x, y,ang, objects, sprites, map, z):
        
        deviation = 0
        if self.max_dev > 0:
            deviation = math.pi * random.uniform(-self.max_dev, self.max_dev)
        f_ball = game_object.spawn_objs(x, y, ang + deviation, self.PROJECTILE, sprites, self.PROJECTILE_STATE, self.PROJECTILE_HEALTH)
        f_ball.delta_z = z
        f_ball.__move__(map,self.OFFSET, 0) 
        objects.append(f_ball)

    def shoot(self,x, y, ang ,objects, sprites, map, z):
        if not self.shoot_toggle:
            self.shoot_toggle = True
            self.shoot_timer = utils.Timed_Toggle(self.fire_rate)
            if (self.magazine.in_mag.current > 0):
                self.magazine.fire()
                self.__actual_shot__(x, y,ang, objects, sprites, map, z)

class Scatter_Gun(Weapon):
    PROJECTILE_STATE = "SCATTER"
    def __actual_shot__ (self,x, y,ang, objects, sprites, map, z):
        for i in range(self.attr["pellets"]):
            deviation = 0
            if self.max_dev > 0:
                deviation = math.pi * random.uniform(-self.max_dev, self.max_dev)
            f_ball = game_object.spawn_objs(x, y, ang + deviation, self.PROJECTILE, sprites, self.PROJECTILE_STATE, self.PROJECTILE_HEALTH)
            f_ball.delta_z = z
            f_ball.__move__(map,self.OFFSET, 0) 
            objects.append(f_ball)