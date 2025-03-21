import utils, map, pygame, player, texture, math, ui

class HUD(ui.UI_Composite):
    MAP_X = 600
    MAP_Y = 20
    COMPASS_X = 300
    COMPASS_Y = 560
    COMPASS_W = 250
    COMPASS_H = 32
    COMPASS_PATH = "/compass/compass_scroll.bmp"
   
    #h_bar
    h_x = 15
    h_y = 480
    h_w = 150
    h_h = 30
    #cross_hair
    cross_size = 6
    cross_spacing = 0
    cross_color = "hot pink"
    #a_bar
    a_x = 15
    a_y = 515
    a_w = 150
    a_h = 30
    delta_a_y = 35
    a_filled = (200, 200, 0)
    MAG_INDEX = 1
    AMMO_INDEX = 2
    MAP_INDEX = 4
    #font
    pygame.font.init()
    FONT = pygame.font.SysFont('Comic Sans MS', 30)
    
    def __init__ (self, internal_screen :pygame.Surface, map : map.Map, player : player.Player):
        self.phase = utils.Ptr(player.ang)
        super().__init__(internal_screen, draw_background= False)
        # add in all ui elements
        self.elements.append(ui.Bar(self.h_x, self.h_y, self.h_w, self.h_h, internal_screen, player.h))
        state = player.get_weapon_state()
        self.elements.append(ui.Bar(self.a_x, self.a_y, self.a_w, self.a_h, internal_screen, state[0], filled_color=self.a_filled))
        self.elements.append(ui.Bar(self.a_x, self.a_y + self.delta_a_y, self.a_w, self.a_h, internal_screen, state[1], filled_color = self.a_filled))
        self.elements.append(ui.Rolling_Image(self.COMPASS_X, self.COMPASS_Y, self.COMPASS_W, self.COMPASS_H, internal_screen, self.COMPASS_PATH, self.phase, phase=math.pi, draw_border = True, border_width= 5))
        self.elements.append(ui.Map_Display(self.MAP_X, self.MAP_Y, internal_screen, map, player))
        self.elements.append(ui.Mouse_Cursor(0,0,self.cross_size,self.cross_spacing,internal_screen, color = self.cross_color))
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
         self.__render_ch__ = mouse.alive
         self.__update_weapons__()
         self.phase.value = self.player.ang
         super().update(mouse, keys)
        

    def map_zoom_out(self):
        self.elements[self.MAP_INDEX].map_zoom_out()

    def map_zoom_in(self):
        self.elements[self.MAP_INDEX].map_zoom_in()

       



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