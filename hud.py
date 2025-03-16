import utils, map, pygame, player, texture, math

class HUD:
    MAP_X = 600
    MAP_Y = 20
    COMPASS_X = 300
    COMPASS_Y = 560
    COMPASS_W = 250
    COMPASS_H = 32
    COMPASS_PATH = "/compass/compass_scroll.bmp"
    #map
    map_w = 20
    map_h = 20
    map_trav_w = 4
    map_trav_h = 3
    default_map_w = 20
    default_map_h = 20
    map_cool_down = 100
    #h_bar
    h_x = 15
    h_y = 480
    h_w = 150
    h_h = 30
    h_filled = "crimson"
    h_empty = "grey"
    h_dead = "black"
    #cross_hair
    cross_size = 6
    cross_spacing = 0
    cross_color = "hot pink"
    #a_bar
    a_x = 15
    a_y = 515
    a_w = 150
    a_h = 30
    delta_a_y = 35
    a_filled = "yellow"
    a_empty = "grey"
    a_dead = "black"
    

    def __init__ (self, internal_screen :pygame.Surface, map : map.Map, player : player.Player):
        self.int_screen = internal_screen
        self.map = map
        self.player = player
        self.map_t = utils.Timed_Toggle(self.map_cool_down)
        self.compass = texture.RollingTexture(self.COMPASS_PATH, math.pi, math.pi , self.COMPASS_W, self.COMPASS_H)
    
    def map_zoom_in(self):
        if (self.map_t.clock):
                old_w = self.map_trav_w
                old_h = self.map_trav_h
                if (old_w > 0):
                    self.map_trav_w -= 1
                    self.map_w = self.map_w * (old_w * 2 + 1)/(self.map_trav_w * 2 + 1)
                if (old_h > 0):
                    self.map_trav_h -= 1
                    self.map_h = self.map_h * (old_h * 2 + 1)/(self.map_trav_h * 2 + 1)

    def map_zoom_out(self):
        if (self.map_t.clock):
                    old_w = self.map_trav_w
                    old_h = self.map_trav_h
                    self.map_trav_w += 1
                    self.map_trav_h += 1
                    self.map_w = self.map_w * (old_w * 2 + 1)/(self.map_trav_w * 2 + 1)
                    self.map_h = self.map_h * (old_h * 2 + 1)/(self.map_trav_h * 2 + 1)


    def update(self, mouse: utils.Mouse_Manager):
         self.map_t.update()
         self.__render_ch__ = mouse.alive
         if (mouse.alive):
            self.mouse_y = mouse.poll_rel()[1] * self.int_screen.size[1]
            self.mouse_x = mouse.poll_rel()[0] * self.int_screen.size[0]

    def __render_map__ (self):
         # render minimap
        self.map.rendermap (self.int_screen, self.player, self.map_trav_w, self.map_trav_h, self.MAP_X, self.MAP_Y, self.map_w, self.map_h)

    def __render_compass__ (self):
        self.compass.render(self.player.ang)
        self.int_screen.blit(self.compass.external_screen, (self.COMPASS_X,self.COMPASS_Y))

    def __render_bar__ (self, x, y, w,h, value, max_value, filled, empty, dead):
          # render health
        if value >= 0:
            fill_ratio = w * value/max_value
            pygame.draw.rect(self.int_screen, filled, (x, y, fill_ratio, h))
            pygame.draw.rect(self.int_screen, empty, (x + fill_ratio, y, w  - fill_ratio, h))
        else:
            pygame.draw.rect(self.int_screen, dead, (x,y,w,h))

    def __render_tree_dot_crosshair__ (self, x, y, color, size, spacing):
         three_halves = 3/2 * size
         one_half = size/2
         # draw bottom
         pygame.draw.rect(self.int_screen, color, (x + three_halves + spacing, y - one_half, size, size))
         # draw top
         pygame.draw.rect(self.int_screen, color, (x - three_halves + spacing, y - one_half, size, size))
         # draw middle
         pygame.draw.rect(self.int_screen, color, (x, y + three_halves + spacing, size, size))

    def render (self):
       self.__render_map__()
       self.__render_compass__()
       if self.__render_ch__:
            self.__render_tree_dot_crosshair__(self.mouse_x, self.mouse_y, self.cross_color, self.cross_size, self.cross_spacing)
       self.__render_bar__(self.h_x, self.h_y, self.h_w, self.h_h, self.player.health, self.player.MAX_HEALTH, self.h_filled, self.h_empty, self.h_dead)
       gun_state = self.player.get_weapon_state()
       self.__render_bar__(self.a_x, self.a_y, self.a_w, self.a_h, gun_state[0], gun_state[1], self.a_filled, self.a_empty, self.a_dead)
       self.__render_bar__(self.a_x, self.a_y + self.delta_a_y, self.a_w, self.a_h, gun_state[2], gun_state[3], self.a_filled, self.a_empty, self.a_dead)