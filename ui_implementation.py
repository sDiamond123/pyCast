import utils, map, pygame, player, math, ui, screen_writer, options

class Map_Screen(ui.UI_Composite):
     MAP_INDEX = 0
     DEFAULT_X_TRAV = 11
     DEFAULT_Y_TRAV = 8
     DEFAULT_W = 35

     def go_back(self):
         self.return_now = True

     def __init__ (self, internal_screen :pygame.Surface, map : map.Map, player : player.Player,draw_background = False, map_x = 0, map_y = 0, trav_x = DEFAULT_X_TRAV, trav_y = DEFAULT_Y_TRAV, cell_w = DEFAULT_W, has_buttons = False):
        self.phase = utils.Ptr(player.ang)
        self.player = player
        super().__init__(internal_screen, draw_background= draw_background)
        self.elements.append(ui.Map_Display(map_x, map_y, internal_screen, map, player, trav_w = trav_x, trav_h = trav_y, cell_w=cell_w, cell_h=cell_w))
        if has_buttons:
            size = utils.Ptr(16)
            cursor = utils.Ptr(0)
            self.elements.append(screen_writer.Text_Box(720,370,60,60,self.display,utils.Ptr("zoom\nin"),size,cursor,10,3,action = self.__direct_z_in__))
            self.elements.append(screen_writer.Text_Box(720,490,60,60,self.display,utils.Ptr("zoom\nout"),size,cursor,10,3,action = self.__direct_z_out__))
            self.elements.append(screen_writer.Text_Box(600,445,30,30,self.display,utils.Ptr("<"),size,cursor,10,3,action = self.__move_left__))
            self.elements.append(screen_writer.Text_Box(645,400,30,30,self.display,utils.Ptr("^"),size,cursor,10,3,action = self.__move_up__))
            self.elements.append(screen_writer.Text_Box(690,445,30,30,self.display,utils.Ptr(">"),size,cursor,10,3,action = self.__move_right__))
            self.elements.append(screen_writer.Text_Box(645,490,30,30,self.display,utils.Ptr("v"),size,cursor,10,3,action = self.__move_down__))
            self.elements.append(screen_writer.Text_Button(15,15,100,40,self.display,utils.Ptr("'"+chr(utils.Key.INTERACT) + "'. Back"),utils.Ptr(20), action = self.go_back))
        self.return_now = False

     def update(self, mouse : utils.Mouse_Manager, keys):
        self.phase.value = self.player.ang
        super().update(mouse, keys)
        if self.return_now:
            self.return_now = False
            return True
        return False

     def map_zoom_out(self):
        self.elements[self.MAP_INDEX].map_zoom_out()

     def map_zoom_in(self):
        self.elements[self.MAP_INDEX].map_zoom_in()

     def __direct_z_in__ (self):
        self.elements[self.MAP_INDEX].__perform_z_in__()

     def __direct_z_out__ (self):
        self.elements[self.MAP_INDEX].__perform_z_out__()

     def __move_up__ (self):
        self.elements[self.MAP_INDEX].y_off -= 1
     def __move_down__ (self):
        self.elements[self.MAP_INDEX].y_off += 1
     def __move_left__ (self):
        self.elements[self.MAP_INDEX].x_off -= 1
     def __move_right__ (self):
        self.elements[self.MAP_INDEX].x_off += 1


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
        self.elements.append(screen_writer.FPS_UI(5,5,10,10,internal_screen, utils.Ptr(12)))
        self.player = player
        self.cur_wep = ""
        self.want_mouse = False
        
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
    ANG_DELTA = 0.002

    def load(self):
        self.control.update_game_state(self.control.GAME_STATES.LOAD)

    def reload_last_save(self):
        self.control.load_state(self.control.state)
        self.control.update_game_state(self.control.GAME_STATES.FPS)

    def exit_game(self):
        self.exit = True

    def cursor_up(self):
        self.cursor.value -= 1

    def cursor_down(self):
        self.cursor.value += 1

    def options(self):
        self.control.update_game_state(self.control.GAME_STATES.OPTIONS)

    def __init__ (self, display, control):
        super().__init__(display, draw_background=False)
        self.control = control
        test = open("data/config/letter.txt")
        text = utils.Ptr(test.readlines())
        test.close()
        size = utils.Ptr(12)
        self.cursor = utils.Ptr(3)
        self.phase = utils.Ptr(0)
        self.elements.append(ui.Rolling_Image(0,0,display.size[0], display.size[1],display, "/menu/main_menu.png",self.phase,fov = math.pi ))
        self.elements.append(screen_writer.Text_Button(15,15,300,80,display,utils.Ptr("Long's Word"),utils.Ptr(50),draw_border=False, color = (239,228,176)))
        self.elements.append(screen_writer.Text_Box(10,450,400,140,self.display,text,size,self.cursor,68,7))
        self.elements.append(ui.Button(420,450,30,30,display,self.cursor_up))
        self.elements.append(ui.Button(420,500,30,30,display,self.cursor_down))
        self.elements.append(ui.Element(595,330,195,260,display, color=ui.UI_Composite.DEFAULT_BACK))
        self.elements.append(screen_writer.Text_Button(605,340,175,40,display,utils.Ptr("1. New"),utils.Ptr(20), color = (155,130,15), activation_key=49))
        self.elements.append(screen_writer.Text_Button(605,390,175,40,display,utils.Ptr("2. Continue"),utils.Ptr(20), color = (155,130,15), activation_key=50, action = self.reload_last_save))
        self.elements.append(screen_writer.Text_Button(605,440,175,40,display,utils.Ptr("3. Load"),utils.Ptr(20), color = (155,130,15), activation_key=51,action=self.load))
        self.elements.append(screen_writer.Text_Button(605,490,175,40,display,utils.Ptr("4. Options"),utils.Ptr(20), color = (155,130,15), activation_key=52, action = self.options))
        self.elements.append(screen_writer.Text_Button(605,540,175,40,display,utils.Ptr("5. Exit Game"),utils.Ptr(20), color = (155,130,15), activation_key=53, action = self.exit_game))

    def update(self, mouse : utils.Mouse_Manager, keys):
         self.phase.value += self.ANG_DELTA
         self.phase.value = utils.normalize_angle(self.phase.value)
         super().update(mouse, keys)
        
class Splash_Screen (ui.UI_Composite):
    BASE_MESSAGE = "Press '" + chr(utils.Key.INTERACT) + "' or click here to start \n CHEAP CHEAP goes the Chick"
    CHICK = "data/config/little_bird_games.png"
    VERSION = "data/config/info.txt"

    def action(self):
        self.control.update_game_state(self.control.GAME_STATES.MENU)

    def __init__ (self, display, control):
        super().__init__(display, background_color="antiquewhite1")
        self.control = control
        self.text = utils.Ptr(self.BASE_MESSAGE)
        size = utils.Ptr(24)
        self.refresh = utils.Ptr(False)
        self.elements.append(ui.Still_Image(0,0,800,600,self.display,self.CHICK))
        self.elements.append(screen_writer.Text_Box(180,490,440,75,self.display,self.text,size,utils.Ptr(0),45,1,action = self.action, activation_key=utils.Key.INTERACT,update_text=self.refresh, color = (200,180,110), y_offset=-2, x_offset=35, border_width= 10))
        small_size = utils.Ptr(8)
        version = open(self.VERSION)
        info = utils.Ptr(version.readlines())
        version.close()
        self.elements.append(screen_writer.Text_Box(15,15,1,1,self.display,info,small_size,utils.Ptr(0),60,2,color = pygame.Color("antiquewhite2"),draw_border=False))
        

class Pause (ui.UI_Composite):
    def continue_play (self):
        self.control.last_state()

    def reload_last_save(self):
        self.control.load_state(self.control.state)
        self.control.update_game_state(self.control.GAME_STATES.FPS)

    def load(self):
        self.control.update_game_state(self.control.GAME_STATES.LOAD)

    def options(self):
        self.control.update_game_state(self.control.GAME_STATES.OPTIONS)

    def exit_game(self):
        self.exit = True

    def menu(self):
        self.control.update_game_state(self.control.GAME_STATES.MENU)

    def __init__ (self, display, control):
        super().__init__(display, draw_background=False)
        self.control = control
        self.elements.append(screen_writer.Text_Button(50,150,175,40,display,utils.Ptr("1. Return"),utils.Ptr(20), activation_key=49, action = self.continue_play))
        self.elements.append(screen_writer.Text_Button(50,200,175,40,display,utils.Ptr("2. Reload Save"),utils.Ptr(20), activation_key=50, action = self.reload_last_save))
        self.elements.append(screen_writer.Text_Button(50,250,175,40,display,utils.Ptr("3. Load"),utils.Ptr(20), activation_key=51,action=self.load))
        self.elements.append(screen_writer.Text_Button(50,300,175,40,display,utils.Ptr("4. Save"),utils.Ptr(20), activation_key=52))
        self.elements.append(screen_writer.Text_Button(50,350,175,40,display,utils.Ptr("5. Options"),utils.Ptr(20), activation_key=53, action = self.options))
        self.elements.append(screen_writer.Text_Button(50,400,175,40,display,utils.Ptr("6. Main Menu"),utils.Ptr(20), activation_key=54,action=self.menu))
        self.elements.append(screen_writer.Text_Button(50,450,175,40,display,utils.Ptr("7. Exit Game"),utils.Ptr(20), activation_key=55, action=self.exit_game))
        self.exit = False

class Load (ui.UI_Composite):
    BUILT_IN = "data/state/built_in/saves.csv"
    CUSTOM = "data/state/saves/saves.csv"
    PATH = 2
    NAME = 1
    DESC = 3
    MAX = 3
    ID = 0
    NAME_W = 250
    NAME_H = 30
    DESC_H = 130
    DESC_W = 500
    DESC_CHAR = 40
    DESC_CHAR_H = 4
    BOX_SPACING = 10
    BOX_DELTA = BOX_SPACING + DESC_H + NAME_H
    BOX_Y0 = 80
    BOX_X0 = 50
    NAME_SIZE = utils.Ptr(20)
    DESC_SIZE = utils.Ptr(16)
    DEFAULT_NAME = utils.Ptr("N/A")
    DEFAULT_TEXT = utils.Ptr("---")
    DESC_COLOR = pygame.Color("bisque3")
    NAME_COLOR = pygame.Color("bisque4")
    LOAD = " <= LOAD"

    def __name__ (self, id, name, i):
        base = str(id) + ": " + name
        if i == 0:
            base += self.LOAD
        return base

    def update_text(self):
        for i in range (self.max):
            self.update_txt[i].value = True
            self.update_name[i].value = True
            if i + self.cursor < len(self.lines) and self.cursor >= 1:
                  self.text[i].value = self.lines[i + self.cursor ][self.DESC]
                  self.name[i].value = self.__name__(self.lines[i + self.cursor ][self.ID], self.lines[i + self.cursor ][self.NAME], i)
            else:
                self.text[i].value = self.DEFAULT_TEXT.value
                self.name[i].value = self.DEFAULT_NAME.value

    def down(self):
        self.cursor = utils.clamp_addition(self.cursor, 1, len(self.lines) - 1,1)
        self.update_text()

    def up(self):
        self.cursor = utils.clamp_addition(self.cursor, -1, len(self.lines) - 1,1)
        self.update_text()

    def return_play (self):
        self.control.last_state()

    def __load__ (self, i):
        if self.cursor + i>= 1 and self.cursor  +i < len(self.lines):
            self.control.load_state(self.lines[self.cursor + i][self.PATH])
            self.control.update_game_state(self.control.GAME_STATES.FPS)

    def load(self):
        self.__load__(0)

    def __init__ (self, display, control, path = BUILT_IN, max_display = MAX):
        super().__init__(display, background_color=(59,54,48))
        self.lines = []
        self.text = []
        self.name = []
        self.control = control
        self.cursor = 1
        self.max = max_display
        self.update_txt = []
        self.update_name = []
        self.lines = utils.bottomless_csv_load(path)
        self.elements.append(screen_writer.Text_Button(15,15,175,40,display,utils.Ptr("'"+chr(utils.Key.MAP) + "'. Back"),utils.Ptr(20), activation_key=utils.Key.MAP, action = self.return_play))
        self.elements.append(screen_writer.Text_Button(600,300,175,40,display,utils.Ptr("'"+chr(utils.Key.BACK) + "'. Down"),utils.Ptr(20), activation_key=utils.Key.BACK, action = self.down))
        self.elements.append(screen_writer.Text_Button(600,200,175,40,display,utils.Ptr("'"+chr(utils.Key.FORWARD) + "'. Up"),utils.Ptr(20), activation_key=utils.Key.FORWARD, action = self.up))
        self.elements.append(screen_writer.Text_Button(600,250,175,40,display,utils.Ptr("'"+chr(utils.Key.INTERACT) + "'. Load TOP"),utils.Ptr(20), activation_key=utils.Key.INTERACT, action = self.load))
        for i in range(self.max):
            self.update_txt.append(utils.Ptr(False))
            self.update_name.append(utils.Ptr(False))
            if i + self.cursor < len(self.lines) and self.cursor >= 1:
                  self.text.append(utils.Ptr(self.lines[i + self.cursor][self.DESC]))
                  self.name.append(utils.Ptr(self.__name__(self.lines[i + self.cursor ][self.ID], self.lines[i + self.cursor ][self.NAME], i)))
            else:
                self.text.append(self.DEFAULT_TEXT)
                self.name.append(self.DEFAULT_NAME)
            self.elements.append(screen_writer.Text_Box(self.BOX_X0, self.BOX_Y0 + self.BOX_DELTA * i, self.NAME_W, self.NAME_H, display,self.name[i],self.NAME_SIZE,utils.Ptr(0),self.DESC_CHAR, 1 ,color=self.NAME_COLOR, border_width= 0, update_text=self.update_name[i], action=self.__load__, activation_key= 49 + i, args = i))
            self.elements.append(screen_writer.Text_Box(self.BOX_X0, self.BOX_Y0 + self.BOX_DELTA * i + self.NAME_H,self.DESC_W, self.DESC_H, display,self.text[i],self.DESC_SIZE,utils.Ptr(0),self.DESC_CHAR, self.DESC_W, color=self.DESC_COLOR, update_text=self.update_txt[i], action=self.__load__, activation_key= 49 + i, args = i))

class Options(ui.UI_Heirarchy):
    def return_play (self):
        self.control.last_state()
    
    CONFIG_ID = 0
    BINDS_ID = 1

    def __init__(self, ext_disp : pygame.Surface, control):
        super().__init__(ext_disp,True,pygame.Color("bisque3"))
        self.control = control
        self.sub_composites.append(Config_Menu(125,25,ext_disp))
        self.sub_composites.append(Binds_Menu(125,25,ext_disp))
        self.elements.append(screen_writer.Text_Button(10,10,110,40,ext_disp,utils.Ptr("'"+chr(utils.Key.MAP) + "'. Back"),utils.Ptr(20), activation_key=utils.Key.MAP, action = self.return_play))
        self.elements.append(screen_writer.Text_Button(10,60,110,40,ext_disp,utils.Ptr("GRAPHICS"),utils.Ptr(20), action = self.focus, args=self.CONFIG_ID))
        self.elements.append(screen_writer.Text_Button(10,110,110,40,ext_disp,utils.Ptr("BINDS"),utils.Ptr(20),  action = self.focus,args=self.BINDS_ID))
        

class Binds_Menu (ui.UI_Sub_Screen):
    WIDTH = 650
    HEIGHT = 550
    TEXT_SIZE = utils.Ptr(12)
    TITLE_SIZE = utils.Ptr(20)
    BUTTON_W = 70
    BUTTON_H = 50
    RED = (150,0,0)

    def __changed_UI__ (self):
        options.CONFIG.contents[options.CONFIG.PROF_NAME].value = "CUSTOM"

    def __increment_x__(self, delta):
        options.CONFIG.contents[options.CONFIG.X_SENSE].value = utils.clamp_addition(options.CONFIG.contents[options.CONFIG.X_SENSE].value, delta, utils.Mouse_Manager.MOUSE_FACTOR,0)
        self.__changed_UI__()

    def __increment_y__(self, delta):
        options.CONFIG.contents[options.CONFIG.Y_SENSE].value = utils.clamp_addition(options.CONFIG.contents[options.CONFIG.Y_SENSE].value, delta, utils.Mouse_Manager.MOUSE_FACTOR,0)
        self.__changed_UI__()

    def __init__ (self, x, y, ext_display: pygame.surface):
        super().__init__(x,y,self.WIDTH,self.HEIGHT,ext_display,pygame.Color("bisque4"),False,True)
        self.elements.append(screen_writer.Text_Button(self.x + 250,self.y,0, 0, ext_display,utils.Ptr("MOUSE Sensitivity"),self.TITLE_SIZE,y_offset=-5))
        self.elements.append(screen_writer.Text_Button(self.x + 20,self.y + 30,0, 0, ext_display,utils.Ptr("X"),self.TITLE_SIZE, text_color=self.RED))
        self.elements.append(screen_writer.Text_Button(self.x + 20,self.y+ 90,0, 0, ext_display,utils.Ptr("Y"),self.TITLE_SIZE, text_color=self.RED))
        self.elements.append(screen_writer.Text_Button(self.x + 310,self.y + 30,0, 0, ext_display,options.CONFIG.contents[options.CONFIG.X_SENSE],self.TITLE_SIZE))
        self.elements.append(screen_writer.Text_Button(self.x + 70,self.y + 30,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("-10"),self.TEXT_SIZE,action=self.__increment_x__,x_offset=5, y_offset=10, args = -10))
        self.elements.append(screen_writer.Text_Button(self.x + 150,self.y + 30,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("-5"),self.TEXT_SIZE,action=self.__increment_x__,x_offset=5, y_offset=10, args = -5))
        self.elements.append(screen_writer.Text_Button(self.x + 230,self.y + 30,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("-1"),self.TEXT_SIZE,action=self.__increment_x__,x_offset=5, y_offset=10, args = -1))
        self.elements.append(screen_writer.Text_Button(self.x + 390,self.y + 30,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("+1"),self.TEXT_SIZE,action=self.__increment_x__,x_offset=5, y_offset=10, args = 1))
        self.elements.append(screen_writer.Text_Button(self.x + 470,self.y + 30,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("+5"),self.TEXT_SIZE,action=self.__increment_x__,x_offset=5, y_offset=10, args = 5))
        self.elements.append(screen_writer.Text_Button(self.x + 550,self.y + 30,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("+10"),self.TEXT_SIZE,action=self.__increment_x__,x_offset=5, y_offset=10, args = 10))
        self.elements.append(screen_writer.Text_Button(self.x + 310,self.y + 90,0, 0, ext_display,options.CONFIG.contents[options.CONFIG.Y_SENSE],self.TITLE_SIZE))
        self.elements.append(screen_writer.Text_Button(self.x + 70,self.y + 90,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("-10"),self.TEXT_SIZE,action=self.__increment_y__,x_offset=5, y_offset=10, args = -10))
        self.elements.append(screen_writer.Text_Button(self.x + 150,self.y + 90,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("-5"),self.TEXT_SIZE,action=self.__increment_y__,x_offset=5, y_offset=10, args = -5))
        self.elements.append(screen_writer.Text_Button(self.x + 230,self.y + 90,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("-1"),self.TEXT_SIZE,action=self.__increment_y__,x_offset=5, y_offset=10, args = -1))
        self.elements.append(screen_writer.Text_Button(self.x + 390,self.y + 90,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("+1"),self.TEXT_SIZE,action=self.__increment_y__,x_offset=5, y_offset=10, args = 1))
        self.elements.append(screen_writer.Text_Button(self.x + 470,self.y + 90,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("+5"),self.TEXT_SIZE,action=self.__increment_y__,x_offset=5, y_offset=10, args = 5))
        self.elements.append(screen_writer.Text_Button(self.x + 550,self.y + 90,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("+10"),self.TEXT_SIZE,action=self.__increment_y__,x_offset=5, y_offset=10, args = 10))
        
        # save changes
        self.elements.append(screen_writer.Text_Button(self.x + 300,self.y + 475,self.BUTTON_W,self.BUTTON_H,ext_display,utils.Ptr("SAVE"),self.TEXT_SIZE,action= options.CONFIG.save_config,x_offset=12, y_offset=10))

class Config_Menu (ui.UI_Sub_Screen):
    WIDTH = 650
    HEIGHT = 550
    TEXT_SIZE = utils.Ptr(12)
    TITLE_SIZE = utils.Ptr(20)
    BUTTON_W = 70
    BUTTON_H = 50
    RED = (150,0,0)

    def __changed_UI__ (self):
        options.CONFIG.contents[options.CONFIG.PROF_NAME].value = "CUSTOM"

    def __init__ (self, x, y, ext_display: pygame.surface):
        super().__init__(x,y,self.WIDTH,self.HEIGHT,ext_display,pygame.Color("bisque4"),True,True)
        # load profiles
        self.elements.append(screen_writer.Text_Button(self.x + 5,self.y,0, 0, ext_display,utils.Ptr("PROFILE:"),self.TITLE_SIZE))
        self.elements.append(screen_writer.Text_Button(self.x + 100,self.y,0, 0, ext_display,options.CONFIG.contents[options.CONFIG.PROF_NAME],self.TITLE_SIZE, text_color=self.RED))
        self.elements.append(screen_writer.Text_Button(self.x + 10,self.y + 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Nasa"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.NASA))
        self.elements.append(screen_writer.Text_Button(self.x + 90,self.y + 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("High"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.HIGH))
        self.elements.append(screen_writer.Text_Button(self.x + 170,self.y + 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Medium"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.MED))
        self.elements.append(screen_writer.Text_Button(self.x + 250,self.y + 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Low"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.LOW))
        self.elements.append(screen_writer.Text_Button(self.x + 330,self.y + 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Potato"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.POTATO))
        self.elements.append(screen_writer.Text_Button(self.x + 410,self.y + 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Current"),self.TEXT_SIZE,action=options.CONFIG.load_config,x_offset=5, y_offset=10))
        self.elements.append(screen_writer.Text_Button(self.x + 490,self.y + 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Default"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.DEFAULT))
        # save changes
        self.elements.append(screen_writer.Text_Button(self.x + 300,self.y + 475,self.BUTTON_W,self.BUTTON_H,ext_display,utils.Ptr("SAVE"),self.TEXT_SIZE,action= options.CONFIG.save_config,x_offset=12, y_offset=10))
        