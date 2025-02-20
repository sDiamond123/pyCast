import pygame
import utils
import map
import camera
import math
import texture

class World:
    PATH = "data\state\\"
    STATE_W = 2
    STATE_H = 6

    state = None
    state_data = []
    internal_w = 0
    internal_h = 0
    internal_display = None
    out_display = None
    ext_w = 0
    ext_h = 0
    
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
        self.compass = texture.RollingTexture("\\compass\compass_scroll.bmp", math.pi, math.pi , 250, 32)
        # load into our game state
        self.load_state(entry_state)

    def load_state(self, state):
        self.state = state
        self.state_data = utils.csv_load(self.PATH+state, self.STATE_W, self.STATE_H)
        # load map
        self.m = map.Map(self.state_data[0][0])
        # load player
        self.p = utils.Player(utils.convert_csv_to_float(self.state_data,2), 
                              utils.convert_csv_to_float(self.state_data,3),
                              utils.convert_csv_to_float(self.state_data,1))
        # load camera
        self.c = camera.Camera(self.m, self.p, self.internal_w, self.internal_h, 
                               self.state_data[4][0], math.radians(self.state_data[5][0]), 
                               self.state_data[5][1])
        # print state
        print("Successfully loaded state: " + self.state)

    def update (self, keys):
        # update keys
        player = self.p
        world = self.m
        if keys[utils.Key.FORWARD]:
            player.move(world, 0.1, 0)
        if keys[utils.Key.BACK]:
            player.move(world, -0.1, 0)
        if keys[utils.Key.S_RIGHT]:
            player.move(world, 0, 0.1)
        if keys[utils.Key.S_LEFT]:
            player.move(world, 0, -0.1)
        if keys[utils.Key.TURN_L]:
            player.turn(-0.04)
        if keys[utils.Key.TURN_R]:
            player.turn(0.04)
        if keys[utils.Key.EXIT]:
            return False
        if keys[utils.Key.JUMP]:
            player.z = 50
        elif keys[utils.Key.CROUCH]:
            player.z = -50
        else:
            player.z = 0 
        return True

    def render (self):
        # render 
        self.c.render()
        #push camera's display onto main display
        self.internal_display.blit(self.c.external_surface)
        # render minimap
        self.m.rendermap (self.internal_display, self.p, 4, 3, 600, 20, 20, 20)
        # render compass
        self.compass.render(self.p.ang)
        self.internal_display.blit(self.compass.external_screen, (300,560))
        # output rendered frame (push to external display)
        pygame.transform.smoothscale(self.internal_display, (self.ext_w,self.ext_h), self.out_display)