


import pygame as pg
import random as rand
import numpy as np

#Want to open a window

pg.init()
width=1480
height=800
n=0

clock=pg.time.Clock()
running=True


screen=pg.display.set_mode((width,height))
pg.display.set_caption('676767676767676776766767767676776')
screen.fill('purple')
while running:

    for event in pg.event.get():
        print(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    n += 0.01
    pg.draw.line(screen,'white',(n*50,400+100*np.tan((n))),(n*50+1,400+100*(np.sin(n))),5)
    pg.display.flip()
    # clock.tick(60)






    # pg.display.flip()
    # n+=1
    # if n==15000:
    #     break
print('all done')


