import pygame as pg
import numpy as np

#Init just required at the start
pg.init()
#Set the screen size caption and clock start and icon
Screen_Size_Height = 720
Screen_Size_Width = 1280
screen = pg.display.set_mode((Screen_Size_Width, Screen_Size_Height))
pg.display.set_caption("Fishing Game")
Time = pg.time.Clock()
Icon = pg.image.load("SGA.jpg")

#Load other images used
BallImage = pg.image.load("Basketball.jpg")
HoopImage = pg.image.load("Hoop.png")
pg.display.set_icon(Icon)

#Other Variables
CTime = 0
Hoop_X = 100
Hoop_Y = 100
Score = 0
Ball_Speed = 15

#Have to declare the font after init
Font = pg.font.SysFont("Arial", 30)

#List of all balls on screen format: [x,y]
Ball_List = []

#Adds the background color, hoop, score, and SGA
def Reset_Screen():
    screen.fill((abs(Red)*255, abs(Green)*255, abs(Blue)*255))
    screen.blit(Icon, pg.mouse.get_pos())
    screen.blit(HoopImage, (Hoop_X, Hoop_Y))
    screen.blit(ScoreText, (700, 100))
    
        
def Update_Balls(Target_X, Target_Y):
    #Temporary Variables to check if teh ball is in the hoop
    global Score

    for Ball in Ball_List:
        BallInX = False
        BallInY = False
        #Move the ball Sideways
        #print(Ball[0])
        if Ball[0] < Target_X-Ball_Speed*2:
            Ball[0] += Ball_Speed
        elif Ball[0] > Target_X+Ball_Speed*2:
            Ball[0] -= Ball_Speed

        #Check if the ball is in the hoop in the X direction
        if Ball[0] > Target_X-Ball_Speed*2 and Ball[0] < Target_X+Ball_Speed*2:
            BallInX = True

        #Move the ball upwards
        if Ball[1] < Target_Y-Ball_Speed*2:
            Ball[1] += Ball_Speed
        elif Ball[1] > Target_Y+Ball_Speed*2:
            Ball[1] -= Ball_Speed

        #Check if the ball is in the hoop in the Y direction
        if Ball[1] > Target_Y-Ball_Speed*2 and Ball[1] < Target_Y+Ball_Speed*2:
            BallInY = True

        #If the ball is in the hoop, add to score and remove ball from list
        print("BallInX: ", BallInX, "BallInY: ", BallInY)
        if BallInX and BallInY:
            Score += 1
            Ball_List.remove(Ball)

        #Draw the ball on the screen
        screen.blit(BallImage, (Ball[0], Ball[1]))



while True:
    #A Variable of time
    CTime += Time.tick(60) / 1000
    #Use Sine and Cosine functions to create a color changing background
    Red = np.sin(CTime)
    Green = np.cos(CTime)
    Blue = np.sin(CTime+1)

    #Set the score text
    ScoreText = Font.render("Score: " + str(Score), True, (0,0,0))

    #call function above

    Reset_Screen()
    Update_Balls(Hoop_X, Hoop_Y)
    #Basically everything you add to the screen is stored in a queue then the display flip updates to whatever is stored in queue
    pg.display.flip()
    print(Ball_List)

    #Set FPS to 60
    Time.tick(60)
    #Detect Events, Mouse clicks and Quit
    for event in pg.event.get():
        #Mouse Clicked, Shoot Ball
        if event.type == pg.MOUSEBUTTONDOWN:
            print("Mouse Clicked at: ", pg.mouse.get_pos())
            Ball_List.append([pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]])
        #Quit Event
        if event.type == pg.QUIT:
            pg.quit()
            quit()