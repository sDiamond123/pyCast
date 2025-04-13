import pygame, ui, utils, clock, normalize
from log import LOG as log
from options import TERM as key_in

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
        log.write("Succesfully loaded font: " + font)

    def render (self, text : str, size : int = default_size, color = "black", antialias = True):
        font = self.fonts[size]
        return font.render(text, antialias = antialias, color = color)
    
DEFAULT_WRITER = Screen_Writer()
GOTHIC = Screen_Writer(FONT_PATH + "/Jacquard_12/Jacquard12-Regular.ttf")
CURSIVE = Screen_Writer(FONT_PATH + "/Playwrite_MX_Guides/PlaywriteMXGuides-Regular.ttf")

class Text_Button (ui.Button):
    def __init__ (self, x, y, w, h, ext_display: pygame.surface,
                   text : utils.Ptr, size: utils.Ptr, writer: Screen_Writer = DEFAULT_WRITER, action : callable = None,
                   color:tuple = ui.Element.DEFAULT_GREY, border_width : int = ui.Interactable_Element.DEFAULT_BORDER_W, 
                  p_button = ui.Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1, x_offset = 0, y_offset = 0,
                    args = None, text_color = pygame.Color("black"), scale = True):
        super().__init__ (x, y, w, h, ext_display, action, color, border_width, 
                  p_button, draw_border , activation_key, args = args, scale=scale)
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
                  p_button = ui.Interactable_Element.DEFAULT_MB, draw_border = True, x_offset = 0, y_offset = 0, text_color = pygame.Color("hotpink"), scale = True):
        super().__init__ (x, y, w, h, ext_display, None, color, border_width, 
                  p_button, draw_border,scale = scale)
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

        if self.has_slider and len(self.lines) != self.old_len:
            if len(self.lines) > self.max_lines:
                 if self.slider != None:
                    self.slider.max = len(self.lines)
                    self.slider.refresh.value = True
                 else:
                    self.slider = ui.Slider((self.x + self.w)/normalize.SCALE_FACTOR_X - self.b_w - 16, self.y/normalize.SCALE_FACTOR_Y + self.b_w, 16,self.h/normalize.SCALE_FACTOR_Y - 2 * self.b_w,self.ext_display,color = self.text_color,current=self.cursor, phantom_dist= 64, max=len(self.lines))
            else:
                self.slider = None
        self.old_len = len(self.lines)

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
                    args = None, text_color = pygame.Color("black"), scale = True, has_slider = True):
        self.max_c_per_line = max_char_per_line
        self.max_lines = max_lines
        self.cursor = cursor
        self.refresh = update_text
        self.true_button = p_button
        self.slider = None
        self.old_len = 0
        super().__init__ (x, y, w, h, ext_display, text , size, writer, action, color, border_width, 
                  p_button, draw_border, activation_key , x_offset=x_offset, y_offset=y_offset,args = args, text_color=text_color, scale = scale)
        self.has_slider = has_slider
        self.__parse_text__()
        
        #if has_slider and len(self.lines) > max_lines:
        #    self.slider = ui.Slider(x + w + border_width, y + border_width, 16,h - 2 * border_width,ext_display,color = text_color,current=self.cursor, phantom_dist= 64, max=len(self.lines))
            
    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        if self.slider!=None:
            self.slider.update(m_x, m_y, mouse, keys)
            if self.slider.state != utils.Mouse_State.UNDEFINED:
                self.activation_button = -1
            else:
                self.activation_button = self.true_button
        super(Text_Button, self).update(m_x, m_y, mouse, keys)
        if self.state == utils.Mouse_State.NOT_PRESSED:
            if mouse.mw != 0:
                self.cursor.value = utils.clamp_addition(self.cursor.value, -mouse.mw, len(self.lines) - 1, 0)
                if self.slider != None:
                    self.slider.refresh.value = True
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
             if self.slider != None:
                 self.slider.render()

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
            if i + self.cursor.value < len(self.lines) and self.cursor.value >= 0:
                  text += str(self.lines[i + self.cursor.value ])
            else:
                text = self.DEFAULT_TEXT.value
            self.text[i].value = text

    def down(self):
        self.cursor.value = utils.clamp_addition(self.cursor.value, 1, len(self.lines) - 1,0)
        self.update_text()
        if self.has_slider:
            self.elements[self.max].refresh.value = True

    def up(self):
        self.cursor.value = utils.clamp_addition(self.cursor.value, -1, len(self.lines) - 1,0)
        self.update_text()
        if self.has_slider:
            self.elements[self.max].refresh.value = True

    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        super().update(m_x, m_y, mouse, keys)
        for element in self.elements:
            if element.state != utils.Mouse_State.UNDEFINED:
                return False
        if (mouse.mw < 0):
            self.down()
        elif (mouse.mw > 0):
            self.up()
        if self.has_slider and self.elements[self.max].moved:
            self.update_text()
        return False
        

    def __init__ (self,x, y, w, h, ext_display: pygame.surface, lines, action:callable = None, max_display = MAX, 
                  color:tuple=(59,54,48), render = True, draw_background = True, x_off = 0, y_off = 0, size = DESC_SIZE, 
                  box_w = -1, box_spacing = 10, box_h = -1, cap_w = 10, draw_cur = True, char_per_line = 100, lines_per_box = 2, scale = True, has_slider = True):
        self.cursor = utils.Ptr(0)
        
        super().__init__(x,y,w,h,ext_display, color,render,draw_background, scale = scale)
        self.lines = lines
        self.text = []
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
            if i + self.cursor.value < len(self.lines) and self.cursor.value >= 0:
                  self.text.append(utils.Ptr(header + str(self.lines[i + self.cursor.value])))
            else:
                self.text.append(self.DEFAULT_TEXT)
            self.elements.append(Text_Box(x + x_off, y+y_off + box_delta * i,box_w, box_h, ext_display,self.text[i],
                                          utils.Ptr(size),utils.Ptr(0),char_per_line,lines_per_box, color=self.DESC_COLOR, 
                                          update_text=self.update_txt[i], action=action, activation_key= 49 + i, args = i))

        if has_slider and len(self.lines) >= self.max:
             self.elements.append(ui.Slider(x + w - 32, y + 16, 16, h-32,ext_display,current = self.cursor, max=len(self.lines)))
             self.has_slider = True
        else:
            self.has_slider = False

class Log(Text_Box):
    def __init__(self, x, y, w, h, ext_display, size, cursor, max_char_per_line, max_lines, update_text = utils.FALSE_PTR, writer = DEFAULT_WRITER, action = None, color = ui.Element.DEFAULT_GREY, border_width = ui.Interactable_Element.DEFAULT_BORDER_W, p_button=ui.Interactable_Element.DEFAULT_MB, draw_border=True, activation_key=-1, x_offset=0, y_offset=0, args=None, text_color=pygame.Color("black"), scale=True):
        super().__init__(x, y, w, h, ext_display, log.log, size, cursor, max_char_per_line, max_lines, update_text, writer, action, color, border_width, p_button, draw_border, activation_key, x_offset, y_offset, args, text_color, scale)

class Typewriter(Text_Box):
    TIME = 30
    MAX_LEN = 256

    def __init__(self, x, y, w, h, ext_display, prompt, size, cursor, max_char_per_line, max_lines, update_text = utils.FALSE_PTR, writer = DEFAULT_WRITER, action = None, color = ui.Element.DEFAULT_GREY, border_width = ui.Interactable_Element.DEFAULT_BORDER_W, draw_border=True, x_offset=0, y_offset=0, text_color=pygame.Color("black"), scale=True, max_len = MAX_LEN, verbose = False):
        self.out = utils.Ptr("")
        super().__init__(x, y, w, h, ext_display, prompt, size, cursor, max_char_per_line, max_lines, update_text, writer, action, color, border_width, -1, draw_border, -1 , x_offset, y_offset, self.out, text_color, scale)
        self.old_keys = [False * 256]
        self.prompt = prompt.value
        self.is_lower = True
        self.body = ""
        self.flash = False
        self.flip = self.TIME
        self.slice = 0
        self.max = max_len
        self.verbose = verbose

    def update(self, m_x, m_y, mouse, keys):
        self.flip -= 1
        if self.flip < 0:
            self.flash = not self.flash
            self.flip = self.TIME
        k_pressed = key_in.poll_keys(keys,self.verbose)
        checkEnd = False
        if k_pressed[key_in.POLL_KP]:
            arrow = k_pressed[key_in.POLL_ARROWS]
            if arrow != key_in.P_NONE:
                    if arrow == key_in.P_UP:
                        self.cursor.value = utils.clamp_addition(self.cursor.value,-1,len(self.lines)-1, 0)
                    elif arrow == key_in.P_DOWN:
                        self.cursor.value = utils.clamp_addition(self.cursor.value,1,len(self.lines)-1, 0)
                    elif arrow == key_in.P_LEFT:
                        self.slice = utils.clamp_addition(self.slice,-1, len(self.body), 0)
                    elif arrow == key_in.P_RIGHT:
                        self.slice = utils.clamp_addition(self.slice, 1, len(self.body), 0)
            self.flash = True 
            self.flip = self.TIME
            if k_pressed[key_in.POLL_ENT] and self.action != None:
                self.action(self.body)
                self.body = ""
                self.slice = 0
                self.cursor.value = 0
            elif k_pressed[key_in.POLL_DEL] and len(self.body) > 0:
                self.body= self.body[:self.slice - 1] + self.body[self.slice:]
                self.slice-=1
            elif len(k_pressed[key_in.POLL_TXT]) + len(self.body) < self.MAX_LEN:
                self.body = self.body[:self.slice] +  k_pressed[key_in.POLL_TXT] + self.body[self.slice:]
                self.slice += len(k_pressed[key_in.POLL_TXT])
                if "\n" in k_pressed[key_in.POLL_TXT]:
                    checkEnd = True
        char = "."
        if self.flash:
            char =  "_"
        self.text.value = self.prompt + self.body[:self.slice] + char + self.body[self.slice:]
        self.refresh.value = True
        super().update(m_x, m_y, mouse, keys)
        if checkEnd:
            self.cursor.value = len(self.lines) - 2