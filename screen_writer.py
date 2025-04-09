import pygame, ui, utils, clock, math

FONT_PATH = "data/fonts"
DEFAULT_FONT = "/Open_Sans/static/OpenSans-Regular.ttf"
DEFAULT_SIZES = [6,8,16,12,20,24,36,50]

if not pygame.font.get_init():
    pygame.font.init()

class Screen_Writer:
    default_size = 12

    def __init__ (self, font:str = FONT_PATH + DEFAULT_FONT, sizes : list[int] = DEFAULT_SIZES):
        self.fonts = {} 
        self.default_size = sizes[0]
        for size in sizes:
            self.fonts[size] = pygame.font.Font(font, size)
        print("Succesfully loaded font: " + font)

    def render (self, text : str, size : int = default_size, color = "black", antialias = True):
        font = self.fonts[size]
        return font.render(text, antialias = antialias, color = color)
    
DEFAULT_WRITER = Screen_Writer()

class Text_Button (ui.Button):
    def __init__ (self, x, y, w, h, ext_display: pygame.surface,
                   text : utils.Ptr, size: utils.Ptr, writer: Screen_Writer = DEFAULT_WRITER, action : callable = None,
                   color:tuple = ui.Element.DEFAULT_GREY, border_width : int = ui.Interactable_Element.DEFAULT_BORDER_W, 
                  p_button = ui.Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1, x_offset = 0, y_offset = 0, args = None, text_color = pygame.Color("black")):
        super().__init__ (x, y, w, h, ext_display, action, color, border_width, 
                  p_button, draw_border , activation_key, args = args)
        self.text = text
        self.size = size
        self.text_color = text_color
        self.writer = writer
        self.x_offset = x_offset + 2 * self.b_w 
        self.y_offset = y_offset + 2 * self.b_w 

    def render(self):
        super().render()
        self.ext_display.blit(self.writer.render(str(self.text.value), self.size.value, color=self.text_color),(self.x + self.x_offset,self.y + self.y_offset))

class FPS_UI (ui.Button):
    FPS_LEN = 4

    def __init__ (self, x, y, w, h, ext_display: pygame.surface, size: utils.Ptr, writer: Screen_Writer = DEFAULT_WRITER,
                   color:tuple = ui.Element.DEFAULT_GREY, border_width : int = ui.Interactable_Element.DEFAULT_BORDER_W, 
                  p_button = ui.Interactable_Element.DEFAULT_MB, draw_border = True, x_offset = 0, y_offset = 0, text_color = pygame.Color("hotpink")):
        super().__init__ (x, y, w, h, ext_display, None, color, border_width, 
                  p_button, draw_border)
        self.size = size
        self.writer = writer
        self.x_offset = x_offset + 2 * self.b_w 
        self.y_offset = y_offset + 2 * self.b_w 
        self.text_color = text_color
    def render(self):
        self.ext_display.blit(self.writer.render(str(clock.CLOCK.get_fps())[:self.FPS_LEN], self.size.value,color =self.text_color),(self.x + self.x_offset,self.y + self.y_offset))

class Text_Box (Text_Button):
    ABS_BREAK_CHARS = ["\r\n", "\n", "\r"]

    def __parse_text__ (self):
        self.lines = []
        line = utils.Ptr("")
        length = utils.Ptr(0)
        if isinstance(self.text.value, str):
            self.__parse_line__(self.text.value, line, length)
        elif isinstance(self.text.value, list):
            for row in self.text.value:
                self.__parse_line__(row, line, length)

    def __end_on_word__ (self, word, line: utils.Ptr, length:utils.Ptr):
        if len(word) < self.max_c_per_line:
            if length.value > 0:
                '''if length.value + len(word) < self.max_c_per_line:
                        line.value += " " + word
                        self.lines.append(line.value)
                        line.value = 0
                        length.value = 0
                        return'''
                self.lines.append(line.value)
        else:
            if length.value > 0:
                self.lines.append(line.value)
            while (len(word) > self.max_c_per_line):
                
                self.lines.append(word[:self.max_c_per_line - 1] + "-")
                word = word[self.max_c_per_line - 1:]
        line.value = word
        length.value = len(word)


    def __parse_line__ (self, value, line: utils.Ptr, length:utils.Ptr):
        split = value.split(" ")
        for word in split:
            if len(word) == 0:
                continue
            skip = False
            for char in self.ABS_BREAK_CHARS:
                if char in word:
                    for words in word.split(char):
                        if len(words) <= 0:
                            if len (line.value) != 0:
                                self.lines.append(line.value)
                                line.value = ""
                                length.value = 0
                            continue
                        self.__end_on_word__(words, line, length)
                        self.lines.append(line.value)
                        line.value = ""
                        length.value = 0
                    skip = True
            if not skip:
                if len(word) + length.value < self.max_c_per_line:
                    line.value += " " + word
                    length.value += len(word) + 1
                else:
                    self.__end_on_word__(word,line,length)
        if length.value != 0:
            self.lines.append(line.value)

    def __init__ (self, x, y, w, h, ext_display: pygame.surface,
                   text : utils.Ptr, size: utils.Ptr, cursor: utils.Ptr,
                    max_char_per_line, max_lines, update_text: utils.Ptr = utils.FALSE_PTR,
                    writer: Screen_Writer = DEFAULT_WRITER, action : callable = None,
                   color:tuple = ui.Element.DEFAULT_GREY, border_width : int = ui.Interactable_Element.DEFAULT_BORDER_W, 
                  p_button = ui.Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1, x_offset = 0, y_offset = 0,
                    args = None, text_color = pygame.Color("black")):
        self.max_c_per_line = max_char_per_line
        self.max_lines = max_lines
        self.cursor = cursor
        self.refresh = update_text
        super().__init__ (x, y, w, h, ext_display, text , size, writer, action, color, border_width, 
                  p_button, draw_border, activation_key , x_offset=x_offset, y_offset=y_offset,args = args, text_color=text_color)
        self.__parse_text__()
    
    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        super(Text_Button, self).update(m_x, m_y, mouse, keys)
        if self.state == utils.Mouse_State.NOT_PRESSED:
            if mouse.mw != 0:
                self.cursor.value = utils.clamp_addition(self.cursor.value, -mouse.mw, len(self.lines) - 1, 0)
        if self.refresh.value:
            self.refresh.value = False
            self.__parse_text__()
        


    def render (self):
         # call button's render
         super(Text_Button, self).render()
         draw_y = self.y + self.y_offset
         for line in range(self.max_lines):
             line_count = line + self.cursor.value
             if line_count < 0:
                 continue
             if line_count >= len(self.lines):
                 break
             rendered =  (self.writer.render(self.lines[line_count], self.size.value,self.text_color))
             delta_y = rendered.size[1]
             self.ext_display.blit(rendered,(self.x_offset + self.x, draw_y))
             draw_y += delta_y

class Text_Menu (ui.UI_Sub_Screen):

    DESC_SIZE = 16
    DEFAULT_TEXT = utils.Ptr("---")
    DESC_COLOR = pygame.Color("bisque3")
    MAX = 3

    def update_text(self):
        for i in range (self.max):
            self.update_txt[i].value = True
            text = ""
            if self.draw_numbers:
                text = str(i) + " . "
            if i + self.cursor < len(self.lines) and self.cursor >= 0:
                  text += str(self.lines[i + self.cursor ])
            else:
                text = self.DEFAULT_TEXT.value
            self.text[i].value = text

    def down(self):
        self.cursor = utils.clamp_addition(self.cursor, 1, len(self.lines) - 1,0)
        self.update_text()

    def up(self):
        self.cursor = utils.clamp_addition(self.cursor, -1, len(self.lines) - 1,0)
        self.update_text()

    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        super().update(m_x, m_y, mouse, keys)
        for element in self.elements:
            if element.state != utils.Mouse_State.UNDEFINED:
                return False
        if (mouse.mw < 0):
            self.down()
        elif (mouse.mw > 0):
            self.up()
        return False
        

    def __init__ (self,x, y, w, h, ext_display: pygame.surface, lines, action:callable = None, max_display = MAX, 
                  color:tuple=(59,54,48), render = True, draw_background = True, x_off = 0, y_off = 0, size = DESC_SIZE, 
                  box_w = -1, box_spacing = 10, box_h = -1, cap_w = 10, draw_cur = True, char_per_line = 100, lines_per_box = 2):
        super().__init__(x,y,w,h,ext_display, color,render,draw_background)
        self.lines = lines
        self.text = []
        self.cursor = 0
        self.max = max_display
        self.update_txt = []
        self.draw_numbers = draw_cur
        if box_w == -1:
            box_w = w - x_off- cap_w
        if box_h == -1:
            box_h = (h-y_off)/max_display - box_spacing
        box_delta = box_h + box_spacing
        for i in range(self.max):
            self.update_txt.append(utils.Ptr(False))
            header = str(i) + " . "
            if (not draw_cur):
                header = ""
            if i + self.cursor < len(self.lines) and self.cursor >= 0:
                  self.text.append(utils.Ptr(header + str(self.lines[i + self.cursor])))
            else:
                self.text.append(self.DEFAULT_TEXT)
            self.elements.append(Text_Box(x + x_off, y+y_off + box_delta * i,box_w, box_h, ext_display,self.text[i],
                                          utils.Ptr(size),utils.Ptr(0),char_per_line,lines_per_box, color=self.DESC_COLOR, 
                                          update_text=self.update_txt[i], action=action, activation_key= 49 + i, args = i))

class Keyboard(ui.Button):
    BUTTONS_PER_ROW = 10
    KEY_SIZE = utils.Ptr(20)
    BUTTON_SPACING = 3
    SPECIAL_CHARS = [("SPACE", ord(' ')),(".", ord('.')), (",", ord(',')), ("ENT", ord('\r'))]

    def keypressed (self, key):
        if key == ord('\r'):
            self.nc_text += " "
            self.cursor.value += 1
        self.nc_text += chr(key)
        self.has_text.value = True
        self.c_text.value = self.nc_text

    def __init__(self, x, y, w, h, ext_display, size, writer = DEFAULT_WRITER, color = ui.Element.DEFAULT_GREY, border_width = ui.Interactable_Element.DEFAULT_BORDER_W, p_button=ui.Interactable_Element.DEFAULT_MB, draw_border=True, x_offset=0, y_offset=0, args=None, text_color=pygame.Color("black"), back_color = pygame.Color("bisque2")):
        self.keyboard = []
        self.keys = []
        self.w = w
        self.h = h
        j = 0
        k = 0
        self.nc_text = ""
        self.c_text = utils.Ptr("")
        self.has_text = utils.Ptr(False)
        self.cursor = utils.Ptr(0)
        button_size = math.floor(self.w/(self.BUTTONS_PER_ROW + 1)) - self.BUTTON_SPACING
        for i in range (256):
            self.keys.append([utils.Ptr(chr(i)), False])
        for i in range (ord("a"), ord("z") + 1):
            self.keyboard.append(Text_Button(x + j * button_size + j * self.BUTTON_SPACING , y + k * button_size + k * self.BUTTON_SPACING, button_size, button_size,ext_display,self.keys[i][0],size,writer,self.keypressed,color,border_width,p_button,draw_border,i,x_offset,y_offset,i,text_color))
            j += 1
            if j > self.BUTTONS_PER_ROW:
                j = 0
                k+=1
        for sc in self.SPECIAL_CHARS:
            self.keys[sc[1]][0] = utils.Ptr(sc[0])
            self.keyboard.append(Text_Button(x + j * button_size + j * self.BUTTON_SPACING , y + k * button_size + k * self.BUTTON_SPACING, button_size, button_size,ext_display,self.keys[sc[1]][0],size,writer,self.keypressed,color,border_width,p_button,draw_border,sc[1],x_offset,y_offset,sc[1],text_color))
            j += 1
            if j > self.BUTTONS_PER_ROW:
                j = 0
                k+=1
        super().__init__(x,y,w,h,ext_display,None,back_color,border_width,p_button=1)
        

    def update(self, m_x, m_y, mouse, keys):
        super().update(m_x,m_y, mouse, keys)
        self.has_text.value = False
        for key in self.keyboard:
            key.update(m_x,m_y,mouse,keys)
            if keys[key.activation_key]:
                if not key.key_lock:
                    key.key_lock = True
            else:
                if key.key_lock:
                    key.key_lock = False
           

    def render(self):
        super().render()
        for key in self.keyboard:
            key.render()