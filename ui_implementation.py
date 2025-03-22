import utils, map, pygame, player, math, ui, screen_writer

class Map_Screen(ui.UI_Composite):
     MAP_INDEX = 0
     DEFAULT_X_TRAV = 11
     DEFAULT_Y_TRAV = 8
     DEFAULT_W = 35

     def __init__ (self, internal_screen :pygame.Surface, map : map.Map, player : player.Player,draw_background = False, map_x = 0, map_y = 0, trav_x = DEFAULT_X_TRAV, trav_y = DEFAULT_Y_TRAV, cell_w = DEFAULT_W):
        self.phase = utils.Ptr(player.ang)
        self.player = player
        super().__init__(internal_screen, draw_background= draw_background)
        self.elements.append(ui.Map_Display(map_x, map_y, internal_screen, map, player, trav_w = trav_x, trav_h = trav_y, cell_w=cell_w, cell_h=cell_w))


     def update(self, mouse : utils.Mouse_Manager, keys):
        self.phase.value = self.player.ang
        super().update(mouse, keys)

     def map_zoom_out(self):
        self.elements[self.MAP_INDEX].map_zoom_out()

     def map_zoom_in(self):
        self.elements[self.MAP_INDEX].map_zoom_in()


class HUD(Map_Screen):
    #map
    MAP_X = 600
    MAP_Y = 20
    DEFAULT_X_TRAV = 4
    DEFAULT_Y_TRAV = 3
    #compass
    COMPASS_X = 300
    COMPASS_Y = 540
    COMPASS_W = 275
    COMPASS_H = 44
    COMPASS_PATH = "/compass/compass_scroll.bmp"
    #h_bar
    HEALTH_X = 15
    HEALTH_Y = 480
    HEALTH_W = 150
    HEALTH_H = 30
    #cross_hair
    CROSS_SIZE = 6
    CROSS_SPACING = 0
    CROSS_COLOR = "hot pink"
    #a_bar
    AMMO_X = 15
    AMMO_Y = 515
    AMMO_W = 150
    AMMO_H = 30
    AMMO_DELTA_Y = 35
    AMMO_FILLED = (200, 200, 0)
    MAG_INDEX = 2
    AMMO_INDEX = 3
    
    
    def __init__ (self, internal_screen :pygame.Surface, map : map.Map, player : player.Player):
        self.phase = utils.Ptr(player.ang)
        super().__init__(internal_screen, map, player, draw_background= False, map_x=self.MAP_X, map_y=self.MAP_Y,   trav_x=self.DEFAULT_X_TRAV, trav_y=self.DEFAULT_Y_TRAV, cell_w=20)
        # add in all ui elements
        self.elements.append(ui.Bar(self.HEALTH_X, self.HEALTH_Y, self.HEALTH_W, self.HEALTH_H, internal_screen, player.h))
        state = player.get_weapon_state()
        self.elements.append(ui.Bar(self.AMMO_X, self.AMMO_Y, self.AMMO_W, self.AMMO_H, internal_screen, state[0], filled_color=self.AMMO_FILLED))
        self.elements.append(ui.Bar(self.AMMO_X, self.AMMO_Y + self.AMMO_DELTA_Y, self.AMMO_W, self.AMMO_H, internal_screen, state[1], filled_color = self.AMMO_FILLED))
        self.elements.append(ui.Rolling_Image(self.COMPASS_X, self.COMPASS_Y, self.COMPASS_W, self.COMPASS_H, internal_screen, self.COMPASS_PATH, self.phase, phase=math.pi, draw_border = True, border_width= 2))
        self.elements.append(ui.Mouse_Cursor(0,0,self.CROSS_SIZE,self.CROSS_SPACING,internal_screen, color = self.CROSS_COLOR))
        self.player = player
        self.cur_wep = ""
        
    def __update_weapons__ (self):
         state = self.player.get_weapon_state()
         if self.player.weapon != None:
            if self.player.weapon.name != self.cur_wep:
                self.cur_wep = self.player.weapon.name
                self.elements[self.MAG_INDEX].data = state[0]
                self.elements[self.AMMO_INDEX].data = state[1]
         elif self.cur_wep != "":
             self.cur_wep = ""

    def update(self, mouse : utils.Mouse_Manager, keys):
         self.__update_weapons__()
         super().update(mouse, keys)
        
class Main_Menu (ui.UI_Composite):
    def action(self):
        self.control.game_state = self.control.GAME_STATES.FPS

    def __init__ (self, display, control):
        super().__init__(display)
        self.control = control
        self.elements.append(ui.Interactable_Element(20,50,40,30,display))
        self.elements.append(ui.Interactable_Element(70,50,50,40,display, border_width= 15, color= (123, 89, 20)))
        self.elements.append(ui.Interactable_Element(70,135,100,100,display,draw_border=False, color = (255,230,15)))
        self.elements.append(ui.Button(400,200,30,30,display,self.action))
        test = open("data/config/letter.txt")
        text = utils.Ptr(test.readlines())
        test.close()
        size = utils.Ptr(12)
        cursor = utils.Ptr(2)
        self.elements.append(screen_writer.Text_Box(200,450,100,100,self.display,text,size,cursor,13,4,action = self.action, activation_key=49))