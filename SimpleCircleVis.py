import pygame as pg
import numpy as np
import random as rand

def InitEngine(zFactor, gSize, sWidth, sHeight, CGirth):
    #Setting global Variables
    global zoomFactor
    zoomFactor = zFactor
    global gridSize
    gridSize = gSize
    global screenWidth
    global screenHeight
    screenWidth = sWidth
    screenHeight = sHeight
    global borderWidth
    global borderHeight
    borderWidth = screenWidth
    borderHeight = screenHeight
    global camera_X
    global camera_Y
    global cameraViewX
    global cameraViewY
    camera_X = -1*screenWidth/2
    camera_Y = -1*screenHeight/2
    cameraViewX = camera_X + (screenWidth / 2) / zoomFactor
    cameraViewY = camera_Y + (screenHeight / 2) / zoomFactor
    global circlesList
    circlesList = []
    global IDCounter
    IDCounter = 0
    global chunklist
    global ChunkGirth
    ChunkGirth = CGirth
    chunklist = []
    for i in range(borderWidth // ChunkGirth):
        chunklist.append([])
        for j in range(borderHeight // ChunkGirth):
            chunklist[i].append([])


    #Setting Pygame Screen
    pg.init()
    global screen
    screen = pg.display.set_mode((screenWidth, screenHeight))
    global clock
    clock = pg.time.Clock()
    pg.display.set_caption("Enthalpy Visualizer")

class Circle():
    def __init__(self, X_Pos, Y_Pos, Circle_Color, Radius, X_Velo, Y_Velo, UID, chunkX=None, chunkY=None):
        self.xPosition = X_Pos
        self.yPosition = Y_Pos
        self.xVelocity = X_Velo
        self.yVelocity = Y_Velo
        self.radius = Radius
        self.color = Circle_Color
        self.uid = UID
        self.NewX = self.xPosition + self.xVelocity
        self.NewY = self.yPosition + self.yVelocity
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
    def getUID(self):
        return self.uid
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
    def updateChunk(self, NewChunkX=None, NewChunkY=None):
        if NewChunkX is not None:
            self.chunkX = NewChunkX
        if NewChunkY is not None:
            self.chunkY = NewChunkY
    def findChunk(self):
        global ChunkGirth, borderWidth, borderHeight
        ChunkX = int((self.xPosition + (borderWidth/2)) // ChunkGirth)
        ChunkY = int((self.yPosition + (borderHeight/2)) // ChunkGirth)
        return ChunkX, ChunkY
    
def SetChunks():
    global chunklist, borderWidth, borderHeight, ChunkGirth
    chunklist = []
    for i in range((borderWidth // ChunkGirth)+1):
        chunklist.append([])
        for j in range((borderHeight // ChunkGirth)+1):
            chunklist[i].append([])
    for RCircle in circlesList:
        ChunkX, ChunkY = Circle.findChunk(RCircle)
        if 0 <= ChunkX < len(chunklist) and 0 <= ChunkY < len(chunklist[ChunkX]):
            chunklist[ChunkX][ChunkY].append(RCircle)
            Circle.updateChunk(RCircle, NewChunkX=ChunkX, NewChunkY=ChunkY)

def drawBorder(BWidth, BHeight):
    global cameraViewX, cameraViewY, zoomFactor, gridSize
    #Draws a shaded box
    pg.draw.rect(screen, (60, 60, 65), (getScreenCoordinates(BWidth/-2, 0, cameraViewX, cameraViewY, zoomFactor)[0], getScreenCoordinates(0, BHeight/-2, cameraViewX, cameraViewY, zoomFactor)[1], BWidth*zoomFactor, BHeight*zoomFactor))
    #Draw Grid
    draw_grid(gridSize, zoomFactor, cameraViewX, cameraViewY, (0, 0, 0)) #Call the function above
    #Drawing Bottom Line
    pg.draw.line(screen, (255,255,255), getScreenCoordinates(BWidth/2, BHeight/2, cameraViewX, cameraViewY, zoomFactor), getScreenCoordinates(-1*BWidth/2, BHeight/2, cameraViewX, cameraViewY, zoomFactor))
    #Drawing Top Line
    pg.draw.line(screen, (255,255,255), getScreenCoordinates(BWidth/2, -1*BHeight/2, cameraViewX, cameraViewY, zoomFactor), getScreenCoordinates(-1*BWidth/2, -1*BHeight/2, cameraViewX, cameraViewY, zoomFactor))
    #Drawing Left Line
    pg.draw.line(screen, (255,255,255), getScreenCoordinates(-1*BWidth/2, BHeight/2, cameraViewX, cameraViewY, zoomFactor), getScreenCoordinates(-1*BWidth/2, -1*BHeight/2, cameraViewX, cameraViewY, zoomFactor))
    #Drawing Right Line
    pg.draw.line(screen, (255,255,255), getScreenCoordinates(BWidth/2, BHeight/2, cameraViewX, cameraViewY, zoomFactor), getScreenCoordinates(BWidth/2, -1*BHeight/2, cameraViewX, cameraViewY, zoomFactor))
    #Draw a 0,0 circle
    pg.draw.circle(screen, (255,0,0), getScreenCoordinates(0, 0, cameraViewX, cameraViewY, zoomFactor), 2)

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
    global circlesList
    global chunklist
    #First we check collision, but the second circle must make sure that it is not doing circles that are before the main circle in the list as to not double update teh collision
    for QCircle in circlesList:
        #Preparing a bunch of variables because it'll be faster to prepare them than to call the functions a bunch
        MainCircleX = Circle.getX(QCircle)
        MainCircleY = Circle.getY(QCircle)
        MainCircleR = Circle.getRadius(QCircle)
        MainCircleMatrix = np.array([MainCircleX,MainCircleY])
        #BCircle is the circle we are testing the main circle against before updating the main circle
        ThisChunkX, ThisChunkY = Circle.findChunk(QCircle)
        #List of Ids is the ones in the same chunk to test
        ListofNearbyCircles = []
        for x, chunks in enumerate(chunklist):
            if x in range(ThisChunkX-1, ThisChunkX+2):
                for y, subchunks in enumerate(chunks):
                    if y in range(ThisChunkY-1, ThisChunkY+2):
                        for Lcircle in subchunks:
                            ListofNearbyCircles.append(Lcircle)
        for BCircle in ListofNearbyCircles:
            #The actual collision code
            if circlesList.index(BCircle) > circlesList.index(QCircle):
                    MainCircleVelocityMatrix = np.array([Circle.getXV(QCircle), Circle.getYV(QCircle)])
                    SecondaryCircleX = Circle.getX(BCircle)
                    SecondaryCircleY = Circle.getY(BCircle)
                    SecondaryCircleR = Circle.getRadius(BCircle)
                    #Checking the distance between the two to see if collision occurs
                    distanceBetweenCircles = (((MainCircleX-SecondaryCircleX)**2) + ((MainCircleY-SecondaryCircleY)**2))
                    if distanceBetweenCircles < (MainCircleR+SecondaryCircleR)**2:
                        #Now we have to do that complicated ish math, For now everything is perfectly elastic
                        SecondaryCircleMatrix = np.array([SecondaryCircleX,SecondaryCircleY])
                        SecondaryCircleVelocityMatrix = np.array([Circle.getXV(BCircle), Circle.getYV(BCircle)])
                        normalVector = (MainCircleMatrix - SecondaryCircleMatrix) #Getting difference between them
                        if np.linalg.norm(normalVector) == 0:
                            normalVector = np.array([1, 0])
                        else:
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
    TotalVelo = np.round(TotalVelo)
    return(str(TotalVelo))

def getCircleTouchingMouse(mouseX, mouseY, cameraX, cameraY, zoomFactor):
    global circlesList
    for ACircle in circlesList:
        CircleScreenX, CircleScreenY = getScreenCoordinates(Circle.getX(ACircle), Circle.getY(ACircle), cameraX, cameraY, zoomFactor)
        if ((mouseX - CircleScreenX)**2 + (mouseY - CircleScreenY)**2) < (Circle.getRadius(ACircle)*zoomFactor)**2:
            return ACircle
    return None

def getCircleByUID(UID):
    global circlesList
    for ACircle in circlesList:
        if Circle.getUID(ACircle) == UID:
            return ACircle
    return None