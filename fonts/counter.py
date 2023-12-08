import pygame

from biba import main_menu
import runpy
counter1 = 0
if counter1 >= 1:
    print("GOVNO1")
    runpy.run_path("biba.py")
    main_menu()
    pygame.display.flip()