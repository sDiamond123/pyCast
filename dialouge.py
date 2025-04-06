import ui, screen_writer, json, pygame
from utils import Ptr as ptr
from database import DB as db

class Talking_Head(ui.Still_Image):
    DEFAULT_IMG = "data/npc_profiles/empty/empty.png"
    ID = 0
    NAME = 1
    IMG = 2
    SENTIMENT = 3
    CUR_E_P = 4
    E_P_LIST = 5
    ATTB = 6
    TEXTS = 7
    
    def __init__ (self, x, y, w, h, ext_display : pygame.surface, id,
                  p_button = ui.Still_Image.DEFAULT_MB, draw_border = False, color = ui.Element.DEFAULT_GREY, 
                  border_width = 0, activation_key = -1):
        self.data = db.get("*", "npc", ("id", id))

        print(self.data)


class Dialouge_Window (ui.UI_Heirarchy):
    DEFAULT_IMG = "data/npc_profiles/empty/empty.png"

    BODY_TXT_SIZE = ptr(16)
    BODY_LINES = 10
    BODY_C_PER_LINE = 55
    BODY_W = 400
    BODY_H = 400
    BODY_X = 400
    BODY_Y = 0

    T_HEAD_X = 0
    T_HEAD_Y = 0
    T_HEAD_W = BODY_W
    T_HEAD_H = BODY_H

    ID = 0
    BODY = 1
    NPC = 2
    HEADER = 3
    CHOICES = 4

    def __init__ (self, surface):
        super().__init__(surface, False)
        self.body = ptr("-")
        self.cursor = ptr(0)
        self.update_txt = ptr(False)
        self.elements.append(screen_writer.Text_Box(self.BODY_X,self.BODY_Y,self.BODY_W,self.BODY_H,surface,self.body,self.BODY_TXT_SIZE,self.cursor,self.BODY_C_PER_LINE,self.BODY_LINES,self.update_txt))
        self.img = ui.Still_Image(self.T_HEAD_X,self.T_HEAD_Y,self.T_HEAD_W,self.T_HEAD_H,surface,self.DEFAULT_IMG)
        self.elements.append(self.img)

    def load (self, entry_point):
        self.data = db.get("*", "dialouge", ("id", entry_point))[0]
        print(self.data)
        self.body.value = self.data[self.BODY]
        self.update_txt.value = True
        self.th = Talking_Head(0,0,0,0,None,self.data[self.NPC])
        