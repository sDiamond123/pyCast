![Recording2025-11-13at19 00 41-ezgif com-crop](https://github.com/user-attachments/assets/7d5ed64e-c4a3-4193-b6c8-891dc6761ccc)

# What am I?
This was a raycaster largely done as a proof of concept over the course of last year. 

Most of what's here is mainly a placeholder as I continue to devolp the game. Turns out I like making the game systems more then I like making games. 

This game is built off of pygame, everything else has been made from scratch (with the exception of placeholder sprites -- art is hard)!

![Recording2025-11-13at19 09 25-ezgif com-crop](https://github.com/user-attachments/assets/27dfe319-bbb2-4149-8f53-157f349884a6)

# Dependancies
This is a raycaster devolped using pygame. [Pygame](https://www.pygame.org/wiki/GettingStarted) is required to run this game. 

# Playing the Game
To Run:

    python3 main.py

![Recording 2025-11-13 at 19 17 56](https://github.com/user-attachments/assets/bc6d47b7-9295-4de0-8539-c325106854cf)

You can open the pause menu ('p' by default) and exited by either exiting in the main menu, pressing escape (by default), or closing the window.

From the main menu:

    New: to expeirence the dialouge system
    Continue: Instant action or go right back to where you left off
    Load: Load saved games (not implemented)
    Extra: Load the differet test maps
    Settings: view and modify settings
    Exit: close the game
    
A log can be found in log.txt

# Settings

Graphics settings and keybindings can be changed from the settings menu. Most graphics settings require a restart to take effect.

<img width="600" height="450"  alt="image" src="https://github.com/user-attachments/assets/09e54501-28d8-4c47-97e5-a75f95892715" />


![Recording2025-11-13at19 31 50-ezgif com-crop](https://github.com/user-attachments/assets/56884783-8825-497e-af72-6610ac7f9a51)

There's also a rudimentary console (type 'help' for commands)

![Recording2025-11-13at19 38 54-ezgif com-crop](https://github.com/user-attachments/assets/9b4e4458-3ffa-4655-8716-ffe67e9b6af7)

# Notes

This was mostly done as a proof of concept. 
Graphics are CPU bound, attempted multi-threading to lack-luster results (think I'm running into python's global interpreter lock).

Got side tracked rewriting it in rust binding of SDL to avoid this, we'll see how it goes from there.

Custom saves are not implemented yet (loading is). 

When I last worked on it I was trying to get it to paritally load large maps from an overworld at runtime, instead of the entire map at load time.  This isn't really working (can see in test maps).

# Screenshots
Animated Textures

![Recording2025-11-13at19 59 45-ezgif com-crop](https://github.com/user-attachments/assets/2ed58da5-fa1f-4a9b-89ae-406d92e3824e)

Dialouge System

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/9d425e2a-ee91-4de3-981d-3f4a14580c5b" />

Loading a save (Extras)

![Recording2025-11-13at20 03 29-ezgif com-crop](https://github.com/user-attachments/assets/f52b9bae-5be9-4667-9485-21bc5fcae969)

Map

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/8d635c56-9266-4eee-b7da-68b170e8d433" />


Pause Menu

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/b3433047-561c-4df6-81d4-7217329ed78c" />

Exit Dialouge

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/df906c90-ed3e-4ccb-9e5b-25f84bb9ac72" />

Various in game screenshots

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/fcc3da69-9cc4-4246-b06a-2f8033bc3adc" />

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/9c7c65b6-a631-4552-b967-944426a23456" />







