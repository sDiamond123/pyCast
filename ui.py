import pygame, utils, texture, math, map, player, math, normalize

class Element():
    DEFAULT_GREY = (155,155,155)
    def __init__ (self, x, y, w, h, ext_display : pygame.Surface, color : tuple = DEFAULT_GREY, scale = True):
        self.y = y
        self.w = w
        self.h = h
        self.x = x
        self.w *= normalize.SCALE_FACTOR_X
        self.h *= normalize.SCALE_FACTOR_Y
        if scale:
            self.y *= normalize.SCALE_FACTOR_Y
            
            self.x *= normalize.SCALE_FACTOR_X
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
                  p_button = DEFAULT_MB, draw_border = True, activation_key = -1, scale = True):
        super().__init__(x,y,w,h, ext_display, color, scale)
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
        pygame.draw.rect(self.ext_display, self.__get_border_color(), (self.x, self.y, self.w, self.b_w))
        pygame.draw.rect(self.ext_display, self.__get_border_color(), (self.x, self.y + self.b_w, self.b_w, self.h - 2 * self.b_w))
        pygame.draw.rect(self.ext_display, self.__get_border_color(), (self.x + self.w - self.b_w , self.y + self.b_w, self.b_w, self.h - 2 * self.b_w))
        pygame.draw.rect(self.ext_display, self.__get_border_color(), (self.x, self.y + self.h - self.b_w , self.w, self.b_w))

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
                  p_button = DEFAULT_MB, draw_border = False, color = Element.DEFAULT_GREY, border_width = 0, activation_key = -1, scale = True):
        super().__init__(x,y,w,h,ext_display, p_button=p_button, draw_border=draw_border, 
                         color=color, border_width=border_width, activation_key=activation_key, scale = scale)
        if isinstance(image, str):
            image = pygame.image.load(image)
            self.image = pygame.transform.scale(image, (self.w - 2 * self.b_w,self.h - 2 * self.b_w))
        else:
            self.image = image
    
    def load(self, new_img):
        self.image = pygame.image.load(new_img)

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
                  p_button = Still_Image.DEFAULT_MB, draw_border = False, color = Element.DEFAULT_GREY, border_width = 0, 
                  activation_key = -1, phase = DEFAULT_PHASE, fov = DEFAULT_FOV, scale = True):
        if isinstance(image, str):
            image = texture.RollingTexture(image, phase, fov, (w - 2 * border_width) * normalize.SCALE_FACTOR_X, (h - 2 * border_width)*normalize.SCALE_FACTOR_Y)
        super().__init__(x,y,w,h,ext_display, image, p_button=p_button, draw_border=draw_border, 
                         color=color, border_width=border_width, activation_key=activation_key, scale = scale)
        self.phase_ptr = phase_ptr

    def render (self):
        if self.draw_border:
            pygame.draw.rect(self.ext_display, self.color, (self.x, self.y, self.w, self.h))
        self.image.render(self.phase_ptr.value)
        self.ext_display.blit(self.image.external_screen, (self.x + self.b_w,self.y + self.b_w))


class Map_Display(Element):

    def __init__ (self, x, y, ext_display : pygame.Surface, map:map.Map, player:player.Player, cell_w = 20, cell_h = 20, trav_w = 4, trav_h = 3, 
                  cool_down = 100, scale = True):
        super().__init__(x,y,0,0,ext_display, scale)
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
        if scale:
            self.map_w *= normalize.SCALE_FACTOR_X
            self.map_h *= normalize.SCALE_FACTOR_Y

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
     def __init__ (self, x, y, w, h, ext_display: pygame.surface, action : callable = None, color:tuple = Element.DEFAULT_GREY, border_width : int = Interactable_Element.DEFAULT_BORDER_W, 
                  p_button = Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1, args = None, scale = True):
         self.action = action
         self.args = args
         self.key_lock = False
         super().__init__(x,y,w,h,ext_display,color,border_width,p_button,draw_border,activation_key=activation_key, scale = scale)

     def activate (self):
         if self.action != None:
            if self.args == None:
                    self.action()
            else:
                self.action(self.args)

     def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        super().update(m_x, m_y, mouse, keys)
        if (self.state == utils.Mouse_State.RELEASED or (self.activation_key != -1 and keys[self.activation_key] and not self.key_lock)):
            self.activate()

class Sticky(Button):
     def __init__ (self, x, y, w, h, ext_display: pygame.surface, action : callable = None, color:tuple = Element.DEFAULT_GREY, border_width : int = Interactable_Element.DEFAULT_BORDER_W, 
                  p_button = Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1, args = None, lock_x = False, lock_y = False, lock_all = False, phantom_dist = 0, scale = True):
            super().__init__(x,y,w,h,ext_display,action,color,border_width,p_button,draw_border,activation_key,args, scale = scale)
            self.lock_x = lock_x
            self.lock_y = lock_y
            self.lock_all = lock_all
            self.moved = False
            self.phantom_dist = phantom_dist
            self.m_x_delta = self.w/2
            self.m_y_delta = self.h/2
            self.hold_lock = True

     def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
         prev_state = self.state
         super().update(m_x, m_y, mouse, keys)
         if (mouse.alive):
            return
         self.moved = False
         if (self.state == utils.Mouse_State.FIRST_PRESSED):
             self.m_x_delta = self.x - m_x
             self.m_y_delta = self.y - m_y
             self.hold_lock = False
         elif (self.state == utils.Mouse_State.UNDEFINED and self.state != prev_state):
             if prev_state == utils.Mouse_State.PRESSED and (self.phantom_dist != 0  and math.dist((m_x, m_y), (self.x - self.w/2, self.y - self.h/2)) < self.phantom_dist):
                    self.state = utils.Mouse_State.PRESSED
         if self.state == utils.Mouse_State.RELEASED:
                  self.hold_lock = True
         if (self.state == utils.Mouse_State.PRESSED and not self.lock_all and not self.hold_lock):
             if not self.lock_x:
                 self.x = m_x  + self.m_x_delta
                 self.moved = True
             if not self.lock_y:
                 self.y = m_y + self.m_y_delta
                 self.moved = True

class Swtich(Button):
    DEFAULT_ON = (10,120,10)
    DEFAULT_OFF = (120,10,10)
    toggle = False
    def __init__ (self, x, y, w, h, ext_display: pygame.surface, action : callable = None, color_off:tuple = DEFAULT_OFF, color_on:tuple = DEFAULT_ON, border_width : int = Interactable_Element.DEFAULT_BORDER_W, 
                  p_button = Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1, args = None, start_state = False, scale = True):
            color = color_off
            if (start_state):
                color = color_on
            self.color_on = color_on
            self.color_off = color_off
            super().__init__(x,y,w,h,ext_display,action,color,border_width,p_button,draw_border,activation_key,args, scale = scale)
            self.toggle = start_state

    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        super().update(m_x,m_y,mouse,keys)
        if (self.state == utils.Mouse_State.RELEASED):
            self.toggle = not self.toggle
            if self.toggle:
                self.color = self.color_on
            else:
                self.color= self.color_off
        if self.toggle:
            super().activate()

class Slider (Interactable_Element):
    MIN_DIM = 5
    def __init__(self, x, y, w, h, ext_display, is_vertical = True, update = utils.Ptr(False), current:utils.Ptr = utils.Ptr(5), max = 10, min = 0, phantom_dist = 32, color = Element.DEFAULT_GREY, border_width = Interactable_Element.DEFAULT_BORDER_W, p_button=Interactable_Element.DEFAULT_MB, draw_border=True, activation_key=-1, scale=True, step =1):
        self.current = current
        self.max = max
        self.min = min
        self.range = (max - min)/step
        self.step = step
        current_pos = (self.current.value - self.min)/(self.max-self.min)
        self.current = current
        self.orientation = is_vertical
        self.refresh = update
        if is_vertical:
            height = h /self.range
            if height < self.MIN_DIM:
                height = self.MIN_DIM
            self.slider = Sticky(x,current_pos * h + y,w, height,ext_display,color = color,lock_x=True, phantom_dist=phantom_dist,border_width=0, scale=scale)
        else:
            width = w /self.range
            if width < self.MIN_DIM:
                width = self.MIN_DIM
            self.slider = Sticky(current_pos * w + x,y,width,h,ext_display,color = color, lock_y=True,phantom_dist=phantom_dist,border_width=0,scale = scale)
        super().__init__(x, y, w, h, ext_display, color, border_width, p_button, draw_border, activation_key, scale)
        self.moved = False
        self.old = self.current.value


    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        super().update(m_x,m_y,mouse,keys)
        if self.moved:
            self.moved = False
        if self.refresh.value or self.current.value != self.old:
            self.old = self.current.value
            self.refresh.value = False
            self.range = (self.max - self.min)/self.step
            factor = ((self.current.value-self.min)/self.range)/self.step
            if self.orientation:
                self.slider.y = self.y + self.h * factor
            else:
                self.slider.x = self.x + self.w * factor
        else:
            self.slider.update(m_x,m_y,mouse,keys)
            if self.slider.moved:
                if self.orientation:
                    self.slider.y = utils.clamp(self.slider.y,self.y+self.h - self.slider.h,self.y)
                    self.current.value = int(self.step * (self.slider.y - self.y)/self.h * self.range + self.min)
                else:
                    self.slider.x = utils.clamp(self.slider.x,self.x+self.w  - self.slider.w,self.x)
                    self.current.value = int(self.step * (self.slider.x - self.x)/self.w * self.range + self.min)
                self.moved = True
                self.old = self.current.value

    def render(self):
        if self.orientation:
            pygame.draw.line(self.ext_display,self.color,(self.x + self.w/2,self.h + self.y),(self.x + self.w/2, self.y),width=int(self.w/8))
        else:
            pygame.draw.line(self.ext_display,self.color,(self.x + self.w, self.y + self.h/2), (self.x, self.y + self.h/2),width=int(self.h/8))
        self.slider.render()
        


class Resizable(Sticky):
    DEFAULT_CORNER = 10
    BOX_DIST = 60
    DEFAULT_CORNER_COLOR = (180,180,250)
    MIN_W = 10
    MIN_H = 10

    def __init__ (self, x, y, w, h, ext_display: pygame.surface, action : callable = None, color:tuple = Element.DEFAULT_GREY, border_width : int = Interactable_Element.DEFAULT_BORDER_W, 
                  p_button = Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1, args = None, lock_x = False, lock_y = False, corner_w = DEFAULT_CORNER, 
                  corner_color = DEFAULT_CORNER_COLOR, render_corner = True, lock_all = False, render_show = True, has_show = True, force_render:utils.Ptr = utils.FALSE_PTR, scale = True):
            super().__init__(x,y,w,h,ext_display,action,color,border_width,p_button,draw_border,activation_key,args, lock_x, lock_y, lock_all, phantom_dist=4 * self.BOX_DIST, scale = scale)
            self.corner = Sticky(x+w-corner_w,y+h,corner_w, corner_w,ext_display, color=corner_color, phantom_dist=self.BOX_DIST, scale = scale)
            if has_show:
                self.show = Swtich(x,y - corner_w,corner_w, corner_w, ext_display, start_state= True, scale = scale)
            self.render_show = render_show
            self.__has_show = has_show
            self.render_corner = render_corner
            self.__mouse_check = True
            self.force_render = force_render

    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
         exit = False
         if self.__has_show and not self.lock_all:
             self.show.update(m_x,m_y,mouse,keys)
             if not self.show.toggle:
                 exit = True
         if (mouse.alive):
            self.__mouse_check = False
            exit = True
         else:
             self.__mouse_check = True
         if exit:
             return
         super().update(m_x, m_y, mouse, keys)
         self.corner.lock_all = (self.corner.state != utils.Mouse_State.PRESSED) and self.lock_all
         self.corner.update(m_x,m_y,mouse,keys)
         if (not self.lock_all and not self.corner.lock_all and not self.moved):
            self.w =  self.corner.x - self.x + self.corner.w
            self.h =  self.corner.y - self.y
            if (self.w < self.MIN_W):
                self.w = self.MIN_W
                self.moved = True
            if (self.h < self.MIN_H):
                self.h = self.MIN_H
                self.moved = True
                
         if self.moved:
             self.corner.x = self.x + self.w - self.corner.w
             self.corner.y = self.y + self.h
             if self.__has_show:
                 self.show.x = self.x
                 self.show.y = self.y - self.show.w
             

    def render_UI(self):
        if self.__mouse_check and (self.force_render.value or not self.lock_all):
            if self.render_corner:
                if self.force_render:
                    if self.__has_show:
                        if self.show.toggle:
                            self.corner.render()
                    else:
                        self.corner.render()
            if self.__has_show and self.render_show:
                self.show.render()

    def render_body(self):
            super().render()

    def render(self):
        if self.force_render.value or not self.__has_show or self.show.toggle:
            self.render_body()
        self.render_UI()

class Mouse_Cursor(Interactable_Element):
    def __init__ (self, x, y, w, h, ext_display: pygame.surface, color:tuple = Element.DEFAULT_GREY, border_width : int = Interactable_Element.DEFAULT_BORDER_W, 
                    p_button = Interactable_Element.DEFAULT_MB, draw_border = True, activation_key = -1, scale = True):
            self.alive = False
            super().__init__(x,y,w,h,ext_display,color,border_width,p_button,draw_border,activation_key=activation_key, scale = scale)

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

    def __init__ (self, x, y, w, h, ext_display : pygame.Surface, data : utils.Partial, filled_color : tuple = DEFAULT_FILLED, empty_color : tuple = DEFAULT_EMPTY, dead_color : tuple = DEFAULT_DEAD, scale = True):
        super().__init__(x,y,w,h,ext_display, scale)
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


class UI_Sub_Screen(Element):
    def __init__ (self, x, y, w, h, ext_display: pygame.surface, color:tuple = Element.DEFAULT_GREY, render = False, draw_background = False, scale = True):
            self.render_elements = render
            self.elements = []
            self.has_back = draw_background
            super().__init__(x,y,w,h,ext_display,color, scale)

    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        if self.render_elements:
            for element in self.elements:
                element.update(m_x, m_y, mouse, keys)

    def render(self):
         if self.render_elements:
            if self.has_back:
                super().render()
            for element in self.elements:
                element.render()

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

class UI_Heirarchy(UI_Composite):
    def __init__(self, ext_disp : pygame.Surface, draw_background = True, background_color = UI_Composite.DEFAULT_BACK):
        super().__init__(ext_disp,draw_background,background_color)
        self.sub_composites = []

    def focus(self,id):
        for i in range (len(self.sub_composites)):
            if i != id:
                self.sub_composites[i].render_elements = False
            else:
                self.sub_composites[i].render_elements = True

    def update(self, mouse, keys):
        coor = mouse.poll_rel()
        size = self.display.size
        m_x = coor[0] * size[0]
        m_y = coor[1] * size[1]
        for screen in self.sub_composites:
            screen.update(m_x, m_y, mouse, keys)
        return super().update(mouse, keys)
    
    def render(self):
        super().render()
        for screen in self.sub_composites:
            screen.render()
        
class UI_Internal_Window(Resizable):
    
    DEFAULT_MB = 2
    def __init__ (self, x, y, w, h, i_w, i_h, ext_display: pygame.surface, has_background = False, background:tuple = Element.DEFAULT_GREY, border_width : int = Interactable_Element.DEFAULT_BORDER_W, 
                  corner_w = Resizable.DEFAULT_CORNER, corner_color = Resizable.DEFAULT_CORNER_COLOR, render_corner = True, lock_all = False, render_show = True, has_show = True, p_button = DEFAULT_MB, scale = True):
        super().__init__(x,y,w,h,ext_display, color=background, corner_w=corner_w, corner_color=corner_color,render_corner=render_corner,lock_all=lock_all, render_show=render_show,has_show=has_show, p_button=p_button, scale=scale)
        self.elements = []
        self.has_background = has_background
        self.back_color = background
        self.border_width = border_width
        self.int_screen = pygame.Surface((i_w,i_h))
        self.i_w = i_w
        self.i_h = i_h
        self.__update_scale()
        
    def update (self, m_x, m_y, mouse : utils.Mouse_Manager, keys):
        old_w = self.w
        old_h = self.h
        super().update(m_x, m_y, mouse, keys)
        if self.w != old_w or self.h != old_h:
            self.__update_scale()
        image_x = (m_x - self.x - self.b_w) * self.mouse_scale_facor_x
        image_y = (m_y - self.y - self.b_w) * self.mouse_scale_factor_y
        for element in self.elements:
            element.update(image_x, image_y, mouse, keys)

    def __update_scale(self):
        self.scale_w = self.w - self.b_w * 2
        self.scale_h = self.h - self.b_w * 2
        self.mouse_scale_facor_x = self.i_w/self.scale_w
        self.mouse_scale_factor_y = self.i_h/self.scale_h
        self.ext_screen = pygame.Surface((self.scale_w, self.scale_h))
        self.scaled = False

    def render_body(self):
        self._Interactable_Element__draw_border()
        if (self.has_background):
            self.int_screen.fill(self.back_color)
        for element in self.elements:
            element.render()
        pygame.transform.scale(self.int_screen, (self.scale_w, self.scale_h), self.ext_screen)
        self.ext_display.blit(self.ext_screen, (self.x + self.b_w, self.y + self.b_w))
