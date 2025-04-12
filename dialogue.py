import ui, screen_writer, json, pygame, utils
from utils import Ptr as ptr
from database import DB as db
from log import LOG as log

class Talking_Head(ui.Still_Image):
    DEFAULT_IMG = "data/npc_profiles/empty/empty.png"
    ID = 0
    NAME = 1
    SENTIMENT = 2
    CUR_E_P = 3
    E_P_LIST = 4
    ATTB = 5
    IMG = 6
    
    IMG_INDEX = 0
    CUTOFF_INDEX = 1
    MIN_SENTIMENT = 0
    MAX_SENTIMENT = 100
    
    

    def __init__ (self, x, y, w, h, ext_display : pygame.surface, id,
                  p_button = ui.Still_Image.DEFAULT_MB, draw_border = False, color = ui.Element.DEFAULT_GREY, 
                  border_width = 0, activation_key = -1):
        self.data = db.get("*", "npc", ("id", id))[0]
        self.sentiment = self.data[self.SENTIMENT]
        self.name = self.data[self.NAME]
        self.id = id
        self.img_folder = self.data[self.IMG]
        self.img_metadata = utils.bottomless_csv_load(self.img_folder + "/meta.csv")
        self.img_name = ""
        self.w = w
        self.h = h
        self.show_img = True
        self.b_w = border_width
        self.bg_name = ""
        self.e_p = json.loads(self.data[self.E_P_LIST])
        self.update_sentiment(0)
        self.current_point = self.data[self.CUR_E_P]
        self.attr = json.loads(self.data[self.ATTB])
        super().__init__(x,y,w,h,ext_display,self.image,p_button,draw_border,color,border_width,activation_key)
        

    def get_img_id(self):
        img_n = self.DEFAULT_IMG
        for line in self.img_metadata:
            if self.sentiment > line[self.CUTOFF_INDEX]:
                break
            img_n = self.img_folder + "/" + line[self.IMG_INDEX]
        return img_n
    
    def set_e_p (self):
        for line in self.e_p:
            if (line["min"] <= self.sentiment and line["max"] > self.sentiment):
                self.current_point = line["entry_point"]

    def update_sentiment(self, delta):
        self.sentiment = utils.clamp_addition(self.sentiment, delta,self.MAX_SENTIMENT, self.MIN_SENTIMENT)
        new_id = self.get_img_id()
        if (new_id != self.img_name):
            self.img_name = new_id
            self.image = pygame.transform.scale(pygame.image.load(self.img_name), (self.w - 2 * self.b_w,self.h - 2 * self.b_w))
        self.set_e_p()

    def update_img(self, background, show_image):
        if (self.bg_name != background):
            self.bg_name = background
            self.background = pygame.transform.scale(pygame.image.load(background), (self.w - 2 * self.b_w,self.h - 2 * self.b_w))
        self.show_img = show_image

    def render (self):
         if self.draw_border:
             pygame.draw.rect(self.ext_display, self.__get_border_color(), (self.x, self.y, self.w, self.h))
         self.ext_display.blit(self.background, (self.x, self.y))
         if self.show_img:
             self.ext_display.blit(self.image,(self.x,self.y))

        


class Dialogue_Window (ui.UI_Heirarchy):
    DEFAULT_PORTRAIT = 0
    DEFAULT_BG = "data/npc_profiles/backgrounds/wall.png"

    MAIN_COLOR =  pygame.Color("antiquewhite2")
    SECONDARY_COLOR = pygame.Color("bisque4")

    BODY_TXT_SIZE = ptr(16)
    BIG_TXT_SIZE = ptr(36)
    BODY_LINES = 10
    BODY_C_PER_LINE = 50
    BODY_W = 400
    BODY_H = 400
    BODY_X = 400
    BODY_Y = 0

    HEADER_X = 0
    HEADER_Y = 0
    HEADER_W = BODY_W
    HEADER_H = 40

    T_HEAD_X = 0
    T_HEAD_Y = HEADER_H
    T_HEAD_W = BODY_W
    T_HEAD_H = BODY_H - HEADER_H

    ID = 0
    BODY = 1
    NPC = 2
    HEADER = 3
    BACKGROUND = 4
    SHOW_NPC = 5
    CHOICES = 6

    def return_play (self):
        self.control.last_state()
        self.__init__(self.display, self.control)

    def __check_prereqs(self, i):
        for prereq in self.prereqs[i]:
            log.write(prereq)
        return True

    def __apply_attr(self, i):
        for attr in self.set_on_click[i]:
            #log.write(attr)
            if (attr["type"] == "sentiment"):
                self.elements[1].update_sentiment(attr["value"])

    def select(self, i):
        i += self.menu.cursor
        if (i >= len(self.lines)):
            return
        if (self.__check_prereqs(i)):
            self.__apply_attr(i)
            if self.goto[i] == -1:
                self.return_play()
            else :
                self.load(self.goto[i])

    def __init__ (self, surface, control):
        super().__init__(surface, False)
        self.body = ptr("-")
        self.cursor = ptr(0)
        self.header = ptr("-")
        self.options = []
        self.update_txt = ptr(False)
        self.update_hdr = ptr(False)
        self.elements.append(screen_writer.Text_Box(self.BODY_X,self.BODY_Y,self.BODY_W,self.BODY_H,surface,self.body,self.BODY_TXT_SIZE,self.cursor,self.BODY_C_PER_LINE,self.BODY_LINES,self.update_txt,color = self.MAIN_COLOR))
        img = Talking_Head(self.T_HEAD_X, self.T_HEAD_Y, self.T_HEAD_W, self.T_HEAD_H, surface, self.DEFAULT_PORTRAIT)
        img.update_img(self.DEFAULT_BG, False)
        self.elements.append(img)
        self.elements.append(screen_writer.Text_Box(self.HEADER_X,self.HEADER_Y,self.HEADER_W,self.HEADER_H,surface,self.header,self.BIG_TXT_SIZE,ptr(0),self.BODY_C_PER_LINE,self.BODY_LINES,self.update_hdr, color=self.SECONDARY_COLOR,writer=screen_writer.GOTHIC, y_offset=-4))
        self.control = control
        self.lines = []
        self.menu = screen_writer.Text_Menu(0,self.BODY_H,800,200,surface,self.lines, x_off= 40, y_off= 10,max_display=3)
        self.sub_composites.append(self.menu)

    def load (self, entry_point):
        self.data = db.get("*", "dialogue", ("id", entry_point))[0]
        self.body.value = self.data[self.BODY]
        self.update_txt.value = True
        self.header.value = self.data[self.HEADER]
        self.update_hdr.value = True
        self.choices = json.loads(self.data[self.CHOICES])
        self.lines = []
        self.goto = []
        self.prereqs = []
        self.set_on_click = []
        for choice in self.choices:
            self.lines.append(choice["body"])
            self.prereqs.append(choice["prereq"])
            self.goto.append(choice["goto"])
            self.set_on_click.append(choice["set"])
        if (self.data[self.NPC] != self.elements[1].id):
            self.elements[1] =  Talking_Head(self.T_HEAD_X, self.T_HEAD_Y, self.T_HEAD_W, self.T_HEAD_H, self.display, self.data[self.NPC])
        self.elements[1].update_img(self.data[self.BACKGROUND], self.data[self.SHOW_NPC] == 1)
        self.menu = screen_writer.Text_Menu(0,self.BODY_H,800,200,self.display,self.lines, x_off= 10, cap_w=100, y_off= 10,max_display=3,action=self.select)
        self.sub_composites[0] = self.menu
        log.write("Succesfully loaded dialouge " + str(entry_point))
        