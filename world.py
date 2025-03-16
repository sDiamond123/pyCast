import pygame
import utils
import map
import camera
import math
import hud
import game_object
import player

class World:
    PATH = "data/state/"
    STATE_W = 2
    STATE_H = 9
    LINES_PER_OBJ = 6
    OBJ_W = 2

    state = None
    state_data = []
    internal_w = 0
    internal_h = 0
    internal_display = None
    out_display = None
    ext_w = 0
    ext_h = 0
    state_objects = []
    object_count = 0
    base_sprites = {}
    
    # game objects
    p = None
    m = None
    c = None
    compass = None
    move_speed = 0.1
    truen_speed = 0.4

    

    def __init__(self, out_display, w, h, i_w, i_h, entry_state):
        # set up internal display and external screen
        self.out_display = out_display
        self.ext_w = w
        self.ext_h = h
        self.internal_w = i_w
        self.internal_h = i_h
        self.internal_display = pygame.Surface((i_w, i_h))
        # load into our game state
        self.load_state(entry_state)
        #change_latter

    def load_state(self, state):
        self.state = state
        self.state_data = utils.csv_load(self.PATH+state, self.STATE_W, self.STATE_H)
        # load map
        self.m = map.Map(self.state_data[0][0])
        # load player
        self.p = player.Player(utils.convert_csv_to_float(self.state_data,2), 
                              utils.convert_csv_to_float(self.state_data,3),
                              utils.convert_csv_to_float(self.state_data,1),
                              utils.convert_csv_to_float(self.state_data,4))
        print("Successfully spawned player: " + str(self.p))
        
        #load game objects
        self.object_count = self.state_data[7][1]
        if self.object_count > 0:
            self.state_objects = [None] * self.state_data[7][1]
            objects = utils.csv_load(self.PATH + self.state_data[7][0], self.OBJ_W, self.LINES_PER_OBJ * self.object_count)
            line = 0
            for i in range (self.object_count):
                x = utils.convert_csv_to_float(objects, line)
                y = utils.convert_csv_to_float(objects, line + 1)
                ang = utils.convert_csv_to_float(objects, line + 2)
                health = utils.convert_csv_to_float(objects, line +3)
                state = objects[line + 4][0]
                self.state_objects[i] = game_object.spawn_objs(x, y, ang, objects[line + 5][0], self.base_sprites, state, health)
                line += self.LINES_PER_OBJ
        else:
            self.state_objects = []
            self.base_sprites = {}
         # load camera
        self.c = camera.Camera(self.m, self.p, self.internal_w, self.internal_h, 
                               self.state_data[5][0], math.radians(self.state_data[6][0]), 
                               self.state_data[6][1], self.state_objects)
        self.hud = hud.HUD(self.internal_display, self.m, self.p)
        self.p.load_inv(self.state_data[8][0])
        # print state
        print("Successfully loaded state: " + self.state)

    def __controls__ (self, keys, mouse):

        # update keys
        player = self.p
        world = self.m
        if keys[utils.Key.FORWARD]:
            player.move_with_minimum(world, 0.1, 0,0.25)
        if keys[utils.Key.BACK]:
            player.move_with_minimum(world, -0.1, 0,0.25)
        if keys[utils.Key.S_RIGHT]:
            player.move_with_minimum(world, 0, 0.1,0.25)
        if keys[utils.Key.S_LEFT]:
            player.move_with_minimum(world, 0, -0.1,0.25)
        if keys[utils.Key.TURN_L]:
            player.turn(-0.04)
        if keys[utils.Key.TURN_R]:
            player.turn(0.04)
        if keys[utils.Key.EXIT]:
            return False
        if keys[utils.Key.SHOOT]:
            z = (0.5 - (mouse.poll_rel()[1])) * mouse.sensetivity[1]
            self.p.shoot(self.state_objects,self.base_sprites, self.m, z)
        if keys[utils.Key.RELOAD]:
            self.p.reload()
        if keys[utils.Key.M_ZOOM_OUT]:
           self.hud.map_zoom_out()
        elif keys[utils.Key.M_ZOOM_IN]:
            self.hud.map_zoom_in()
        if keys[utils.Key.CYCLE_NEXT]:
            self.p.cycle_next()
        elif keys[utils.Key.CYCLE_PREV]:
            self.p.cycle_prev()
        if keys[utils.Key.JUMP]:
            player.z = 50
        elif keys[utils.Key.CROUCH]:
            player.z = -50
        else:
            player.z = 0 
        if keys[utils.Key.FREE_LOOK]:
            mouse.toggle()

        mouse.update()
        if (mouse.alive):
            player.turn(mouse.poll_delta()[0])
        self.mouse = mouse

        
        return True

    def update (self, keys, mouse):
        self.hud.update(mouse)

        check = self.__controls__(keys, mouse)
        if not check:
            return check
        
        self.p.update()

        to_pop = []
        #update objects
        for i in range(len(self.state_objects)):
            object = self.state_objects[i]
            object.update(self.p, self.state_objects, self.m)
            if object.health() <= 0:
                print("reaping: " + object.name)
                to_pop.append(i)
        #reap dead objects
        for dead in reversed(to_pop):
            self.state_objects.pop(dead)

        return True

    def render (self):
        # render 
        self.c.render()
        #push camera's display onto main display
        self.internal_display.blit(self.c.external_surface)
        # render hud
        self.hud.render()
        # output rendered frame (push to external display)
        pygame.transform.smoothscale(self.internal_display, self.out_display.size, self.out_display)