import utils, inventory, weapon




class Player (utils.Obj_Vector):
    COOL_DOWN = 400
    MAX_HEALTH = 100
    
    def __init__(self, x, y, ang, h):
        super().__init__(x,y,ang,h)
        self.weapon = None
        self.cycle_timer = utils.Timed_Toggle(self.COOL_DOWN)
    
    def load_inv(self, file):
        self.inventory = inventory.Inventory(file)
        self.weapon = self.inventory.get_equiped()
        
    def reload(self):
        if (self.weapon != None):
            self.weapon.reload()

    def cycle_next(self):
        if (self.cycle_timer.clock):
            self.weapon = self.inventory.cycle_next()

    def cycle_prev(self):
        if (self.cycle_timer.clock):
            self.weapon = self.inventory.cycle_prev()

    def update(self):
        if (self.weapon != None):
            self.weapon.update()
        self.cycle_timer.update()

    def shoot(self,objects, sprites, map, z):
        if (self.weapon != None):
            self.weapon.shoot(self.x, self.y, self.ang, objects, sprites, map, z)

    def get_weapon_state(self):
        if self.weapon != None:
            return (self.weapon.magazine.in_mag, self.weapon.magazine.size, self.weapon.magazine.total, self.weapon.magazine.max)
        return (1,1,1,1)