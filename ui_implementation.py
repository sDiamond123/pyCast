import utils, map, pygame, player, math, ui, screen_writer, options, sheet, options, normalize
from log import LOG as log

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
            self.elements.append(screen_writer.Text_Box(720,370,60,60,self.display,utils.Ptr("zoom\nin"),size,cursor,10,3,action = self.__direct_z_in__,writer=screen_writer.GOTHIC))
            self.elements.append(screen_writer.Text_Box(720,490,60,60,self.display,utils.Ptr("zoom\nout"),size,cursor,10,3,action = self.__direct_z_out__,writer=screen_writer.GOTHIC))
            self.elements.append(screen_writer.Text_Box(600,445,30,30,self.display,utils.Ptr("<"),size,cursor,10,3,action = self.__move_left__))
            self.elements.append(screen_writer.Text_Box(645,400,30,30,self.display,utils.Ptr("^"),size,cursor,10,3,action = self.__move_up__))
            self.elements.append(screen_writer.Text_Box(690,445,30,30,self.display,utils.Ptr(">"),size,cursor,10,3,action = self.__move_right__))
            self.elements.append(screen_writer.Text_Box(645,490,30,30,self.display,utils.Ptr("v"),size,cursor,10,3,action = self.__move_down__))
            self.elements.append(screen_writer.Text_Button(15,15,100,40,self.display,utils.Ptr("'"+chr(options.Key.INTERACT) + "'. Back"),utils.Ptr(20), action = self.go_back))
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
        self.elements.append(sheet.char_sheet(100,100,300,300,internal_screen))
        
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

    def extras(self):
        self.control.update_game_state(self.control.GAME_STATES.EXTRAS)

    def reload_last_save(self):
        self.control.load_state(self.control.state)
        self.control.update_game_state(self.control.GAME_STATES.FPS)

    def new_game(self):
        self.control.update_game_state(self.control.GAME_STATES.DIALOUGE)
        self.control. set_dialouge_entry_point(0)

    def exit_game(self):
        self.control.update_game_state(self.control.GAME_STATES.EXIT)

    def options(self):
        self.control.update_game_state(self.control.GAME_STATES.OPTIONS)

    def __init__ (self, display, control):
        super().__init__(display, draw_background=False)
        self.control = control
        test = open("data/config/letter.txt")
        text = utils.Ptr(test.readlines())
        test.close()
        size = utils.Ptr(12)
        self.cursor = utils.Ptr(0)
        self.phase = utils.Ptr(0)
        self.elements.append(ui.Rolling_Image(0,0,display.size[0], display.size[1],display, "/menu/main_menu.png",self.phase,fov = math.pi ))
        self.elements.append(screen_writer.Text_Button(15,15,0,0,display,utils.Ptr("Long's Word"),utils.Ptr(50),draw_border=False, text_color = (0, 70, 20),writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Box(10,450,400,140,self.display,text,size,self.cursor,65,7))
        self.elements.append(ui.Element(595,280,195,310,display, color=(20,20,20)))
        self.elements.append(screen_writer.Text_Button(605,290,175,40,display,utils.Ptr("1. New"),utils.Ptr(20), color = (155,130,15), activation_key=49, action = self.new_game,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(605,340,175,40,display,utils.Ptr("2. Continue"),utils.Ptr(20), color = (155,130,15), activation_key=50, action = self.reload_last_save,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(605,390,175,40,display,utils.Ptr("3. Load"),utils.Ptr(20), color = (155,130,15), activation_key=51,action=self.load,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(605,440,175,40,display,utils.Ptr("4. Settings"),utils.Ptr(20), color = (155,130,15), activation_key=52, action = self.options,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(605,490,175,40,display,utils.Ptr("5. Extras"),utils.Ptr(20), color = (155,130,15), activation_key=53, action = self.extras,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(605,540,175,40,display,utils.Ptr("6. Exit Game"),utils.Ptr(20), color = (155,130,15), activation_key=54, action = self.exit_game,writer=screen_writer.GOTHIC))

    def update(self, mouse : utils.Mouse_Manager, keys):
         self.phase.value += self.ANG_DELTA
         self.phase.value = utils.normalize_angle(self.phase.value)
         super().update(mouse, keys)
        
class Splash_Screen (ui.UI_Composite):
    BASE_MESSAGE = "Press '" + chr(options.Key.INTERACT) + "' or click here to start \n CHEAP CHEAP"
    CHICK = "data/config/little_bird.png"
    VERSION = "data/config/info.txt"

    def action(self):
        self.control.update_game_state(self.control.GAME_STATES.MENU)

    def __init__ (self, display, control):
        super().__init__(display, draw_background=False)
        self.control = control
        self.text = utils.Ptr(self.BASE_MESSAGE)
        size = utils.Ptr(36)
        self.refresh = utils.Ptr(False)
        self.elements.append(ui.Still_Image(0,0,800,600,self.display,self.CHICK))
        self.elements.append(screen_writer.Text_Box(180,490,440,75,self.display,self.text,size,utils.Ptr(0),45,1,action = self.action, activation_key=options.Key.INTERACT,update_text=self.refresh, color = (200,180,110), y_offset=-2, border_width= 10,writer=screen_writer.GOTHIC,has_slider=False))
        small_size = utils.Ptr(8)
        version = open(self.VERSION)
        info = utils.Ptr(version.readlines())
        version.close()
        self.elements.append(screen_writer.Text_Box(15,15,1,1,self.display,info,small_size,utils.Ptr(0),60,2,color = pygame.Color("antiquewhite2"),draw_border=False,has_slider=False))


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
        self.control.update_game_state(self.control.GAME_STATES.EXIT)

    def menu(self):
        self.control.update_game_state(self.control.GAME_STATES.MENU)

    def __init__ (self, display, control):
        super().__init__(display, draw_background=False)
        self.control = control
        self.elements.append(screen_writer.Text_Button(50,150,175,40,display,utils.Ptr("1. Return"),utils.Ptr(20), activation_key=49, action = self.continue_play,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(50,200,175,40,display,utils.Ptr("2. Reload Save"),utils.Ptr(20), activation_key=50, action = self.reload_last_save,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(50,250,175,40,display,utils.Ptr("3. Load"),utils.Ptr(20), activation_key=51,action=self.load,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(50,300,175,40,display,utils.Ptr("4. Save"),utils.Ptr(20), activation_key=52,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(50,350,175,40,display,utils.Ptr("5. Options"),utils.Ptr(20), activation_key=53, action = self.options,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(50,400,175,40,display,utils.Ptr("6. Main Menu"),utils.Ptr(20), activation_key=54,action=self.menu,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(50,450,175,40,display,utils.Ptr("7. Exit Game"),utils.Ptr(20), activation_key=55, action=self.exit_game,writer=screen_writer.GOTHIC))
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
    DESC_W = 630
    DESC_CHAR = 80
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
            if i + self.cursor.value < len(self.lines) and self.cursor.value >= 1:
                  self.text[i].value = self.lines[i + self.cursor.value ][self.DESC]
                  self.name[i].value = self.__name__(self.lines[i + self.cursor.value ][self.ID], self.lines[i + self.cursor.value ][self.NAME], i)
            else:
                self.text[i].value = self.DEFAULT_TEXT.value
                self.name[i].value = self.DEFAULT_NAME.value

    def down(self):
        self.cursor.value = utils.clamp_addition(self.cursor.value, 1, len(self.lines) - 1,1)
        self.update_text()

    def up(self):
        self.cursor.value = utils.clamp_addition(self.cursor.value, -1, len(self.lines) - 1,1)
        self.update_text()

    def return_play (self):
        self.control.last_state()

    def __load__ (self, i):
        if self.cursor.value + i>= 1 and self.cursor.value  +i < len(self.lines):
            self.control.load_state(self.lines[self.cursor.value + i][self.PATH])
            self.control.update_game_state(self.control.GAME_STATES.FPS)

    def load(self):
        self.__load__(0)

    def update(self, mouse, keys):
        super().update(mouse, keys)
        if self.has_scroll and self.elements[2 * self.max+4].moved:
            self.update_text()
        for element in self.elements:
            if element.state != utils.Mouse_State.UNDEFINED:
                return False
        if (mouse.mw < 0):
            self.down()
        elif (mouse.mw > 0):
            self.up()
        return False
        

    def __init__ (self, display, control, path = BUILT_IN, max_display = MAX):
        super().__init__(display, background_color=(59,54,48))
        self.lines = []
        self.text = []
        self.name = []
        self.control = control
        self.cursor = utils.Ptr(1)
        self.max = max_display
        self.update_txt = []
        self.update_name = []
        self.lines = utils.bottomless_csv_load(path)
        self.elements.append(screen_writer.Text_Button(15,15,150,40,display,utils.Ptr("'"+chr(options.Key.MAP) + "'. Back"),utils.Ptr(20), activation_key=options.Key.MAP, action = self.return_play))
        self.elements.append(screen_writer.Text_Button(510,15,150,40,display,utils.Ptr("'"+chr(options.Key.BACK) + "'. Down"),utils.Ptr(20), activation_key=options.Key.BACK, action = self.down))
        self.elements.append(screen_writer.Text_Button(345,15,150,40,display,utils.Ptr("'"+chr(options.Key.FORWARD) + "'. Up"),utils.Ptr(20), activation_key=options.Key.FORWARD, action = self.up))
        self.elements.append(screen_writer.Text_Button(180,15,150,40,display,utils.Ptr("'"+chr(options.Key.INTERACT) + "'. Load TOP"),utils.Ptr(20), activation_key=options.Key.INTERACT, action = self.load))
        for i in range(self.max):
            self.update_txt.append(utils.Ptr(False))
            self.update_name.append(utils.Ptr(False))
            if i + self.cursor.value < len(self.lines) and self.cursor.value >= 1:
                  self.text.append(utils.Ptr(self.lines[i + self.cursor.value][self.DESC]))
                  self.name.append(utils.Ptr(self.__name__(self.lines[i + self.cursor.value ][self.ID], self.lines[i + self.cursor.value ][self.NAME], i)))
            else:
                self.text.append(self.DEFAULT_TEXT)
                self.name.append(self.DEFAULT_NAME)
            self.elements.append(screen_writer.Text_Box(self.BOX_X0, self.BOX_Y0 + self.BOX_DELTA * i, self.NAME_W, self.NAME_H, display,self.name[i],self.NAME_SIZE,utils.Ptr(0),self.DESC_CHAR, 1 ,color=self.NAME_COLOR, border_width= 0, update_text=self.update_name[i], action=self.__load__, activation_key= 49 + i, args = i))
            self.elements.append(screen_writer.Text_Box(self.BOX_X0, self.BOX_Y0 + self.BOX_DELTA * i + self.NAME_H,self.DESC_W, self.DESC_H, display,self.text[i],self.DESC_SIZE,utils.Ptr(0),self.DESC_CHAR, self.DESC_W, color=self.DESC_COLOR, update_text=self.update_txt[i], action=self.__load__, activation_key= 49 + i, args = i))
        if len(self.lines) > self.max:
            self.has_scroll = True
            self.elements .append(ui.Slider(700,110,32,450,display,current=self.cursor,min = 1, max = len(self.lines),phantom_dist=64))
        else:
            self.has_scroll = False
class Options(ui.UI_Heirarchy):
    def return_play (self):
        self.control.last_state()
    
    CONFIG_ID = 0
    BINDS_ID = 1
    CONSOLE_ID = 2

    def __init__(self, ext_disp : pygame.Surface, control):
        super().__init__(ext_disp,True,pygame.Color("bisque3"))
        self.control = control
        self.sub_composites.append(Config_Menu(125,25,ext_disp))
        self.sub_composites.append(Binds_Menu(125,25,ext_disp, control))
        self.sub_composites.append(Console(125,25,ext_disp, control))
        self.elements.append(screen_writer.Text_Button(10,10,110,40,ext_disp,utils.Ptr("'"+chr(options.Key.MAP) + "'. Back"),utils.Ptr(20), activation_key=options.Key.MAP, action = self.return_play))
        self.elements.append(screen_writer.Text_Button(10,60,110,40,ext_disp,utils.Ptr("OPTIONS"),utils.Ptr(20), action = self.focus, args=self.CONFIG_ID))
        self.elements.append(screen_writer.Text_Button(10,110,110,40,ext_disp,utils.Ptr("BINDS"),utils.Ptr(20),  action = self.focus,args=self.BINDS_ID))
        self.elements.append(screen_writer.Text_Button(10,160,110,40,ext_disp,utils.Ptr("CONSOLE"),utils.Ptr(20),  action = self.focus,args=self.CONSOLE_ID))
        self.focus(self.CONFIG_ID)
        

    def update(self, mouse, keys):
        if self.sub_composites[self.CONSOLE_ID].render_elements:
            self.elements[0].key_lock = True
        elif self.elements[0].key_lock:
            self.elements[0].key_lock = False
        return super().update(mouse, keys)

   


class Binds_Menu (ui.UI_Sub_Screen):
    WIDTH = 650
    HEIGHT = 550
    TEXT_SIZE = utils.Ptr(12)
    TITLE_SIZE = utils.Ptr(20)
    BUTTON_W = 70
    BUTTON_H = 50
    RED = (150,0,0)
    

    def __update_menu__(self):
        for i in range(len(options.Key.BINDS)):
            bind = options.Key.BINDS[i]
            self.lines[i] = (bind[options.Key.LABEL] + ": " + options.Key.PRINT_TABLE[bind[options.Key.KEY]][options.Key.PT_PRINT_LOWER])
        self.elements[1].update_contents(self.lines)

    def __modify_key__ (self, index):
        index += self.elements[1].cursor.value
        log.write("modifying key:" + str(index) + "->" + str(options.Key.BINDS[index]))
        self.control.modify_key_bind(index)

    def __load_def__ (self):
        options.Key.load_defaults()
        self.__update_menu__()

    def __load_cur__ (self):
        options.Key.load_current()
        self.__update_menu__()


    def __init__ (self, x, y, ext_display: pygame.surface, control):
        super().__init__(x,y,self.WIDTH,self.HEIGHT,ext_display,pygame.Color("bisque4"),False,True)
        self.control = control
        self.lines = []
        for bind in options.Key.BINDS:
            self.lines.append(bind[options.Key.LABEL] + ": " + options.Key.PRINT_TABLE[bind[options.Key.KEY]][options.Key.PT_PRINT_LOWER])
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 75,self.y+ normalize.SCALE_FACTOR_Y * 10,0, 0, ext_display,utils.Ptr("KEYBINDS (click to change):"),self.TITLE_SIZE,scale = False))
        self.elements.append(screen_writer.Text_Menu(self.x + normalize.SCALE_FACTOR_X * 110, self.y + normalize.SCALE_FACTOR_Y * 50, 465, 440,ext_display,self.lines,max_display=10,scale=False,draw_background=False,box_color=ui.Element.DEFAULT_GREY, action=self.__modify_key__))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X *300,self.y + normalize.SCALE_FACTOR_Y *490,self.BUTTON_W,self.BUTTON_H,ext_display,utils.Ptr("SAVE"),self.TEXT_SIZE,action= options.Key.save_binds,x_offset=12, y_offset=10,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X *110,self.y + normalize.SCALE_FACTOR_Y *490,self.BUTTON_W,self.BUTTON_H,ext_display,utils.Ptr("RELOAD"),self.TEXT_SIZE,action= self.__load_cur__,x_offset=5, y_offset=10,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + self.w - normalize.SCALE_FACTOR_X *180,self.y + normalize.SCALE_FACTOR_Y *490,self.BUTTON_W,self.BUTTON_H,ext_display,utils.Ptr("DEFAULT"),self.TEXT_SIZE,action= self.__load_def__,x_offset=1, y_offset=10,scale = False))

class Key_Prompt (ui.UI_Composite):
    TEXT_SIZE = utils.Ptr(20)
    TITLE_SIZE = utils.Ptr(36)

    def __update__(self):
        log.write("setting " + self.label.value + " to " + options.Key.PRINT_TABLE[self.key][options.Key.PT_PRINT_LOWER])
        options.Key.BINDS[self.bind][options.Key.KEY] = self.key
        self.control.last_state()
        if (self.key != self.prev ):
           # pure fucking spaghetti
           menu =  self.control.UI[self.control.GAME_STATES.OPTIONS.value]
           menu.sub_composites[menu.BINDS_ID].__update_menu__() 

    def __clear__(self):
        self.key = -1
        self.text.value = "PRESS KEY\n " + options.Key.PRINT_TABLE[self.key][options.Key.PT_PRINT_LOWER]

    def __default__(self):
        self.key = self.data[options.Key.DEF_KEY]
        self.text.value = "PRESS KEY\n " + options.Key.PRINT_TABLE[self.key][options.Key.PT_PRINT_LOWER]

    def __prev__(self):
        self.key = self.prev
        self.text.value = "PRESS KEY\n " + options.Key.PRINT_TABLE[self.key][options.Key.PT_PRINT_LOWER]

    def __init__(self, control, ext_disp, key_index = 0, background_color=ui.UI_Composite.DEFAULT_BACK):
        super().__init__(ext_disp, False, background_color)
        self.label = utils.Ptr("")
        self.current_key = utils.Ptr("")
        self.default_key = utils.Ptr("")
        self.text = utils.Ptr("")
        self.control = control
        self.set_key(key_index)
        self.elements.append(ui.Element(200,100,400,300,ext_disp,pygame.Color("bisque3")))
        self.elements.append(screen_writer.Text_Button(210,350,100,40,ext_disp,utils.Ptr("cancel"),self.TEXT_SIZE,action=control.last_state))
        self.elements.append(screen_writer.Text_Button(350,350,100,40,ext_disp,utils.Ptr("update"),self.TEXT_SIZE,action=self.__update__))
        self.elements.append(screen_writer.Text_Button(490,350,100,40,ext_disp,utils.Ptr("clear"),self.TEXT_SIZE,action=self.__clear__))
        self.elements.append(screen_writer.Text_Button(410,110,180,40,ext_disp,self.default_key,self.TEXT_SIZE,action=self.__default__))
        self.elements.append(screen_writer.Text_Button(200,50,300,50,ext_disp,self.label,self.TITLE_SIZE,text_color=(150,0,0), color=pygame.Color("bisque2"), y_offset= - 6))
        self.elements.append(screen_writer.Text_Button(210,110,180,40,ext_disp,self.current_key,self.TEXT_SIZE, action = self.__prev__))
        #self.elements.append(ui.Element(210,160,380,180,ext_disp,(30,30,30)))
        self.elements.append(screen_writer.Text_Button(210,160,380,180,ext_disp,self.text,self.TITLE_SIZE,text_color=(150,0,0),color=(30,30,30),x_offset=20, y_offset=20))

    def set_key(self, i):
        self.bind = i
        self.data = options.Key.BINDS[i]
        self.key = self.data[options.Key.KEY]
        self.prev = self.key
        self.label.value = self.data[options.Key.LABEL]
        self.current_key.value = "Currently: " + options.Key.PRINT_TABLE[self.key][options.Key.PT_PRINT_LOWER]
        self.default_key.value = "Default: " + options.Key.PRINT_TABLE[self.data[options.Key.DEF_KEY]][options.Key.PT_PRINT_LOWER]
        self.text.value = "PRESS KEY\n "  + options.Key.PRINT_TABLE[self.key][options.Key.PT_PRINT_LOWER]

    def update(self, mouse, keys):
        poll = options.TERM.poll_keys(keys,raw=True)
        if (poll != None):
            self.key = poll[0]
            self.text.value = "PRESS KEY\n " + poll[1]
        return super().update(mouse, keys)

class Config_Menu (ui.UI_Sub_Screen):
    WIDTH = 650
    HEIGHT = 550
    TEXT_SIZE = utils.Ptr(12)
    TITLE_SIZE = utils.Ptr(20)
    BUTTON_W = 70
    BUTTON_H = 50
    RED = (150,0,0)

    def __check_w_res_(self):
        self.w_res.value = str(options.CONFIG.contents[options.CONFIG.W]) + "x" + str(options.CONFIG.contents[options.CONFIG.H]) 
    
    def __check_I_res_(self):
        self.I_res.value = str(options.CONFIG.contents[options.CONFIG.I_W]) + "x" + str(options.CONFIG.contents[options.CONFIG.I_H]) 
    

    def __update_window_resolution(self, scale):
        options.CONFIG.contents[options.CONFIG.W] = scale[0]
        options.CONFIG.contents[options.CONFIG.H] = scale[1]
        self.__changed_UI__()

    def __update_I_resolution(self, scale):
        options.CONFIG.contents[options.CONFIG.I_W] = scale[0]
        options.CONFIG.contents[options.CONFIG.I_H] = scale[1]
        self.__changed_UI__()

    def __changed_UI__ (self):
        options.CONFIG.contents[options.CONFIG.PROF_NAME].value = "CUSTOM"

    def __update_fs__ (self):
        options.CONFIG.contents[options.CONFIG.FULLSCREEN] = not options.CONFIG.contents[options.CONFIG.FULLSCREEN]
        self.__changed_UI__()

    def __init__ (self, x, y, ext_display: pygame.surface):
        super().__init__(x,y,self.WIDTH,self.HEIGHT,ext_display,pygame.Color("bisque4"),True,True)
        # load profiles
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 20,self.y,0, 0, ext_display,utils.Ptr("PROFILE:"),self.TITLE_SIZE,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X *120,self.y,0, 0, ext_display,options.CONFIG.contents[options.CONFIG.PROF_NAME],self.TITLE_SIZE, text_color=self.RED,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X *30,self.y + normalize.SCALE_FACTOR_Y * 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Nasa"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.NASA,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 110,self.y + normalize.SCALE_FACTOR_Y * 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("High"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.HIGH,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 190,self.y + normalize.SCALE_FACTOR_Y * 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Medium"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.MED,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 270,self.y + normalize.SCALE_FACTOR_Y * 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Low"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.LOW,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 350,self.y + normalize.SCALE_FACTOR_Y * 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Potato"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.POTATO,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 430,self.y + normalize.SCALE_FACTOR_Y * 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Current"),self.TEXT_SIZE,action=options.CONFIG.load_config,x_offset=5, y_offset=10,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 510,self.y + normalize.SCALE_FACTOR_Y * 40,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("Default"),self.TEXT_SIZE,action=options.CONFIG.load_custom,x_offset=5, y_offset=10, args = options.CONFIG.DEFAULT,scale = False))
        # set camerasettings
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 20,self.y +normalize.SCALE_FACTOR_Y * 90,0, 0, ext_display,utils.Ptr("FPS:"),self.TITLE_SIZE, text_color=self.RED,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 20,self.y+normalize.SCALE_FACTOR_Y * 120,0, 0, ext_display,utils.Ptr("FOV:"),self.TITLE_SIZE, text_color=self.RED,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 80,self.y +normalize.SCALE_FACTOR_Y * 90,0, 0, ext_display,options.CONFIG.contents[options.CONFIG.FPS],self.TITLE_SIZE,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 80,self.y +normalize.SCALE_FACTOR_Y * 120,0, 0, ext_display,options.CONFIG.contents[options.CONFIG.FOV],self.TITLE_SIZE,scale = False))
        self.elements.append(ui.Slider(self.x + 200 * normalize.SCALE_FACTOR_X, self.y + 105 * normalize.SCALE_FACTOR_Y,400,10,ext_display,False,current = options.CONFIG.contents[options.CONFIG.FPS],max=243, min = 20,scale=False, step = 2))
        self.elements.append(ui.Slider(self.x + 200 * normalize.SCALE_FACTOR_X, self.y + 135 * normalize.SCALE_FACTOR_Y,400,10,ext_display,False,current = options.CONFIG.contents[options.CONFIG.FOV],max=180, min = 30,scale=False, step = 3))
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 20,self.y +normalize.SCALE_FACTOR_Y * 150,0, 0, ext_display,utils.Ptr("RAYS:"),self.TITLE_SIZE, text_color=self.RED,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 20,self.y+normalize.SCALE_FACTOR_Y * 180,0, 0, ext_display,utils.Ptr("DRAW_DIST:"),self.TITLE_SIZE, text_color=self.RED,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 80,self.y +normalize.SCALE_FACTOR_Y * 150,0, 0, ext_display,options.CONFIG.contents[options.CONFIG.RAYS],self.TITLE_SIZE,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 140,self.y +normalize.SCALE_FACTOR_Y * 180,0, 0, ext_display,options.CONFIG.contents[options.CONFIG.DRAW_DIST],self.TITLE_SIZE,scale = False))
        self.elements.append(ui.Slider(self.x + 200 * normalize.SCALE_FACTOR_X, self.y + 165 * normalize.SCALE_FACTOR_Y,400,10,ext_display,False,current = options.CONFIG.contents[options.CONFIG.RAYS],max=1024, min = 16,scale=False, step = 8, phantom_dist=64))
        self.elements.append(ui.Slider(self.x + 200 * normalize.SCALE_FACTOR_X, self.y + 195 * normalize.SCALE_FACTOR_Y,400,10,ext_display,False,current = options.CONFIG.contents[options.CONFIG.DRAW_DIST],max=17, min = 1,scale=False, step = 1, phantom_dist= 64))
        # mouse 
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 20,self.y +normalize.SCALE_FACTOR_Y * 210,0, 0, ext_display,utils.Ptr("MOUSE X SENSETIVITY:"),self.TITLE_SIZE, text_color=self.RED,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 20,self.y+normalize.SCALE_FACTOR_Y * 240,0, 0, ext_display,utils.Ptr("MOUSE Y SENSETIVITY:"),self.TITLE_SIZE, text_color=self.RED,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 240,self.y +normalize.SCALE_FACTOR_Y * 210,0, 0, ext_display,options.CONFIG.contents[options.CONFIG.X_SENSE],self.TITLE_SIZE,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 240,self.y +normalize.SCALE_FACTOR_Y * 240,0, 0, ext_display,options.CONFIG.contents[options.CONFIG.Y_SENSE],self.TITLE_SIZE,scale = False))
        self.elements.append(ui.Slider(self.x + 300 * normalize.SCALE_FACTOR_X, self.y + 225 * normalize.SCALE_FACTOR_Y,300,10,ext_display,False,current = options.CONFIG.contents[options.CONFIG.X_SENSE],max=300, min = 1,scale=False, step = 5, phantom_dist=64))
        self.elements.append(ui.Slider(self.x + 300 * normalize.SCALE_FACTOR_X, self.y + 255 * normalize.SCALE_FACTOR_Y,300,10,ext_display,False,current = options.CONFIG.contents[options.CONFIG.Y_SENSE],max=300, min = 1,scale=False, step = 5,phantom_dist=64))
       # update window resolution
        self.w_res = utils.Ptr("")
        self.__check_w_res_()
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 20,self.y + normalize.SCALE_FACTOR_Y * 270,0, 0, ext_display,utils.Ptr("RESOLUTION:"),self.TITLE_SIZE,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X *160,self.y + normalize.SCALE_FACTOR_Y * 270,0, 0, ext_display,self.w_res,self.TITLE_SIZE, text_color=self.RED,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X *30,self.y + normalize.SCALE_FACTOR_Y * 310,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("400x300"),self.TEXT_SIZE,action=self.__update_window_resolution,x_offset=5, y_offset=10, args = (400, 300),scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 110,self.y + normalize.SCALE_FACTOR_Y * 310,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("640x480"),self.TEXT_SIZE,action=self.__update_window_resolution,x_offset=5, y_offset=10, args = (640, 480),scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 190,self.y + normalize.SCALE_FACTOR_Y * 310,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("800x600"),self.TEXT_SIZE,action=self.__update_window_resolution,x_offset=5, y_offset=10, args =(800, 600),scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 270,self.y + normalize.SCALE_FACTOR_Y * 310,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("1024x768"),self.TEXT_SIZE,action=self.__update_window_resolution,x_offset=-1, y_offset=10, args = (1024,768),scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 350,self.y + normalize.SCALE_FACTOR_Y * 310,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("1152x870"),self.TEXT_SIZE,action=self.__update_window_resolution,x_offset=-1, y_offset=10, args = (1152,870),scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 430,self.y + normalize.SCALE_FACTOR_Y * 310,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("1280x720"),self.TEXT_SIZE,action=self.__update_window_resolution,x_offset=-1, y_offset=10, args = (1280, 720), scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 510,self.y + normalize.SCALE_FACTOR_Y * 310,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("2560x1440"),self.TEXT_SIZE,action=self.__update_window_resolution,x_offset=-1, y_offset=10, args = (2560,1440),scale = False))
         # set fullscreen
        self.fs = utils.Ptr(options.CONFIG.contents[options.CONFIG.FULLSCREEN])
        self.elements.append(screen_writer.Text_Button(self.x +normalize.SCALE_FACTOR_X * 20,self.y+normalize.SCALE_FACTOR_Y * 360,0, 0, ext_display,utils.Ptr("FULLSCREEN:"),self.TITLE_SIZE, text_color=self.RED,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X *160,self.y + normalize.SCALE_FACTOR_Y * 364,40, 30, ext_display,self.fs,self.TEXT_SIZE,action=self.__update_fs__,x_offset=0, y_offset=0,scale = False))
        # update internal resolution
        self.I_res = utils.Ptr("")
        self.__check_I_res_()
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 20,self.y + normalize.SCALE_FACTOR_Y * 390,0, 0, ext_display,utils.Ptr("UI RESOLUTION:"),self.TITLE_SIZE,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X *190,self.y + normalize.SCALE_FACTOR_Y * 390,0, 0, ext_display,self.I_res,self.TITLE_SIZE, text_color=self.RED,scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X *30,self.y + normalize.SCALE_FACTOR_Y * 430,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("400x300"),self.TEXT_SIZE,action=self.__update_I_resolution,x_offset=5, y_offset=10, args = (400, 300),scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 110,self.y + normalize.SCALE_FACTOR_Y * 430,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("640x480"),self.TEXT_SIZE,action=self.__update_I_resolution,x_offset=5, y_offset=10, args = (640, 480),scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 190,self.y + normalize.SCALE_FACTOR_Y * 430,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("800x600"),self.TEXT_SIZE,action=self.__update_I_resolution,x_offset=5, y_offset=10, args =(800, 600),scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 270,self.y + normalize.SCALE_FACTOR_Y * 430,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("1024x768"),self.TEXT_SIZE,action=self.__update_I_resolution,x_offset=-1, y_offset=10, args = (1024,768),scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 350,self.y + normalize.SCALE_FACTOR_Y * 430,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("1152x870"),self.TEXT_SIZE,action=self.__update_I_resolution,x_offset=-1, y_offset=10, args = (1152,870),scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 430,self.y + normalize.SCALE_FACTOR_Y * 430,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("1280x720"),self.TEXT_SIZE,action=self.__update_I_resolution,x_offset=-1, y_offset=10, args = (1280, 720), scale = False))
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X * 510,self.y + normalize.SCALE_FACTOR_Y * 430,self.BUTTON_W, self.BUTTON_H, ext_display,utils.Ptr("2560x1440"),self.TEXT_SIZE,action=self.__update_I_resolution,x_offset=-1, y_offset=10, args = (2560,1440),scale = False))
         # save changes
        self.elements.append(screen_writer.Text_Button(self.x + normalize.SCALE_FACTOR_X *300,self.y + normalize.SCALE_FACTOR_Y *490,self.BUTTON_W,self.BUTTON_H,ext_display,utils.Ptr("SAVE"),self.TEXT_SIZE,action= options.CONFIG.save_config,x_offset=12, y_offset=10,scale = False))

    def update(self, m_x, m_y, mouse, keys):
        self.fs.value = (options.CONFIG.contents[options.CONFIG.FULLSCREEN])
        self.__check_w_res_()
        self.__check_I_res_()
        return super().update(m_x, m_y, mouse, keys)
    
class Console (ui.UI_Sub_Screen):
    WIDTH = 650
    HEIGHT = 550
    TEXT_SIZE = utils.Ptr(12)
    TITLE_SIZE = utils.Ptr(20)
    BUTTON_W = 70
    BUTTON_H = 50

    def execute(self, task):
        self.elements[0].cursor.value += 1
        self.control.execute(task)

    def __init__ (self, x, y, ext_display: pygame.surface, control):
        super().__init__(x,y,self.WIDTH,self.HEIGHT,ext_display,pygame.Color("bisque4"),True,True)
        self.cursor = utils.Ptr(0)
        self.elements.append(screen_writer.Log(self.x +normalize.SCALE_FACTOR_X * 10, self.y +normalize.SCALE_FACTOR_Y * 10, self.w/normalize.SCALE_FACTOR_X-20, 440,ext_display,self.TEXT_SIZE,self.cursor,120,int(25 * normalize.SCALE_FACTOR_X),log.new, scale = False, color=(0,0,0), text_color=(50,200,50)))
        self.elements.append(screen_writer.Typewriter(self.x +normalize.SCALE_FACTOR_X * 10, self.y + normalize.SCALE_FACTOR_Y * 450,self.w/normalize.SCALE_FACTOR_X - 20, 90, ext_display,utils.Ptr("> "),self.TITLE_SIZE,utils.Ptr(0),50,int(3*normalize.SCALE_FACTOR_X),  color=(20,20,20), text_color=(50,200,50), action=self.execute, scale=False))
        self.control = control
        self.execute("help") 

class Death_Menu (ui.UI_Composite):

    def load(self):
        self.control.update_game_state(self.control.GAME_STATES.LOAD)

    def reload_last_save(self):
        self.control.load_state(self.control.state)
        self.control.update_game_state(self.control.GAME_STATES.FPS)

    def exit_game(self):
        self.control.update_game_state(self.control.GAME_STATES.EXIT)

    def options(self):
        self.control.update_game_state(self.control.GAME_STATES.OPTIONS)

    def main_menu(self):
        self.control.update_game_state(self.control.GAME_STATES.MENU)

    def __init__ (self, display, control):
        super().__init__(display, draw_background=False)
        self.control = control
        self.elements.append(screen_writer.Text_Button(150,80,500,50,display,utils.Ptr("YOU HAVE FALLEN"),utils.Ptr(50),draw_border=False, text_color = (20,20,20),writer=screen_writer.GOTHIC, color=pygame.Color("red"), y_offset= -5, x_offset= + 25))
        self.elements.append(ui.Element(300,150,200,270,display, color=(30,30,30)))
        self.elements.append(screen_writer.Text_Button(310,160,180,40,display,utils.Ptr("1. Last Save"),utils.Ptr(20), color = (155,130,15), activation_key=50, action = self.reload_last_save,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(310,210,180,40,display,utils.Ptr("2. Load"),utils.Ptr(20), color = (155,130,15), activation_key=51,action=self.load,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(310,260,180,40,display,utils.Ptr("3. Options"),utils.Ptr(20), color = (155,130,15), activation_key=52, action = self.options,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(310,310,180,40,display,utils.Ptr("4. Main Menu"),utils.Ptr(20), color = (155,130,15), activation_key=53, action = self.main_menu,writer=screen_writer.GOTHIC))
        self.elements.append(screen_writer.Text_Button(310,360,180,40,display,utils.Ptr("5. Exit Game"),utils.Ptr(20), color = (155,130,15), activation_key=54, action = self.exit_game,writer=screen_writer.GOTHIC))

class Exit_Popup (ui.UI_Composite):
    def continue_play (self):
        self.control.last_state()

    def exit_game(self):
        self.exit = True

    def __init__ (self, display, control):
        super().__init__(display, draw_background=False)
        self.control = control
        self.elements.append(screen_writer.Text_Button(350,200,100,50,display,utils.Ptr("Quit"),utils.Ptr(50),draw_border=False, color = (30,30,30),text_color = (155,130,15), y_offset= -5, x_offset= -2, writer=screen_writer.GOTHIC))
        self.elements.append(ui.Element(350,250,100,110,display, color=(30,30,30)))
        self.elements.append(screen_writer.Text_Button(360,260,80,40,display,utils.Ptr("\'Y\'es"),utils.Ptr(20), color = pygame.Color("red"), activation_key=ord('y'), action = self.exit_game,writer=screen_writer.GOTHIC, x_offset= 8))
        self.elements.append(screen_writer.Text_Button(360,310,80,40,display,utils.Ptr("\'N\'o"),utils.Ptr(20), color = pygame.Color("green"), activation_key=ord('n'), action = self.continue_play,writer=screen_writer.GOTHIC, x_offset= 15))
        self.exit = False
