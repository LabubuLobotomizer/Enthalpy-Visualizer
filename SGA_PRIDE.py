import pygame as pg
import numpy as np

pg.init()
Screen_Size_Height = 720
Screen_Size_Width = 1280
screen = pg.display.set_mode((Screen_Size_Width, Screen_Size_Height))
pg.display.set_caption("Fishing Game")
Time = 0
Icon = pg.image.load("SGA.jpg")
pg.display.set_icon(Icon)


while True:
    Time += 0.001
    Red = np.sin(Time)
    Green = np.cos(Time)
    Blue = np.sin(Time+1)


    

    print("Red: ", Red, "Green: ", Green, "Blue: ", Blue)
    screen.fill((abs(Red)*255, abs(Green)*255, abs(Blue)*255))

    screen.blit(Icon, pg.mouse.get_pos())

    pg.display.flip()



    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()