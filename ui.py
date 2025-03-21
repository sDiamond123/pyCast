import pygame, utils

class Element():
    DEFAULT_GREY = (155,155,155)
    def __init__ (self, x, y, w, h, ext_display, color : tuple = DEFAULT_GREY):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.ext_display = ext_display
    
    def __adjust_color__ (self, delta):
        return (utils.clamp_addition(self.color[0], delta, self.COLOR_MAX, 0),
                utils.clamp_addition(self.color[1], delta, self.COLOR_MAX, 0),
                utils.clamp_addition(self.color[2], delta, self.COLOR_MAX, 0))
    
    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        pass

    def Render(self):
        pygame.draw.rect(self.ext_display, self.color, (self.x, self.y, self.w, self.h))

class Interactable_Element(Element):
    COLOR_MAX = 255
    COLOR_DELTA = 20
    DEFAULT_BORDER_W = 3
    DEFAULT_MB = 0

    def __init__ (self, x, y, w, h, ext_display: pygame.surface, color:tuple = Element.DEFAULT_GREY, border_width : int = DEFAULT_BORDER_W, 
                  p_button = DEFAULT_MB, draw_border = True, activation_key = ''):
        super().__init__(x,y,w,h, ext_display, color)
        self.b_w = border_width
        self.state = utils.Mouse_State.UNDEFINED
        self.activation_button = p_button
        self.activation_key = activation_key
        self.draw_border = draw_border

    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        super().update(m_x, m_y, mouse, keys)
        if m_x >= self.x and m_x < self.x + self.w and m_y >= self.h and m_y <= self.y + self.h:
            self.state = mouse.state[self.activation_button]
        else:
            self.state = utils.Mouse_State.UNDEFINED

    def __get_border_color(self):
        b_delta = - self.COLOR_DELTA
        if (self.state == utils.Mouse_State.NOT_PRESSED):
            b_delta = 0
        elif (self.state == utils.Mouse_State.PRESSED):
             b_delta = self.COLOR_DELTA
        return self.__adjust_color__(b_delta)
    
    def __draw_border(self):
        # draw border
        pygame.draw.rect(self.ext_display, self.__get_border_color(), (self.x, self.y, self.w, self.h))

    def render (self):
        color_adjustment = 0
        if (self.state == utils.Mouse_State.PRESSED):
            color_adjustment = - self.COLOR_DELTA
        draw_color = self.__adjust_color__(color_adjustment)
        if self.draw_border:
            self.__draw_border()
            # draw button
            pygame.draw.rect(self.ext_display, draw_color, (self.x + self.b_w, self.y + self.b_w, self.w - (2 * self.b_w), self.h - (2 * self.b_w)))
    
        else:
            # draw button
            pygame.draw.rect(self.ext_display, draw_color, (self.x, self.y, self.w, self.h))
    
class Image (Interactable_Element):
    COLOR_MAX = 255
    COLOR_DELTA = 20
    DEFAULT_MB = -1

    def __init__ (self, x, y, w, h, ext_display : pygame.surface, image,
                  p_button = DEFAULT_MB, draw_border = False, color = Element.DEFAULT_GREY, border_width = 0, activation_key = ''):
        super().__init__(x,y,w,h,ext_display, p_button=p_button, draw_border=draw_border, 
                         color=color, border_width=border_width, activation_key=activation_key)
        if isinstance(image, str):
            image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (w - 2 * self.b_w,h - 2 * self.b_w))
    
    def __get_border_color(self):
        if self.activation_button == self.DEFAULT_MB:
            return self.color
        else:
            return super().__get_border_color()

    def render (self):
         if self.draw_border:
             self.__draw_border()
         self.ext_display.blit(self.image, (self.x, self.y))


class Text_Box(Interactable_Element):
    text = ""

class Button(Interactable_Element):
     def __init__ (self, x, y, w, h, ext_display: pygame.surface, action : callable, color:tuple = Element.DEFAULT_GREY, border_width : int = Interactable_Element.DEFAULT_BORDER_W, 
                  p_button = Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = '', text = None):
         self.action = action
         super().__init__(x,y,w,h,ext_display,color,border_width,p_button,draw_border,activation_key=activation_key)

     def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        super().update(m_x, m_y, mouse, keys)
        if (self.state == utils.Mouse_State.RELEASED):
            self.action()

class UI_Composite ():
    DEFAULT_BACK = (100,100,200)

    def __init__(self, ext_disp : pygame.Surface, draw_background = True, background_color = DEFAULT_BACK):
        self.display = ext_disp
        self.elements = []
        self.has_back = draw_background
        self.back_color = background_color

    def update(self, mouse : utils.Mouse_Manager, keys):
        coor = mouse.poll_rel()
        size = self.display.size
        m_x = coor[0] * size[0]
        m_y = coor[1] * size[1]
        for element in self.elements:
            element.update(m_x, m_y, mouse, keys)

    def render(self):
        if self.has_back:
            self.display.fill(self.back_color)
        for element in self.elements:
            element.render()


class Main_Menu (UI_Composite):
    def action(self):
        self.control.game_state = self.control.GAME_STATES.FPS

    def __init__ (self, display, control):
        super().__init__(display)
        self.control = control
        self.elements.append(Interactable_Element(20,50,40,30,display))
        self.elements.append(Interactable_Element(70,50,50,40,display, border_width= 15, color= (123, 89, 20)))
        self.elements.append(Interactable_Element(70,135,100,100,display,draw_border=False, color = (255,230,15)))
        self.elements.append(Button(400,200,30,30,display,self.action))