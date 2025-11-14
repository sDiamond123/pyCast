![Recording2025-11-13at19 00 41-ezgif com-crop](https://github.com/user-attachments/assets/7d5ed64e-c4a3-4193-b6c8-891dc6761ccc)

# What am I?
This was a [raycaster](https://en.wikipedia.org/wiki/Ray_casting) largely done as a proof of concept over the course of last year. 

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

![Recording2025-11-13at21 46 06-ezgif com-crop](https://github.com/user-attachments/assets/fda28d5a-ab4c-4a3e-8919-ca66f99789dd)

On exit, a log is automatically saved to:

    data/log.txt

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

# Features


## Different Weapons

![Recording2025-11-13at21 43 04-ezgif com-crop](https://github.com/user-attachments/assets/d1c752b5-8fc2-4974-8209-69165941b820)

## Reload Mechanics

![Recording2025-11-13at22 06 40-ezgif com-crop](https://github.com/user-attachments/assets/91d141a2-8028-47c8-8297-d02464582a7b)

## Rudamentary Enemy AI and Death Screen

![Recording2025-11-13at22 18 56-ezgif com-crop](https://github.com/user-attachments/assets/a4439637-1052-4c7f-a737-1b35d4db9abc)

## Dialouge System

![Recording2025-11-13at21 50 56-ezgif com-crop](https://github.com/user-attachments/assets/ac8c073c-5b95-48fc-a907-b2657cb383e2)

## Interactive Map

![Recording2025-11-13at22 09 22-ezgif com-crop](https://github.com/user-attachments/assets/ae5f5d5c-86b4-49b8-85d0-4f889339a192)

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/8d635c56-9266-4eee-b7da-68b170e8d433" />

## Animated Textures

![Recording2025-11-13at19 59 45-ezgif com-crop](https://github.com/user-attachments/assets/2ed58da5-fa1f-4a9b-89ae-406d92e3824e)

## Loading a save (Extras)

![Recording2025-11-13at20 03 29-ezgif com-crop](https://github.com/user-attachments/assets/f52b9bae-5be9-4667-9485-21bc5fcae969)

## Pause Menu

![Recording2025-11-13at22 13 24-ezgif com-crop](https://github.com/user-attachments/assets/a90ce9da-b7bf-492e-bd79-f6cba3f655cb)

## Exit Dialouge

![Recording2025-11-13at22 16 03-ezgif com-crop](https://github.com/user-attachments/assets/0b2bfa0a-abe9-4e78-91da-2e594bb7f14d)


# Screenshots

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/fb045869-d15b-464a-876e-8914390f7a4c" />

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/fcc3da69-9cc4-4246-b06a-2f8033bc3adc" />

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/9c7c65b6-a631-4552-b967-944426a23456" />

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/a206accb-6024-418e-9b78-d1c8ab78ad7c" />

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/5f5d6a79-29ba-482d-a21a-8ab134a40945" />








