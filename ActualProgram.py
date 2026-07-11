import SimpleCircleVis as SCV
import pygame as pg
import random as rand

SCV.InitEngine(1.0, 150, 1280, 720, 100)

font = pg.font.SysFont("Arial", 36)

running = True
unlocked = True
while running:
    
    SCV.clock.tick(60)  # Limit the frame rate to 60 FPS


    SCV.screen.fill((40, 40, 45))  # Clear the screen with Dark Grey
    SCV.drawBorder(SCV.borderWidth, SCV.borderHeight)
    SCV.SetChunks()
    SCV.updateCircles()
    SCV.drawCircles(SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor) #Draws all the circles

    #Text
    TotalVelocityText = font.render("Total Velocity: " + SCV.CalcTotalVelo(), True, (255, 255, 255))
    SCV.screen.blit(TotalVelocityText, (50,50))


    SCV.pg.display.flip()


 #Gets a list of all pressed keys and does the actions for each one as described
    keys = pg.key.get_pressed()
    if unlocked:
        if keys[pg.K_UP]:
            SCV.zoomFactor *= 1.03
        if keys[pg.K_DOWN]:
            SCV.zoomFactor /= 1.03
        if keys[pg.K_w]:
            SCV.cameraViewY -= 10 / SCV.zoomFactor
        if keys[pg.K_s]:
            SCV.cameraViewY += 10 / SCV.zoomFactor
        if keys[pg.K_a]:
            SCV.cameraViewX -= 10 / SCV.zoomFactor
        if keys[pg.K_d]:
            SCV.cameraViewX += 10 / SCV.zoomFactor

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                circleWorld = SCV.getWorldCoordinates(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor)
                randXVelo = 0
                randYVelo = 0
                while randXVelo == 0:
                    randXVelo = rand.randint(-10, 10)
                while randYVelo == 0:
                    randYVelo = rand.randint(-10, 10)
                SCV.circlesList.append(SCV.Circle(circleWorld[0], circleWorld[1], (rand.randint(0,255), rand.randint(0,255), rand.randint(0,255)), rand.randint(5, 35), randXVelo, randYVelo, SCV.IDCounter))
                SCV.IDCounter += 1
