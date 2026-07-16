import pygame
import math
import numpy as np

#setting up the screen
Screen_Width = 1280
Screen_Height = 720
pygame.init()
window_size = (Screen_Width, Screen_Height)
screen = pygame.display.set_mode(window_size)
R = True

#list of the circles properties
Circles_X = [0, 1, 0, -0.5, 0]
Circles_Y = [0, -.5, -5.5, .75, 0] 
Circles_Z = [3, 2, 2, 1, 15] 
Circles_Size = [1.5, 0.5, 5, 0.25, 11]
Circles_color =[np.array([180, 20, 20]), np.array([20, 20, 180]), np.array([20, 180, 20]), np.array([150, 150, 150]), np.array([60, 30, 100])] #0-255
Circles_Brightness = [1, 1, 1, 1, 1] #0-1
Circles_Shininess = [.05, .05, .05, .2, .1] #0-1

Light_Source = [np.array([0, 2, 1])]
Ambient_Light = 0.1

#Fov in degress (YFov is based off of the ratio from height to width)
FOV = 90
YFOV = ((Screen_Height/Screen_Width) * FOV)

#Player(Camera) Position
Player_X = 0
Player_Y = 0
Player_Z = 0
Player_Rotation_XZ = 0
Player_Rotation_Y = 0

#Not currently in use, math for a matrix containing the players looking direction
#Player_Unit_Vector = np.array([math.sin(Player_Rotation_XZ) * math.cos(Player_Rotation_Y), math.sin(Player_Rotation_Y), math.cos(Player_Rotation_XZ) * math.cos(Player_Rotation_Y)])

#Quality of the render
Render_Distance = 5
Bounce_Limit = 5

#L is so the raytracing is only run once
L = True
#R handles quitting events
while R:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                R = False
    if (L):
        for i in range(1, Screen_Width, 1):
            #print(i)
            pygame.display.flip()
            Ajd_Dir_XZ = math.radians(Player_Rotation_XZ - (FOV/2) + (FOV * i / Screen_Width))
            for ii in range(1,Screen_Height, 1):
                #Ajd_Dir is the rotation in radians
                Ajd_Dir_Y = 0 - math.radians(Player_Rotation_Y - (YFOV/2) + (YFOV * ii / Screen_Height))

                #Defining Variables for the Vector
                VectorOrg = np.array([Player_X, Player_Y, Player_Z])
                Vector_Direction = np.array([math.sin(Ajd_Dir_XZ) * math.cos(Ajd_Dir_Y), math.sin(Ajd_Dir_Y), math.cos(Ajd_Dir_XZ) * math.cos(Ajd_Dir_Y)])
                Vector_Color = np.array([0, 0, 0])

            
                Bounces = 0
                Prev_Circle_Shininess = 1
                Total_Distance = 0

                #Check until bounces
                while(Bounces<=Bounce_Limit):

                    Closest_Intersection = 100000
                    Closest_Circle = -1
                    
                    
                    #iterate across all the spheres
                    for Circle_Number in range(0, len(Circles_Size), 1):
                        c_Center = np.array([Circles_X[Circle_Number], Circles_Y[Circle_Number], Circles_Z[Circle_Number]])
                        c_Radius = Circles_Size[Circle_Number]

                        #finding the locations of intersections
                        M = VectorOrg - c_Center
                        b = np.dot(M, Vector_Direction)
                        c = np.dot(M, M) - c_Radius**2

                        Discriminant = b**2 - c
                        #preparing Variables
                        d1 = 0
                        d2 = 0
                        
                        #if Discriminant<0 than there are no intersections
                        if(Discriminant>=0):
                            d1 = -b - math.sqrt(Discriminant)
                            d2 = -b + math.sqrt(Discriminant)
                            if(d1>0 and d1<Closest_Intersection):
                                Closest_Intersection = d1
                                Closest_Circle = Circle_Number
                            if(d2>0 and d1!=d2 and d2<Closest_Intersection):
                                Closest_Intersection = d2
                                Closest_Circle = Circle_Number
                        
                    #Calculate Color and Reflection
                    if(Closest_Circle>-1):
                        Total_Distance += Closest_Intersection
                        Bounces += 1
                        VectorOrg = VectorOrg + (Closest_Intersection * Vector_Direction)
                        Closest_Circle_Position = np.array([Circles_X[Closest_Circle], Circles_Y[Closest_Circle], Circles_Z[Closest_Circle]])
                        Normal_Circle_Vector = (VectorOrg - Closest_Circle_Position) / Circles_Size[Closest_Circle]
                        Vector_Direction = Vector_Direction - (2 * np.dot(Vector_Direction, Normal_Circle_Vector) * Normal_Circle_Vector)
                        Light_Source_Direction = (Light_Source[0] - VectorOrg)
                        Light_Source_Magnitude = np.linalg.norm(Light_Source)
                        Light_Source_Direction = Light_Source_Direction / Light_Source_Magnitude
                        VectorOrg = VectorOrg + (Normal_Circle_Vector *0.0000001)
                        
                        #Calculate the Color
                        Vector_Color = Vector_Color + (Circles_color[Closest_Circle]*(1-Circles_Shininess[Closest_Circle])*Prev_Circle_Shininess*max(0, np.dot(Normal_Circle_Vector, Light_Source_Direction)))
                        Vector_Color = Vector_Color + Circles_color[Closest_Circle] * Ambient_Light
                        Prev_Circle_Shininess = Circles_Shininess[Closest_Circle]
                    else:
                        Bounces = 10000
                        
                    #print(Closest_Circle, Closest_Intersection)
                #print(Vector_Color[0], Vector_Color[1], Vector_Color[2])
                screen.set_at((i,ii), (min(Vector_Color[0], 255), min(Vector_Color[1], 255), min(Vector_Color[2], 255)))
                #pygame.display.flip()
#min(Circles_color[Closest_Circle][0]/(Closest_Intersection)*Circles_Brightness[Closest_Circle], 255), min(Circles_color[Closest_Circle][1]/(Closest_Intersection)*Circles_Brightness[Closest_Circle], 255), min(Circles_color[Closest_Circle][2]/(Closest_Intersection)*Circles_Brightness[Closest_Circle], 255)))
        pygame.display.flip()
        print("done")
        L = False

    pygame.display.flip() 


