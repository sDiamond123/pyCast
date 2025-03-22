import pygame
from pygame.locals import MOUSEWHEEL
import world, utils, screen_writer

if __name__ == "__main__":
    # pygame setup
    pygame.init()
    # read in config file and set w/h
    # should probably move to it's own class, but whatever
    config = open("data/config/config.txt", "r")
    config.readline()
    name = config.readline().strip()
    pygame.display.set_caption(name)
    config.readline()
    pygame.display.set_icon(pygame.image.load(config.readline()[:-1]))
    config.readline()
    fullscreen = "true" == (config.readline().strip().lower())
    config.readline()
    w = int(config.readline())
    config.readline()
    h = int(config.readline())
    config.readline()
    fps = int(config.readline())
    config.readline()
    i_w = int(config.readline())
    config.readline()
    i_h = int(config.readline())
    config.readline()
    x_sense = int(config.readline())
    config.readline()
    y_sense = int(config.readline())
    config.close()

    #print out config to terminal
    print ("Started: "+name+"\nWindow: " + str(w) + " by " + str(h) +"\nFullscreen: "+str(fullscreen)+
           "\nInternal Resolution: "+str(i_w)+" by "+ str(i_h)+"\nTargeting " + str(fps) +" FPS")
    
    # finish pygame init
    if not fullscreen:
        screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
    else:
        screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    running = True
    dt = 0

    mouse = utils.Mouse_Manager((x_sense,y_sense),(w,h))
    #manager = world.World(screen,w,h,i_w, i_h, "basic_mansion.csv")
    manager = world.World(screen, w,h,i_w,i_h,"town.csv")
    #manager = world.World(screen, w, h, i_w, i_h, "default.csv")
    print("Game Start!")
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
            dt = clock.tick(fps) / 1000
            #print(clock.get_fps())
    print(name + " Succesfully Exited")
    pygame.quit()