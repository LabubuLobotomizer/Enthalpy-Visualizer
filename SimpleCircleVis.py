import pygame as pg
import numpy as np
import random as rand

pg.init

#Starting the view at (0,0)
camera_X = 0
camera_Y = 0
#Zoom base is the regular amount of pixels to be shown in the X direction, zoom factor is how zoomed out you are
zoomBase = 1280
zoomFactor = 1.0
#A value to determine what looks good, space in between lines on the grid
gridSize = 150
#Setting the size of the screen
screenWidth = 1280
screenHeight = 720

circlesList = []
cameraViewX = camera_X + (screenWidth / 2) / zoomFactor
cameraViewY = camera_Y + (screenHeight / 2) / zoomFactor

#Setting up the screen
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Simple Circle Visualizer")
clock = pg.time.Clock()

def getScreenCoordinates(worldX, worldY, cameraX, cameraY, zoomFactor):
    #Calculating the screen coordinates based on the world coordinates, camera position, and zoom factor
    global screenWidth, screenHeight
    screenX = (worldX - cameraX) * zoomFactor + (screenWidth / 2)
    screenY = (worldY - cameraY) * zoomFactor + (screenHeight / 2)
    return screenX, screenY

def getWorldCoordinates(screenX, screenY, cameraX, cameraY, zoomFactor):
    #Calculating the absolute coordinates based off of the screen coordinates given
    global screenWidth, screenHeight
    worldX = ((screenX - (screenWidth/2)) / zoomFactor)  + cameraX
    worldY = ((screenY - (screenHeight/2)) / zoomFactor) + cameraY
    return worldX, worldY

#This function will go before anything else happens each frame to draw the grid on the screen behind the circles
#Mostly put in place to create a reference for scale and position as you zoom out and move
def draw_grid(grid_size, zoom_factor, camera_x, camera_y, color: tuple = (int, int, int)):
    #Im gonna start at 0,0 draw each vertical line, then go back the 0,0 and draw each horizontal line
    global screenWidth, screenHeight
    #as we move left, the origin will move right
    tempX = 0
    tempDrawX = getScreenCoordinates(tempX, 0, camera_x, camera_y, zoom_factor)[0]
    #moving to the right of the screen, drawing each vertical line
    #Drawing the vertical lines
    #Drawing the ones to the right of the origin
    while tempDrawX < screenWidth:
        if tempDrawX < 0:
            tempX += grid_size
            tempDrawX = getScreenCoordinates(tempX, 0, camera_x, camera_y, zoom_factor)[0]
            continue
        pg.draw.line(screen, color, (tempDrawX, 0), (tempDrawX, screenHeight), 1)
        tempX += grid_size
        tempDrawX = getScreenCoordinates(tempX, 0, camera_x, camera_y, zoom_factor)[0]
    #drawing the ones to the left of the origin
    tempX = 0
    tempDrawX = getScreenCoordinates(tempX, 0, camera_x, camera_y, zoom_factor)[0]
    while tempDrawX > 0:
        if tempDrawX > screenWidth:
            tempX -= grid_size
            tempDrawX = getScreenCoordinates(tempX, 0, camera_x, camera_y, zoom_factor)[0]
            continue
        pg.draw.line(screen, color, (tempDrawX, 0), (tempDrawX, screenHeight), 1)
        tempX -= grid_size
        tempDrawX = getScreenCoordinates(tempX, 0, camera_x, camera_y, zoom_factor)[0]
    #Drawing the horizontal lines
    #Drawing the ones below the origin
    tempY = 0
    tempDrawY = getScreenCoordinates(0, tempY, camera_x, camera_y, zoom_factor)[1]
    while tempDrawY < screenHeight:
        if tempDrawY < 0:
            tempY += grid_size
            tempDrawY = getScreenCoordinates(0, tempY, camera_x, camera_y, zoom_factor)[1]
            continue
        pg.draw.line(screen, color, (0, tempDrawY), (screenWidth, tempDrawY), 1)
        tempY += grid_size
        tempDrawY = getScreenCoordinates(0, tempY, camera_x, camera_y, zoom_factor)[1]
    #drawing the ones above the origin
    tempY = 0
    tempDrawY = getScreenCoordinates(0, tempY, camera_x, camera_y, zoom_factor)[1]
    while tempDrawY > 0:
        if tempDrawY > screenHeight:
            tempY -= grid_size
            tempDrawY = getScreenCoordinates(0, tempY, camera_x, camera_y, zoom_factor)[1]
            continue
        pg.draw.line(screen, color, (0, tempDrawY), (screenWidth, tempDrawY), 1)
        tempY -= grid_size
        tempDrawY = getScreenCoordinates(0, tempY, camera_x, camera_y, zoom_factor)[1]

def drawCircles(CameraX, CameraY, ZoomFactor):
    global circlesList, screenWidth, screenHeight
    for Circle in circlesList:
        print()
        pg.draw.circle(screen, Circle[2], (getScreenCoordinates(Circle[0], Circle[1], CameraX, CameraY, ZoomFactor)), Circle[3]*zoomFactor)



#Running makes sure we didn't cancel
#Unlocked is just a toggle to lock key inputs, currently unused, but could be useful for a pause menu
running = True
unlocked = True
while running:
    #Locking the script at 60fps
    clock.tick(60)


    screen.fill((40, 40, 45))  # Clear the screen with black
    draw_grid(gridSize, zoomFactor, cameraViewX, cameraViewY, (0, 0, 0)) #Call the function above
    drawCircles(cameraViewX, cameraViewY, zoomFactor) #Draws all the circles


    pg.display.flip()  # Update the display

    #Gets a list of all pressed keys and does the actions for each one as described
    keys = pg.key.get_pressed()
    if unlocked:
        if keys[pg.K_UP]:
            zoomFactor *= 1.03
        if keys[pg.K_DOWN]:
            zoomFactor /= 1.03
        if keys[pg.K_w]:
            cameraViewY -= 10 / zoomFactor
        if keys[pg.K_s]:
            cameraViewY += 10 / zoomFactor
        if keys[pg.K_a]:
            cameraViewX -= 10 / zoomFactor
        if keys[pg.K_d]:
            cameraViewX += 10 / zoomFactor

    #gets only the keys that were first pressed between this frame and last, not the ones that were held down
    #can also get other inputs like the X button being pressed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                circleWorld = getWorldCoordinates(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], cameraViewX, cameraViewY, zoomFactor)
                circlesList.append([circleWorld[0], circleWorld[1], (rand.randint(0,255), rand.randint(0,255), rand.randint(0,255)), rand.randint(10, 600)])
                print(circleWorld)
