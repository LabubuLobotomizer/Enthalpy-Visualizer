import pygame as pg
import numpy as np
import random as rand

pg.init()

#Zoom base is the regular amount of pixels to be shown in the X direction, zoom factor is how zoomed out you are
zoomBase = 1280
zoomFactor = 1.0
#A value to determine what looks good, space in between lines on the grid
gridSize = 150
#Setting the size of the screen
screenWidth = 1280
screenHeight = 720
#Setting a border for the circles to bounce around in, centered on 0,0
borderWidth = screenWidth
borderHeight = screenHeight
#Starting the view at (0,0)
camera_X = -1*screenWidth/2
camera_Y = -1*screenHeight/2

circlesList = []
cameraViewX = camera_X + (screenWidth / 2) / zoomFactor
cameraViewY = camera_Y + (screenHeight / 2) / zoomFactor

#Setting up the screen
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Simple Circle Visualizer")
clock = pg.time.Clock()

class Circle():
    def __init__(self, X_Pos, Y_Pos, Circle_Color, Radius, X_Velo, Y_Velo):
        self.xPosition = X_Pos
        self.yPosition = Y_Pos
        self.xVelocity = X_Velo
        self.yVelocity = Y_Velo
        self.radius = Radius
        self.color = Circle_Color
    def getX(self):
        return self.xPosition
    def getY(self):
        return self.yPosition
    def getXV(self):
        return self.xVelocity
    def getYV(self):
        return self.yVelocity
    def getRadius(self):
        return self.radius
    def getColor(self):
        return self.color
    #This is assuming that the newX and newY are none by default unless explicitly changed, that way it is easy to update one at a time
    def updatePos(self, NewX=None, NewY=None):
        if NewX is not None:
            self.xPosition = NewX
        if NewY is not None:
            self.yPosition = NewY
    def updateVelo(self, NewXV=None, NewYV=None):
        if NewXV is not None:
            self.xVelocity = NewXV
        if NewYV is not None:
            self.yVelocity = NewYV
    
def drawBorder(BWidth, BHeight):
    global cameraViewX, cameraViewY, zoomFactor
    #Drawing Bottom Line
    pg.draw.line(screen, (255,255,255), getScreenCoordinates(BWidth/2, BHeight/2, cameraViewX, cameraViewY, zoomFactor), getScreenCoordinates(-1*BWidth/2, BHeight/2, cameraViewX, cameraViewY, zoomFactor))
    #Drawing Top Line
    pg.draw.line(screen, (255,255,255), getScreenCoordinates(BWidth/2, -1*BHeight/2, cameraViewX, cameraViewY, zoomFactor), getScreenCoordinates(-1*BWidth/2, -1*BHeight/2, cameraViewX, cameraViewY, zoomFactor))
    #Drawing Left Line
    pg.draw.line(screen, (255,255,255), getScreenCoordinates(-1*BWidth/2, BHeight/2, cameraViewX, cameraViewY, zoomFactor), getScreenCoordinates(-1*BWidth/2, -1*BHeight/2, cameraViewX, cameraViewY, zoomFactor))
    #Drawing Right Line
    pg.draw.line(screen, (255,255,255), getScreenCoordinates(BWidth/2, BHeight/2, cameraViewX, cameraViewY, zoomFactor), getScreenCoordinates(BWidth/2, -1*BHeight/2, cameraViewX, cameraViewY, zoomFactor))

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
    for CurrentCircle in circlesList:
        #print(getScreenCoordinates(Circle.getX(CurrentCircle), Circle.getY(CurrentCircle), CameraX, CameraY, ZoomFactor))
        pg.draw.circle(screen, Circle.getColor(CurrentCircle), (getScreenCoordinates(Circle.getX(CurrentCircle), Circle.getY(CurrentCircle), CameraX, CameraY, ZoomFactor)), Circle.getRadius(CurrentCircle)*zoomFactor)

def updateCircles():
    #Defining things up here for optimization
    XVectorFlat = np.array([1 , 0])
    YVectorFlat = np.array([0 , 1])
    global circlesList
    #First we check collision, but the second circle must make sure that it is not doing circles that are before the main circle in the list as to not double update teh collision
    for QCircle in circlesList:
        #Preparing a bunch of variables because itll be faster to prepare them than to call the functions a bunch
        MainCircleX = Circle.getX(QCircle)
        MainCircleY = Circle.getY(QCircle)
        MainCircleR = Circle.getRadius(QCircle)
        MainCircleMatrix = np.array([MainCircleX,MainCircleY])
        #BCircle is the circle we are testing the main circle against before updating the main circle
        for BCircle in circlesList:
            if circlesList.index(BCircle) > circlesList.index(QCircle):
                MainCircleVelocityMatrix = np.array([Circle.getXV(QCircle), Circle.getYV(QCircle)])
                SecondaryCircleX = Circle.getX(BCircle)
                SecondaryCircleY = Circle.getY(BCircle)
                SecondaryCircleR = Circle.getRadius(BCircle)
                #Checking the distance between the two to see if collision occurs
                distanceBetweenCircles = np.sqrt(((MainCircleX-SecondaryCircleX)**2) + ((MainCircleY-SecondaryCircleY)**2))
                if distanceBetweenCircles < MainCircleR+SecondaryCircleR:
                    #Now we have to do that complicated ish math, For now everything is perfectly elastic
                    SecondaryCircleMatrix = np.array([SecondaryCircleX,SecondaryCircleY])
                    SecondaryCircleVelocityMatrix = np.array([Circle.getXV(BCircle), Circle.getYV(BCircle)])
                    normalVector = (MainCircleMatrix - SecondaryCircleMatrix) #Getting difference between them
                    normalVector = normalVector / np.linalg.norm(normalVector) #Converting it to normal vector
                    #Some like math thing about rotating the interaction to be 90* hit not the actual angle of contact
                    projection = np.dot(MainCircleVelocityMatrix - SecondaryCircleVelocityMatrix, normalVector)
                    NewMainCircleVelocityMatrix = MainCircleVelocityMatrix - (projection * normalVector)
                    NewSecondaryCircleVelocityMatrix = SecondaryCircleVelocityMatrix + (projection * normalVector)

                    Circle.updateVelo(QCircle, NewXV=NewMainCircleVelocityMatrix[0], NewYV=NewMainCircleVelocityMatrix[1])
                    Circle.updateVelo(BCircle, NewXV=NewSecondaryCircleVelocityMatrix[0], NewYV=NewSecondaryCircleVelocityMatrix[1])
                    
                    #Here we also have to separate overlapped circles
                    overlap = MainCircleR+SecondaryCircleR - np.sqrt(((MainCircleX-SecondaryCircleX)**2) + ((MainCircleY-SecondaryCircleY)**2))
                    MainCircleX += normalVector[0] * overlap
                    MainCircleY += normalVector[1] * overlap
                    Circle.updatePos(QCircle, NewX=MainCircleX, NewY=MainCircleY)
    global borderWidth, borderHeight
    #Now we check if circles are colliding with edges of our border
    for CCircle in circlesList:
        if Circle.getX(CCircle) > borderWidth/2:
            Circle.updateVelo(CCircle, NewXV=Circle.getXV(CCircle)*-1)
        if Circle.getX(CCircle) < -1*borderWidth/2:
            Circle.updateVelo(CCircle, NewXV=Circle.getXV(CCircle)*-1)
        if Circle.getY(CCircle) < -1*borderHeight/2:
            Circle.updateVelo(CCircle, NewYV=Circle.getYV(CCircle)*-1)
        if Circle.getY(CCircle) > 1*borderHeight/2:
            Circle.updateVelo(CCircle, NewYV=Circle.getYV(CCircle)*-1)
    #Now we gotta correct ones still outside of the border due to errors
    for CCircle in circlesList:
        if Circle.getX(CCircle) > borderWidth/2:
            Circle.updatePos(CCircle, NewX=((borderWidth/2) - 1))
        if Circle.getX(CCircle) < -1*borderWidth/2:
            Circle.updatePos(CCircle, NewX=((borderWidth/-2) + 1))
        if Circle.getY(CCircle) < -1*borderHeight/2:
            Circle.updatePos(CCircle, NewY=((borderHeight/-2) + 1))
        if Circle.getY(CCircle) > 1*borderHeight/2:
            Circle.updatePos(CCircle, NewY=((borderHeight/2) - 1))
    #Now we finally actually move the circles
    for PCircle in circlesList:
        Circle.updatePos(PCircle, NewX=Circle.getX(PCircle)+Circle.getXV(PCircle), NewY=Circle.getY(PCircle)+Circle.getYV(PCircle))
    

def CalcTotalVelo():
    global circlesList
    TotalVelo = 0
    for I in circlesList:
        TotalVelo += Circle.getXV(I)**2 + Circle.getYV(I)**2
    return(str(TotalVelo))



                    
font = pg.font.SysFont("Arial", 36)
#Running makes sure we didn't cancel
#Unlocked is just a toggle to lock key inputs, currently unused, but could be useful for a pause menu
running = True
unlocked = True
while running:
    #Locking the script at 60fps
    clock.tick(60)

    #Filling the screen with all the visual elements
    screen.fill((40, 40, 45))  # Clear the screen with Dark Grey
    pg.draw.rect(screen, (60, 60, 65), (getScreenCoordinates(borderWidth/-2, 0, cameraViewX, cameraViewY, zoomFactor)[0], getScreenCoordinates(0, borderHeight/-2, cameraViewX, cameraViewY, zoomFactor)[1], borderWidth*zoomFactor, borderHeight*zoomFactor))
    draw_grid(gridSize, zoomFactor, cameraViewX, cameraViewY, (0, 0, 0)) #Call the function above
    drawBorder(borderWidth, borderHeight)
    updateCircles()
    drawCircles(cameraViewX, cameraViewY, zoomFactor) #Draws all the circles
    pg.draw.circle(screen, (255,0,0), getScreenCoordinates(0, 0, cameraViewX, cameraViewY, zoomFactor), 2)
    TotalVelocityText = font.render("Total Velocity: " + CalcTotalVelo(), True, (255, 255, 255))
    screen.blit(TotalVelocityText, (50,50))

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
                circlesList.append(Circle(circleWorld[0], circleWorld[1], (rand.randint(0,255), rand.randint(0,255), rand.randint(0,255)), 15, rand.randint(-10, 10), rand.randint(-10, 10)))
