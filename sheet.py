import ui, pygame, utils

class char_sheet (ui.UI_Internal_Window):
    DEFAULT_W = 500
    DEFAULT_H = 350
    def __init__(self, x, y, w, h, ext_display: pygame.surface):
        super().__init__(x,y,w,h,self.DEFAULT_W, self.DEFAULT_H, ext_display, has_background=True, background=pygame.Color("bisque3"))
        self.elements.append(ui.Resizable(50,50,200,150,self.int_screen, None, force_render=utils.TRUE_PTR))