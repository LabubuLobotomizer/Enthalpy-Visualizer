import pygame as pg
import numpy as np
import random as rand

def InitEngine(zFactor, gSize, sWidth, sHeight, CGirth):
    #Setting global Variables so we can call these functions in another file
    #Makes this engine reusable across multiple projects
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
    global wallsList
    wallsList = []
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
    
class Wall():
    def __init__(self, StartX, StartY, EndX, EndY, Width, Color: tuple = (int, int, int), Permeability=1):
        self.StartingX = StartX
        self.StartingY= StartY
        self.EndingX = EndX
        self.EndingY = EndY
        #Total Width of wall all the way through btw
        self.WallWidth = Width
        self.WallColor = Color
        self.WallPermeability = Permeability
        #Defined a bunch of math stuff here so we don't have to calculate it every time we call iterate later
        self.WallStartPos = np.array([self.StartingX, self.StartingY])
        self.WallEndPos = np.array([self.EndingX, self.EndingY])
        self.WallRelativePos = self.WallEndPos - self.WallStartPos
        self.WallLength = np.linalg.norm(self.WallRelativePos)
        self.WallDirection = self.WallRelativePos / self.WallLength
        self.WallNormal = np.array([-self.WallDirection[0], self.WallDirection[1]])
    def getStartX(self):
        return(self.StartingX)
    def getStartY(self):
        return(self.StartingY)
    def getEndX(self):
        return(self.EndingX)
    def getEndY(self):
        return(self.EndingY)
    def getWidth(self):
        return(self.WallWidth)
    def getColor(self):
        return(self.WallColor)
    def getPermeability(self):
        return(self.WallPermeability)
    def getStartPosTuple(self):
        return((self.StartingX, self.StartingY))
    def getEndPosTuple(self):
        return((self.EndingX, self.EndingY))
    def getStartMatrix(self):
        return(self.WallStartPos)
    def getEndMatrix(self):
        return(self.WallEndPos)
    def getWallRelativePos(self):
        return(self.WallRelativePos)
    def getWallLength(self):
        return(self.WallLength)
    def getWallDirection(self):
        return(self.WallDirection)
    def getWallNormal(self):
        return(self.WallNormal)
    
def SetChunks():
    #This checks the x,y coordinates of each circle and assigns them to a chunk
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
    #Draws the border and grid, and basically the whole background
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
    #Draws circles, Lowest UID in list has the lowest Z order
    global circlesList, screenWidth, screenHeight
    for CurrentCircle in circlesList:
        #print(getScreenCoordinates(Circle.getX(CurrentCircle), Circle.getY(CurrentCircle), CameraX, CameraY, ZoomFactor))
        pg.draw.circle(screen, Circle.getColor(CurrentCircle), (getScreenCoordinates(Circle.getX(CurrentCircle), Circle.getY(CurrentCircle), CameraX, CameraY, ZoomFactor)), Circle.getRadius(CurrentCircle)*zoomFactor)

def drawWalls(CameraX, CameraY, ZoomFactor):
    #Draws all of the walls
    global wallsList, screenWidth, screenHeight
    for CurrentWall in wallsList:
        pg.draw.line(screen, Wall.getColor(CurrentWall), (getScreenCoordinates(Wall.getStartX(CurrentWall), Wall.getStartY(CurrentWall), CameraX, CameraY, ZoomFactor)), (getScreenCoordinates(Wall.getEndX(CurrentWall), Wall.getEndY(CurrentWall), CameraX, CameraY, ZoomFactor)), width= max(1, int(Wall.getWidth(CurrentWall) * zoomFactor)))

def runCirclesOnCirclesCollision():
    #So this is the bulk of the engine, and the name is self explanatory
    global circlesList
    global chunklist
    #QCircle is the "MainCircle" that we are iterating against
    for QCircle in circlesList:
        #Preparing a bunch of variables because it'll be faster to prepare them than to call the functions a bunch
        #Sadly, this does make it harder to read, but its a LOT faster
        MainCircleX = Circle.getX(QCircle)
        MainCircleY = Circle.getY(QCircle)
        MainCircleR = Circle.getRadius(QCircle)
        MainCircleMatrix = np.array([MainCircleX,MainCircleY])#Numpy Array for the win
        MainCircleVelocityMatrix = np.array([Circle.getXV(QCircle), Circle.getYV(QCircle)])
        ThisChunkX, ThisChunkY = Circle.findChunk(QCircle) #This defines the chunk that the main circle is in
        #List of NearbyCircles is the circles in the surrounding chunks that we are going to check for collisions
        #We can load the same class in separate lists and modify or call it from both and it accuratly reflects the changes
        ListofNearbyCircles = []
        #Using "enumerate" here is a big optimization
        #enumerate turns "chunklist" into a list of tuples: (index in chunklist, the value at the index)
        #This is useful, because now instead of ever having to call the index of the item we are looking at we have it saved in our for loop
        #basically we are iterating through the for loop with x, but changing chunks everytime to the value of chunklist at x
        #but its faster than updating them separately
        for x, chunks in enumerate(chunklist):
            if x in range(ThisChunkX-1, ThisChunkX+2): #checks if the chunk we are currently checking is bordering the chunk our main circle is in on the left or right, or vertical to it
                for y, subchunks in enumerate(chunks):
                    if y in range(ThisChunkY-1, ThisChunkY+2): #checks if the chunk is bordering vertically or in the same row
                        for Lcircle in subchunks: #goes through each circle in the chunk that we just verified is within range of needing to be checked
                            ListofNearbyCircles.append(Lcircle) #adds each circle to a new list we have to check
        #This is where we move onto actual collision code
        for BCircle in ListofNearbyCircles: #BCircle is the circle we need to check if we are colliding, we only iterate through list of nearby circles
            #here we check if the index of BCircle is greater than index of Qcircle
            #This makes sure we dont double the collisions, or collide Qcircle with itself
            #It may be faster to call the UID of each circle, but we don't have a proper benchmark system set up yet to test that theory
            if circlesList.index(BCircle) > circlesList.index(QCircle):
                    #We only define the necessary variables for distance calculation here for optimization reasons
                    SecondaryCircleX = Circle.getX(BCircle)
                    SecondaryCircleY = Circle.getY(BCircle)
                    SecondaryCircleR = Circle.getRadius(BCircle)
                    #Checking the distance between the two to see if collision occurs
                    distanceBetweenCircles = (((MainCircleX-SecondaryCircleX)**2) + ((MainCircleY-SecondaryCircleY)**2)) 
                    #Both sides are squared like you suggested
                    if distanceBetweenCircles < (MainCircleR+SecondaryCircleR)**2:
                        #Here we define more variables that wouldn't have needed to be defined if overlap wasn't there
                        SecondaryCircleMatrix = np.array([SecondaryCircleX,SecondaryCircleY])
                        SecondaryCircleVelocityMatrix = np.array([Circle.getXV(BCircle), Circle.getYV(BCircle)])
                        #This is not the definition of the normal vector, but first we get the relative position between them
                        #We update this variable later, but it is more efficient to reuse variable than make new one for everything
                        normalVector = (MainCircleMatrix - SecondaryCircleMatrix)
                        #If np.linalg.norm(normalVector) returns 0, then that means that the circles have the exact same coordinates
                        #If we dont have a special case for this we run into a divide by 0 error
                        if np.linalg.norm(normalVector) == 0:
                            #Sets an arbitrary value if it is 0
                            normalVector = np.array([1, 0])
                        else:
                            #Here We actually turn the normalVector Variable into a normal Vector
                            #A Normal vector is a vector who's point lies at 0,0 and the unit circle
                            #But in this case we basically just mean it has a length of exactly 1
                            normalVector = normalVector / np.linalg.norm(normalVector)
                        #So for readability purposes, it would be better for this to read:
                            #relativeVelocity = MainCircleVelocityMatrix - SecondaryCircle Velocity Matrix
                            #projection = np.dot(relativeVelocity, normalVector)
                        #But this is more optimized
                        #The projection is the amount of the forced in the normal direction (so we ignore forces tangent to the collision)
                        projection = np.dot(MainCircleVelocityMatrix - SecondaryCircleVelocityMatrix, normalVector)
                        
                        #Because the projection already takes into account both circles velocities we dont need to call them again
                        #We re-multiply the project by the normal vector because the projection is a scalar value not a matrix
                        #We need to it be a matrix to do matrix addition/subtraction
                        #Multiplying it by the normal breaks its value down into an x and y that we can work with
                        #if we defined relative velocity as SecondaryCircleVelocityMatrix - MainCircleVelocityMatrix we would have the + sign in the first line and the - sign in the second
                        NewMainCircleVelocityMatrix = MainCircleVelocityMatrix - (projection * normalVector)
                        NewSecondaryCircleVelocityMatrix = SecondaryCircleVelocityMatrix + (projection * normalVector)

                        #Updates the circles with the new velocity matrixes we just made them
                        Circle.updateVelo(QCircle, NewXV=NewMainCircleVelocityMatrix[0], NewYV=NewMainCircleVelocityMatrix[1])
                        Circle.updateVelo(BCircle, NewXV=NewSecondaryCircleVelocityMatrix[0], NewYV=NewSecondaryCircleVelocityMatrix[1])
                        MainCircleVelocityMatrix = NewMainCircleVelocityMatrix #So that it is proper for the next collision

                        #Here we also have to separate overlapped circles
                        #First we figure out how much they overlap by, then we push the main circle away
                        #The proper way to do this is to push both away ~50% of the distance, but I was too lazy
                        overlap = MainCircleR+SecondaryCircleR - np.sqrt(((MainCircleX-SecondaryCircleX)**2) + ((MainCircleY-SecondaryCircleY)**2))
                        MainCircleX += normalVector[0] * overlap
                        MainCircleY += normalVector[1] * overlap
                        #Updates the circles with the new positions
                        Circle.updatePos(QCircle, NewX=MainCircleX, NewY=MainCircleY)
                        MainCircleMatrix = np.array([MainCircleX, MainCircleY])

def runCirlcesOnWallCollision():
    global circlesList
    #We iterate through each circle to see if it is colliding with any wall
    for WCircle in circlesList:
        #Defining Variable here
        WCirclePositionMatrix = np.array([Circle.getX(WCircle), Circle.getY(WCircle)])
        for AWall in wallsList:
            #We are gonna basically rotate the circle's center so its on a plane where the wall's rectangular body is align with the axis
            #At first I thought this was gonna be too taxxing to do
            #But if we just do all this math when we initialize the wall we don't need to do it again!!!
            wallRelativePosition = Wall.getWallRelativePos(AWall)
            wallStartPos = Wall.getStartMatrix(AWall)
            #Here we have to start doing math for every wall but still nothing heavy
            relativeCircleCoord = WCirclePositionMatrix - wallStartPos
            distanceAlongWall = np.dot(relativeCircleCoord, wallRelativePosition)
            distanceAlongWall = distanceAlongWall / np.dot(wallRelativePosition, wallRelativePosition)
            distanceAlongWall = np.clip(distanceAlongWall, 0.0, 1.0)
            closestPointToCircle = wallStartPos + (distanceAlongWall * wallRelativePosition)
            shortestDistanceToWall = np.linalg.norm(WCirclePositionMatrix - closestPointToCircle)
            #Now we check if the distance is less than the radius plus half the width of the wall
            if shortestDistanceToWall < ((Wall.getWidth(AWall)/2) + Circle.getRadius(WCircle)):
                #Now we just reflect the balls
                #First we gotta set more variables, including a special case where the circle is on the line and causes a divide by 0
                if shortestDistanceToWall == 0:
                    normal = Wall.getWallNormal(AWall)
                else:
                    #this happens the majority of the time
                    #The normal is the normal vector of the wall towards the circle
                    normal = (WCirclePositionMatrix - closestPointToCircle) / shortestDistanceToWall
                #The penetration is how deep the circle goes into the wall
                penetration = (Wall.getWidth(AWall)/2 +Circle.getRadius(WCircle)) - shortestDistanceToWall

                #Now we push the circle out of the wall by the penetration amount
                WCirclePositionMatrix += normal * penetration
                Circle.updatePos(WCircle, NewX= WCirclePositionMatrix[0], NewY = WCirclePositionMatrix[1])

                #Now we reflect Velocity
                WCircleVelocityMatrix = np.array([Circle.getXV(WCircle), Circle.getYV(WCircle)])
                WCircleVelocityMatrix = WCircleVelocityMatrix - 2 * np.dot(WCircleVelocityMatrix, normal) * normal
                if np.dot(WCircleVelocityMatrix, normal) > 0:
                    Circle.updateVelo(WCircle, NewXV=WCircleVelocityMatrix[0], NewYV=WCircleVelocityMatrix[1])

def runCirclesOnBorderCollision():
    #This first step is reflecting the velocity if the edge of the circle is outside of the border
    global borderWidth, borderHeight
    for CCircle in circlesList:
        if Circle.getX(CCircle) + Circle.getRadius(CCircle) > borderWidth/2:
            Circle.updateVelo(CCircle, NewXV=Circle.getXV(CCircle)*-1)
        if Circle.getX(CCircle) - Circle.getRadius(CCircle) < -1*borderWidth/2:
            Circle.updateVelo(CCircle, NewXV=Circle.getXV(CCircle)*-1)
        if Circle.getY(CCircle) - Circle.getRadius(CCircle) < -1*borderHeight/2:
            Circle.updateVelo(CCircle, NewYV=Circle.getYV(CCircle)*-1)
        if Circle.getY(CCircle) + Circle.getRadius(CCircle) > 1*borderHeight/2:
            Circle.updateVelo(CCircle, NewYV=Circle.getYV(CCircle)*-1)

    #Now we gotta correct ones still outside of the border due to errors
    #This teleports ones too far out back in, but also handles ones that would have collided mid frame
    #This is handled by effectively dragging them back to where they intersected the border and moving the percent left in the frame
    #But instead of doing that slow logic, we just reflect them because its the same result and faster
    for CCircle in circlesList:
        if Circle.getX(CCircle) + Circle.getRadius(CCircle) > borderWidth/2:
            if Circle.getX(CCircle) + Circle.getRadius(CCircle) > borderWidth:
                Circle.updatePos(CCircle, NewX=((borderWidth/2) - Circle.getRadius(CCircle)))
            else:
                Circle.updatePos(CCircle, NewX=(((borderWidth/2) - Circle.getRadius(CCircle)) - (Circle.getX(CCircle) + Circle.getRadius(CCircle) - borderWidth/2)))
        if Circle.getX(CCircle) - Circle.getRadius(CCircle) < -1*borderWidth/2:
            if Circle.getX(CCircle) - Circle.getRadius(CCircle) < -1*borderWidth:
                Circle.updatePos(CCircle, NewX=((borderWidth/-2) + Circle.getRadius(CCircle)))
            else:
                Circle.updatePos(CCircle, NewX=(((borderWidth/-2) + Circle.getRadius(CCircle)) - (Circle.getX(CCircle) - Circle.getRadius(CCircle) + borderWidth/2)))
        if Circle.getY(CCircle) - Circle.getRadius(CCircle) < -1*borderHeight/2:
            if Circle.getY(CCircle) - Circle.getRadius(CCircle) < -1*borderHeight:
                Circle.updatePos(CCircle, NewY=((borderHeight/-2) + Circle.getRadius(CCircle)))
            else:
                Circle.updatePos(CCircle, NewY=(((borderHeight/-2) + Circle.getRadius(CCircle)) - (Circle.getY(CCircle) - Circle.getRadius(CCircle) + borderHeight/2)))
        if Circle.getY(CCircle) + Circle.getRadius(CCircle) > 1*borderHeight/2:
            if Circle.getY(CCircle) + Circle.getRadius(CCircle) > borderHeight:
                Circle.updatePos(CCircle, NewY=((borderHeight/2) - Circle.getRadius(CCircle)))
            else:
                Circle.updatePos(CCircle, NewY=(((borderHeight/2) - Circle.getRadius(CCircle)) - (Circle.getY(CCircle) + Circle.getRadius(CCircle) - borderHeight/2)))

def updateCircles():
    #Running Circle on Circle Collision, this reflects the velocity along the tangent of the collision
    #This also nudges the circles apart if they are overlapping
    runCirclesOnCirclesCollision()
    #Running Circle on Border Collision
    #Reflects circle off of border
    #Teleports circle back into the border if it is outside of it
    #Accurately handles mid frame collisions
    runCirclesOnBorderCollision()
    #Now we collide the circles with the wall class i just made
    runCirlcesOnWallCollision()
    #Now we finally actually move the circles
    #This is self explanatory
    for PCircle in circlesList:
        Circle.updatePos(PCircle, NewX=Circle.getX(PCircle)+Circle.getXV(PCircle), NewY=Circle.getY(PCircle)+Circle.getYV(PCircle))
    
def CalcTotalVelo():
    #Just calculates the total momentum, I know it says velocity but I don't want to change the name of the function
    #Just used for the text display
    global circlesList
    TotalVelo = 0
    for I in circlesList:
        TotalVelo += Circle.getXV(I)**2 + Circle.getYV(I)**2
    TotalVelo = np.round(TotalVelo)
    return(str(TotalVelo))

def getCircleTouchingMouse(mouseX, mouseY, cameraX, cameraY, zoomFactor):
    #This is used for selecting circles
    #Returns the mouse earliest in the list (furthest back in the z order)
    #Returns None if no circle is being touched
    global circlesList
    for ACircle in circlesList:
        CircleScreenX, CircleScreenY = getScreenCoordinates(Circle.getX(ACircle), Circle.getY(ACircle), cameraX, cameraY, zoomFactor)
        if ((mouseX - CircleScreenX)**2 + (mouseY - CircleScreenY)**2) < (Circle.getRadius(ACircle)*zoomFactor)**2:
            return ACircle
    return None

def getCircleByUID(UID):
    #This function will return the circle with the given UID, or None if no such circle exists
    #The UID is for uniquely identifying circles, and is assigned when the circle is created
    global circlesList
    for ACircle in circlesList:
        if Circle.getUID(ACircle) == UID:
            return ACircle
    return None