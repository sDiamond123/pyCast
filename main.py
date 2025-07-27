import pygame
from pygame.locals import *
import world, utils, clock, options
from log import LOG as log

if __name__ == "__main__":
    # pygame setup
    pygame.init()
    config = options.CONFIG
    name = config.contents[config.WINDOW_NAME]
    pygame.display.set_caption(name)
    pygame.display.set_icon(pygame.image.load(config.contents[config.ICON]))
    fullscreen = config.contents[config.FULLSCREEN]
    w = config.contents[config.W]
    h = config.contents[config.H]
    fps = config.contents[config.FPS]
    i_w = config.contents[config.I_W]
    i_h = config.contents[config.I_H]
    x_sense = config.contents[config.X_SENSE]
    y_sense = config.contents[config.Y_SENSE]
    fov = config.contents[config.FOV]
    rays = config.contents[config.RAYS]
    draw_dist = config.contents[config.DRAW_DIST]


    #print out config to terminal
    log.write ("Started: "+name+" \n Window: " + str(w) + " by " + str(h) +" \n Fullscreen: "+str(fullscreen)+
           " \n Internal Resolution: "+str(i_w)+" by "+ str(i_h)+" \n Targeting " + str(fps) +" FPS")
    
    # finish pygame init
    if not fullscreen:
        screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
    else:
        screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
    running = True
    dt = 0

    mouse = utils.Mouse_Manager((x_sense,y_sense),(w,h))
    #manager = world.World(screen,w,h,i_w, i_h, "basic_mansion.csv")
    manager = world.World(screen, w,h,i_w,i_h,"built_in/town.csv",(fov,rays,draw_dist))
    #manager = world.World(screen, w, h, i_w, i_h, "default.csv")
    print(name + " started")
    log.write("Game Start!")
    # main loop
    while running:
        
        # poll for events
        mouse.set_mouse_wheel(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                if event.type == MOUSEWHEEL:
                    mouse.set_mouse_wheel(event.y)
                elif event.type == VIDEORESIZE:
                    mouse.resize(screen.size)
                    w = screen.size[0]
                    
        # run a frame of the game
        if running:
            keys = pygame.key.get_pressed()
            running = manager.update(keys, mouse)
            manager.render()
            if mouse.alive:
                # if we are holding mouse, reset position
                # for some reason this doesn't work in the mouse class
                pygame.mouse.set_pos((w/2, mouse.abs[1]))
            # push frame to screen
            pygame.display.flip()

            # limits FPS
            dt = clock.CLOCK.tick(fps.value) / 1000
            #print(clock.get_fps())
    log.write(name + " Succesfully Exited")
    print(name + " exited\nsee data/log.txt for more info")
    log.dump()
    pygame.quit()