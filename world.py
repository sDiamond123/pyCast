import pygame,utils,map,camera,math,ui_implementation,game_object,player, ui, enum

class World:
    PATH = "data/state/"
    STATE_W = 2
    STATE_H = 7
    LINES_PER_OBJ = 6
    OBJ_W = 2
    GAME_STATES = enum.Enum('State', [('LOAD', 8), ('SPLASH_SCREEN', 7),('FPS', 1), ('MENU', 2), ('DIALOUGE', 3), ("PLAYER_MENU", 4), ("PAUSE_MENU", 5), ("MAP", 6)])

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

    

    def __init__(self, out_display, w, h, i_w, i_h, entry_state, cam_settings):
        #set entry state
        self.game_state = self.GAME_STATES.SPLASH_SCREEN
        # set up internal display and external screen
        self.out_display = out_display
        self.ext_w = w
        self.ext_h = h
        self.internal_w = i_w
        self.internal_h = i_h
        self.internal_display = pygame.Surface((i_w, i_h))
        self.prev_states = []
        self.UI = {}
        self.fps_fov = cam_settings[0]
        self.fps_rays = cam_settings[1]
        self.draw_dist = cam_settings[2]
        # load into our game state
        self.state = entry_state
        #change_latter
        self.UI[self.GAME_STATES.MENU.value] = ui_implementation.Main_Menu(self.internal_display, self)
        self.UI[self.GAME_STATES.SPLASH_SCREEN.value] = ui_implementation.Splash_Screen(self.internal_display, self)
        self.UI[self.GAME_STATES.PAUSE_MENU.value] = ui_implementation.Pause(self.internal_display, self)
        self.UI[self.GAME_STATES.LOAD.value] = ui_implementation.Load(self.internal_display,self)

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
        self.object_count = self.state_data[5][1]
        if self.object_count > 0:
            self.state_objects = [None] * self.state_data[5][1]
            objects = utils.csv_load(self.PATH + self.state_data[5][0], self.OBJ_W, self.LINES_PER_OBJ * self.object_count)
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
                               self.fps_rays, math.radians(self.fps_fov), 
                               self.draw_dist, self.state_objects)
        self.UI[self.GAME_STATES.FPS.value] =ui_implementation.HUD(self.internal_display, self.m, self.p)
        self.UI[self.GAME_STATES.MAP.value] = ui_implementation.Map_Screen(self.internal_display,self.m, self.p, has_buttons=True)
        self.p.load_inv(self.state_data[6][0])
        # print state
        print("Successfully loaded save: " + self.state)

    def __map_controls__ (self, keys, mouse):
        if keys[utils.Key.M_ZOOM_OUT]:
           self.UI[self.GAME_STATES.MAP.value].map_zoom_out()
        elif keys[utils.Key.M_ZOOM_IN]:
            self.UI[self.GAME_STATES.MAP.value].map_zoom_in()
        if keys[utils.Key.INTERACT]:
            self.last_state()
        if keys[utils.Key.FORWARD]:
           self.UI[self.GAME_STATES.MAP.value].__move_up__()
        if keys[utils.Key.BACK]:
            self.UI[self.GAME_STATES.MAP.value].__move_down__()
        if keys[utils.Key.S_RIGHT]:
             self.UI[self.GAME_STATES.MAP.value].__move_right__()
        if keys[utils.Key.S_LEFT]:
             self.UI[self.GAME_STATES.MAP.value].__move_left__()
        if keys[utils.Key.PAUSE]:
            self.update_game_state(self.GAME_STATES.PAUSE_MENU)

    def __fps_controls__ (self, keys, mouse):
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
        if keys[utils.Key.SHOOT]:
            z = (0.5 - (mouse.poll_rel()[1])) * mouse.sensetivity[1]
            self.p.shoot(self.state_objects,self.base_sprites, self.m, z)
        if keys[utils.Key.RELOAD]:
            self.p.reload()
        if keys[utils.Key.M_ZOOM_OUT]:
           self.UI[self.GAME_STATES.FPS.value].map_zoom_out()
        elif keys[utils.Key.M_ZOOM_IN]:
            self.UI[self.GAME_STATES.FPS.value].map_zoom_in()
        if keys[utils.Key.CYCLE_NEXT]:
            self.p.cycle_next()
        elif keys[utils.Key.CYCLE_PREV]:
            self.p.cycle_prev()
        if keys[utils.Key.JUMP]:
            player.z = 50
        elif keys[utils.Key.CROUCH]:
            player.z = -50
        elif keys[utils.Key.MAP]:
            self.update_game_state(self.GAME_STATES.MAP)
        else:
            player.z = 0 
        if keys[utils.Key.PAUSE]:
            self.update_game_state(self.GAME_STATES.PAUSE_MENU)
        # update mouse
        if (mouse.alive):
            player.turn(mouse.poll_delta()[0])

    def __general_controls__ (self, keys, mouse):
        # update keys
        if keys[utils.Key.EXIT]:
            return False
        if keys[utils.Key.FREE_LOOK]:
            mouse.toggle()
        mouse.update()
        self.mouse = mouse
        return True

    def update (self, keys, mouse : utils.Mouse_Manager):
        check = self.__general_controls__(keys, mouse)
        if not check:
            return check
        if self.game_state == self.GAME_STATES.FPS:
            # check if your dead
            if self.p.health() <= 0:
                self.update_game_state(self.GAME_STATES.MENU)
                # autoload last save
                self.load_state(self.state)
                return True
            # update controls
            self.__fps_controls__(keys, mouse)
            self.p.update()
            to_pop = []
            #update objects
            for i in range(len(self.state_objects)):
                object = self.state_objects[i]
                object.update(self.p, self.state_objects, self.m)
                if object.health() <= 0:
                    #print("reaping: " + object.name)
                    to_pop.append(i)
            #reap dead objects
            for dead in reversed(to_pop):
                self.state_objects.pop(dead)
        elif self.game_state == self.GAME_STATES.MAP:
            self.__map_controls__(keys, mouse)

        # update UI
        if self.game_state.value in self.UI and self.UI[self.game_state.value] != None:
            if (self.UI[self.game_state.value].update(mouse, keys)):
                self.last_state()
            if (self.UI[self.game_state.value].exit):
                return False
        return True

    def render (self):
        if self.game_state == self.GAME_STATES.FPS:
            # render 
            self.c.render()
            #push camera's display onto main display
            self.internal_display.blit(self.c.external_surface)

        # render UI
        if self.game_state.value in self.UI and self.UI[self.game_state.value] != None:
            self.UI[self.game_state.value].render()


        # output rendered frame (push to external display)
        pygame.transform.smoothscale(self.internal_display, self.out_display.size, self.out_display)

    MAX_SAVED_STATES = 10

    def update_game_state (self, new_state):
        self.prev_states.append(self.game_state)
        self.game_state = new_state
        print("switching state to: " + self.game_state.name)
        if len(self.prev_states) > self.MAX_SAVED_STATES:
            self.prev_states.pop(0)
        if self.UI[self.game_state.value].want_mouse:
            if self.mouse.alive:
                self.mouse.toggle()
        elif not self.mouse.alive:
            self.mouse.toggle()

    def last_state(self):
        if len(self.prev_states) > 0:
            self.game_state = self.prev_states.pop()
        else:
            self.game_state = self.GAME_STATES.MENU
        print("reverting state to: " + self.game_state.name)
        if self.UI[self.game_state.value].want_mouse:
            if self.mouse.alive:
                self.mouse.toggle()
        elif not self.mouse.alive:
            self.mouse.toggle()