import utils, game_object
class Player (utils.Obj_Vector):
    COOL_DOWN = 200

    def __init__(self, x, y, ang, h):
        super().__init__(x,y,ang,h)
        self.shoot_timer = utils.Timed_Toggle(self.COOL_DOWN)

    def update(self):
        self.shoot_timer.update()

    def shoot(self,objects, sprites, map):
        if (self.shoot_timer.clock):
            f_ball = game_object.spawn_objs(self.x, self.y, self.ang, "data/objects/fire_ball", sprites, "CAST", 5)
            f_ball.__move__(map, 0.3, 0)
            objects.append(f_ball)