


import pygame as pg
import random as random
import numpy as np

#Want to open a window

pg.init()
width=1480
height=800
# n=0

clock=pg.time.Clock()
running=True
list=[]
list_items=1000
for i in range(list_items):
    list.append(int((i+1)*height/list_items))






random.shuffle(list)
screen=pg.display.set_mode((width,height))
pg.display.set_caption('676767676767676776766767767676776')
screen.fill('purple')

def order(list):
    for n in range(1,len(list)):
        if not list[n-1]<list[n]:
            return False
    return True
def sort(list,n):

    if list[n-1]>list[n]:
        list[n-1],list[n]=list[n],list[n-1]
ordered=order(list)
def insort(list,n):
    if list[n-1]>list[n]:
        list[n-1],list[n]=list[n],list[n-1]
        if n!=1:
            insort(list,n-1)

def escape(events):
    global running
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                return False
    return True


passthrough=0
while running:
    if not ordered:























        for n in range(1,len(list)-passthrough):
            screen.fill('purple')
            insort(list, n)
            for number in range( len(list)):  #draws all lines

                pg.draw.line(screen, 'white', (width * number / len(list), height),
                                 (width * number / len(list), height - list[number]), (int(width / len(list) * 0.9)))
            events=pg.event.get()
            esc=escape(events)
            if not esc:
                break
            pg.display.flip()
            # clock.tick(len(list))
        passthrough+=1
        ordered=order(list)

















    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False









    # pg.display.flip()
    # n+=1
    # if n==15000:
    #     break
print('all done')


