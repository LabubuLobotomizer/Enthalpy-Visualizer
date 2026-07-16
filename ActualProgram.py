import SimpleCircleVis as SCV
import pygame as pg
import random as rand
import Enthalpy_Zones as ENTH

#region startup/init
SCV.InitEngine(1.0, 150, 1280, 720, 100)

font = pg.font.SysFont("Arial", 36)
stored_dh=0
running = True
Cameraunlocked = True
Circlesunlocked = True
CircleLockCD = 0
GuiVisible = True
GUIToggleCD = 0
selectedCircle = None
# endregion
WallStarted = None
WallEnding = None
TempMouseWall = SCV.Wall(0, 0, 0, 0, 15, (255,0,255))

def camera_mov_and_circle_lock():
    global CircleLockCD
    global Circlesunlocked
    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        SCV.zoomFactor *= 1.03
    if keys[pg.K_DOWN]:
        SCV.zoomFactor /= 1.03
    if Cameraunlocked:
        if keys[pg.K_w]:
            SCV.cameraViewY -= 10 / SCV.zoomFactor
        if keys[pg.K_s]:
            SCV.cameraViewY += 10 / SCV.zoomFactor
        if keys[pg.K_a]:
            SCV.cameraViewX -= 10 / SCV.zoomFactor
        if keys[pg.K_d]:
            SCV.cameraViewX += 10 / SCV.zoomFactor
    if keys[pg.K_SPACE]:
        if CircleLockCD == 0:
            Circlesunlocked = not Circlesunlocked
            CircleLockCD = 30  #

def os_events():
    global selectedCircle
    global WallStarted
    global WallEnding
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False
            if event.key == pg.K_l:
                if WallStarted is not None:
                    SCV.wallsList.append(SCV.Wall(WallStarted[0], WallStarted[1], WallEnding[0], WallEnding[1], 15, (255,0,255)))
                    WallStarted = None
                else:
                    WallStarted = SCV.getWorldCoordinates(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor )
        #Mouse Input
        if event.type == pg.MOUSEBUTTONDOWN:
            #Left Clicking to create a circle
            if event.button == 1:
                circleWorld = SCV.getWorldCoordinates(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor)
                randXVelo = 0
                randYVelo = 0
                while randXVelo == 0:
                    randXVelo = rand.randint(-20, 20)
                while randYVelo == 0:
                    randYVelo = rand.randint(-20, 20)
                SCV.circlesList.append(SCV.Circle(circleWorld[0], circleWorld[1], (rand.randint(0,255), rand.randint(0,255), rand.randint(0,255)), rand.randint(15, 35), randXVelo, randYVelo, SCV.IDCounter))
                SCV.IDCounter += 1
            #Right Clicking to select a circle
            if event.button == 3:
                if selectedCircle is not None:
                    if selectedCircle == SCV.getCircleTouchingMouse(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor):
                        selectedCircle = None
                        print("Selected Circle UID:none")
                    else:
                        selectedCircle = SCV.getCircleTouchingMouse(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor)
                        if selectedCircle is not None:
                            print("Selected Circle UID:" + str(SCV.Circle.getUID(selectedCircle)))
                else:
                    selectedCircle = SCV.getCircleTouchingMouse(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor)
                    if selectedCircle is not None:
                        print("Selected Circle UID:" + str(SCV.Circle.getUID(selectedCircle)))
        if event.type == pg.MOUSEWHEEL:
            if event.y > 0:
                SCV.zoomFactor *= 1.1
            elif event.y < 0:
                SCV.zoomFactor /= 1.1
    return True

def pg_frames_and_screenfill():
    SCV.clock.tick(60)  # Limit the frame rate to 60 FPS

    SCV.screen.fill((40, 40, 45))  # Clear the screen with Dark Grey
    SCV.drawBorder(SCV.borderWidth, SCV.borderHeight)
    SCV.SetChunks()

def circle_lock():

    if Circlesunlocked:
        SCV.updateCircles()
    SCV.drawCircles(SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor) #Draws all the circles

    if selectedCircle is not None:
        # Draw a highlight around the selected circle
        CircleScreenX, CircleScreenY = SCV.getScreenCoordinates(SCV.Circle.getX(selectedCircle), SCV.Circle.getY(selectedCircle), SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor)
        pg.draw.circle(SCV.screen, (255, 0, 0), (int(CircleScreenX), int(CircleScreenY)), int(SCV.Circle.getRadius(selectedCircle) * SCV.zoomFactor) + 5, 3)

while running:
    pg_frames_and_screenfill()

    circle_lock()

    if WallStarted is not None:
        WallEnding = SCV.getWorldCoordinates(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor )
        SCV.Wall.updateWallPositions(TempMouseWall, NewStartX = WallStarted[0], NewStartY = WallStarted[1], NewEndX = WallEnding[0], NewEndY= WallEnding[1])
        SCV.customWallDrawer(TempMouseWall, SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor)

    SCV.drawWalls(SCV.cameraViewX, SCV.cameraViewY, SCV.zoomFactor)
    #Draws the GUI if GuiVisible is True
    if GuiVisible:
        if selectedCircle is not None:
            Cameraunlocked = False
            SCV.cameraViewX = SCV.Circle.getX(selectedCircle)
            SCV.cameraViewY = SCV.Circle.getY(selectedCircle)
            pg.draw.rect(SCV.screen, SCV.Circle.getColor(selectedCircle), (10, 10, SCV.screenWidth//4, SCV.screenHeight//2))  # Draw a dark grey rectangle for the GUI background
        else:
            Cameraunlocked = True


    #region Velo printer
    TotalVelocityText = font.render("Total Velocity: " + SCV.CalcTotalVelo(), True, (255, 255, 255))
    SCV.screen.blit(TotalVelocityText, (50,50))

    if CircleLockCD > 0:
        CircleLockCD -= 1
    if GUIToggleCD > 0:
        GUIToggleCD -= 1
    SCV.pg.display.flip()
    vertices = [
        (0, 0),
        (1200, 0),
        (1200, 400),
        (0, 400),

    ]

    dh=ENTH.enthalpy(SCV.circlesList, vertices)
    if stored_dh<dh:
        print('gaining enthalpy in region +++++++++')

    elif stored_dh>dh:
        print('losing enthalpy ----------')
    else:
        print('enthalpy static')

    stored_dh=dh
    #endregion

 #Gets a list of all pressed keys and does the actions for each one as described
    camera_mov_and_circle_lock()


    running = os_events()