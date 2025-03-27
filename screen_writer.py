import pygame, ui, utils

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
                  p_button = ui.Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1, x_offset = 0, y_offset = 0, args = None):
        super().__init__ (x, y, w, h, ext_display, action, color, border_width, 
                  p_button, draw_border , activation_key, args = args)
        self.text = text
        self.size = size
        self.writer = writer
        self.x_offset = x_offset + 2 * self.b_w 
        self.y_offset = y_offset + 2 * self.b_w 

    def render(self):
        super().render()
        self.ext_display.blit(self.writer.render(self.text.value, self.size.value),(self.x + self.x_offset,self.y + self.y_offset))

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
                    max_char_per_line, max_lines, update_text: utils.Ptr = utils.Ptr(False),
                    writer: Screen_Writer = DEFAULT_WRITER, action : callable = None,
                   color:tuple = ui.Element.DEFAULT_GREY, border_width : int = ui.Interactable_Element.DEFAULT_BORDER_W, 
                  p_button = ui.Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1, x_offset = 0, y_offset = 0, args = None):
        self.max_c_per_line = max_char_per_line
        self.max_lines = max_lines
        self.cursor = cursor
        self.refresh = update_text
        super().__init__ (x, y, w, h, ext_display, text , size, writer, action, color, border_width, 
                  p_button, draw_border, activation_key , x_offset=x_offset, y_offset=y_offset,args = args)
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
             rendered =  (self.writer.render(self.lines[line_count], self.size.value))
             delta_y = rendered.size[1]
             self.ext_display.blit(rendered,(self.x_offset + self.x, draw_y))
             draw_y += delta_y

    

    