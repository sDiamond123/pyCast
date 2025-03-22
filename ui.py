import pygame, utils, texture, math, map, player

class Element():
    DEFAULT_GREY = (155,155,155)
    def __init__ (self, x, y, w, h, ext_display : pygame.Surface, color : tuple = DEFAULT_GREY):
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

    def render(self):
        pygame.draw.rect(self.ext_display, self.color, (self.x, self.y, self.w, self.h))

class Interactable_Element(Element):
    COLOR_MAX = 255
    COLOR_DELTA = 20
    DEFAULT_BORDER_W = 3
    DEFAULT_MB = 0

    def __init__ (self, x, y, w, h, ext_display: pygame.surface, color:tuple = Element.DEFAULT_GREY, border_width : int = DEFAULT_BORDER_W, 
                  p_button = DEFAULT_MB, draw_border = True, activation_key = -1):
        super().__init__(x,y,w,h, ext_display, color)
        self.b_w = border_width
        self.state = utils.Mouse_State.UNDEFINED
        self.activation_button = p_button
        self.activation_key = activation_key
        self.draw_border = draw_border

    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        super().update(m_x, m_y, mouse, keys)
        if m_x >= self.x and m_x < self.x + self.w and m_y >= self.y and m_y < self.y + self.h:
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
    
class Still_Image (Interactable_Element):
    COLOR_MAX = 255
    COLOR_DELTA = 20
    DEFAULT_MB = -1

    def __init__ (self, x, y, w, h, ext_display : pygame.surface, image,
                  p_button = DEFAULT_MB, draw_border = False, color = Element.DEFAULT_GREY, border_width = 0, activation_key = -1):
        super().__init__(x,y,w,h,ext_display, p_button=p_button, draw_border=draw_border, 
                         color=color, border_width=border_width, activation_key=activation_key)
        if isinstance(image, str):
            image = pygame.image.load(image)
            self.image = pygame.transform.scale(image, (w - 2 * self.b_w,h - 2 * self.b_w))
        else:
            self.image = image
    
    def __get_border_color(self):
        if self.activation_button == self.DEFAULT_MB:
            return self.color
        else:
            return super().__get_border_color()

    def render (self):
         if self.draw_border:
             pygame.draw.rect(self.ext_display, self.__get_border_color(), (self.x, self.y, self.w, self.h))
         self.ext_display.blit(self.image, (self.x, self.y))

class Rolling_Image (Still_Image):
    DEFAULT_PHASE = 0
    DEFAULT_FOV = math.pi
    def __init__ (self, x, y, w, h, ext_display : pygame.surface, image,phase_ptr:utils.Ptr,
                  p_button = Still_Image.DEFAULT_MB, draw_border = False, color = Element.DEFAULT_GREY, border_width = 0, activation_key = -1, phase = DEFAULT_PHASE, fov = DEFAULT_FOV):
        if isinstance(image, str):
            image = texture.RollingTexture(image, phase, fov, w - 2 * border_width, h - 2 * border_width)
        super().__init__(x,y,w,h,ext_display, image, p_button=p_button, draw_border=draw_border, 
                         color=color, border_width=border_width, activation_key=activation_key)
        self.phase_ptr = phase_ptr

    def render (self):
        if self.draw_border:
            pygame.draw.rect(self.ext_display, self.color, (self.x, self.y, self.w, self.h))
        self.image.render(self.phase_ptr.value)
        self.ext_display.blit(self.image.external_screen, (self.x + self.b_w,self.y + self.b_w))


class Map_Display(Element):

    def __init__ (self, x, y, ext_display : pygame.Surface, map:map.Map, player:player.Player, cell_w = 20, cell_h = 20, trav_w = 4, trav_h = 3, cool_down = 100):
        super().__init__(x,y,0,0,ext_display)
        self.map = map
        self.player = player
        self.map_w = cell_w
        self.map_h = cell_h
        self.map_trav_w = trav_w
        self.map_trav_h = trav_h
        self.map_cool_down = cool_down
        self.map_t = utils.Timed_Toggle(self.map_cool_down)
        self.x_off = 0
        self.y_off = 0

    def __perform_z_in__ (self):
        old_w = self.map_trav_w
        old_h = self.map_trav_h
        if (old_w > 0):
            self.map_trav_w -= 1
            self.map_w = self.map_w * (old_w * 2 + 1)/(self.map_trav_w * 2 + 1)
        if (old_h > 0):
            self.map_trav_h -= 1
            self.map_h = self.map_h * (old_h * 2 + 1)/(self.map_trav_h * 2 + 1)      

    def __perform_z_out__ (self):
         old_w = self.map_trav_w
         old_h = self.map_trav_h
         self.map_trav_w += 1
         self.map_trav_h += 1
         self.map_w = self.map_w * (old_w * 2 + 1)/(self.map_trav_w * 2 + 1)
         self.map_h = self.map_h * (old_h * 2 + 1)/(self.map_trav_h * 2 + 1)

    def map_zoom_in(self):
        if (self.map_t.clock):
            self.__perform_z_in__()    

    def map_zoom_out(self):
        if (self.map_t.clock):
            self.__perform_z_out__()   


    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        self.map_t.update()

    def render (self):
         # render minimap
        self.map.rendermap (self.ext_display, self.player, self.map_trav_w, self.map_trav_h, self.x, self.y, self.map_w, self.map_h, self.x_off, self.y_off)

class Button(Interactable_Element):
     def __init__ (self, x, y, w, h, ext_display: pygame.surface, action : callable, color:tuple = Element.DEFAULT_GREY, border_width : int = Interactable_Element.DEFAULT_BORDER_W, 
                  p_button = Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1):
         self.action = action
         super().__init__(x,y,w,h,ext_display,color,border_width,p_button,draw_border,activation_key=activation_key)

     def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        super().update(m_x, m_y, mouse, keys)
        if (self.state == utils.Mouse_State.RELEASED or (self.activation_key != -1 and keys[self.activation_key])) and self.action != None:
            self.action()

class Mouse_Cursor(Interactable_Element):
    def __init__ (self, x, y, w, h, ext_display: pygame.surface, color:tuple = Element.DEFAULT_GREY, border_width : int = Interactable_Element.DEFAULT_BORDER_W, 
                    p_button = Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1):
            self.alive = False
            super().__init__(x,y,w,h,ext_display,color,border_width,p_button,draw_border,activation_key=activation_key)

    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        self.x = m_x
        self.y = m_y
        self.alive = mouse.alive

    def render(self):
         if self.alive:
            # uses self.w as sidelength, self.h as a spacer
            three_halves = 3/2 * self.w
            one_half = self.w/2
            # draw bottom
            pygame.draw.rect(self.ext_display, self.color, (self.x + three_halves + self.h, self.y - one_half, self.w, self.w))
            # draw top
            pygame.draw.rect(self.ext_display, self.color, (self.x - three_halves + self.h, self.y - one_half, self.w, self.w))
            # draw middle
            pygame.draw.rect(self.ext_display, self.color, (self.x, self.y + three_halves + self.h, self.w, self.w))


class Bar(Element):
    DEFAULT_FILLED = (155, 10, 10)
    DEFAULT_EMPTY = (120, 120, 120)
    DEFAULT_DEAD = (0,0,0)

    def __init__ (self, x, y, w, h, ext_display : pygame.Surface, data : utils.Partial, filled_color : tuple = DEFAULT_FILLED, empty_color : tuple = DEFAULT_EMPTY, dead_color : tuple = DEFAULT_DEAD):
        super().__init__(x,y,w,h,ext_display)
        self.filled = filled_color
        self.empty = empty_color
        self.dead = dead_color
        self.data = data
        

    def render (self):
          # render health
        if self.data.current >= 0:
            fill_ratio = self.w * self.data.ratio
            pygame.draw.rect(self.ext_display, self.filled, (self.x, self.y, fill_ratio, self.h))
            pygame.draw.rect(self.ext_display, self.empty, (self.x + fill_ratio, self.y, self.w  - fill_ratio, self.h))
        else:
            pygame.draw.rect(self.ext_display, self.dead, (self.x,self.y,self.w,self.h))




class UI_Composite ():
    DEFAULT_BACK = (100,100,200)

    def __init__(self, ext_disp : pygame.Surface, draw_background = True, background_color = DEFAULT_BACK):
        self.display = ext_disp
        self.elements = []
        self.has_back = draw_background
        self.back_color = background_color
        self.exit = False
        self.want_mouse = True

    def update(self, mouse : utils.Mouse_Manager, keys):
        coor = mouse.poll_rel()
        size = self.display.size
        m_x = coor[0] * size[0]
        m_y = coor[1] * size[1]
        for element in self.elements:
            element.update(m_x, m_y, mouse, keys)
        return False

    def render(self):
        if self.has_back:
            self.display.fill(self.back_color)
        for element in self.elements:
            element.render()


