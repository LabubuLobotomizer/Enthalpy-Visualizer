

import pygame as pg
import numpy as np
import random as sixseven

#change
# region
pg.init()
clock = pg.time.Clock()

WIDTH=1280
HEIGHT=720

screen=pg.display.set_mode((WIDTH, HEIGHT))
static_grid=pg.Surface((WIDTH, HEIGHT))  #grid so no redraws needed for faster compute (no zoom)
background=pg.Surface((WIDTH,HEIGHT))
# endregion
#region Grid
#drawing grid 12 across width with squares
def draw_grid(lines, Width):
    square_length = Width / lines
    for n in range(1,lines):
        pg.draw.line(static_grid,'grey', (n*square_length,0), (n * square_length, HEIGHT), 1)
        pg.draw.line(static_grid, 'grey', (0, 1*square_length*n), (Width, 1*square_length*n), 1)
draw_grid(40, WIDTH)  #note this means 12 total lines across width

background.blit(static_grid,(0,0))

#endregion grid complete

class Wall:
    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.rect = pg.Rect(x, y, width, height)
        self.left=self.x
        self.right=self.x+self.width
        self.top=self.y
        self.bottom=self.y+self.height
        if self.width<=self.height:
            self.type='vertical'
        elif self.width>self.height:
            self.type='horizontal'
        else:
            raise Warning('invalid wall type')

    def draw_back(self):
        pg.draw.rect(background,'salmon',self.rect  )
    def collide(self,particle):
        if self.type=='vertical':

            Right_collision = (particle.radius + particle.newx >= self.left) and (
                        particle.radius + particle.xPosition <= self.left)
            Left_collision = (-particle.radius + particle.newx <= self.right) and (
                    -particle.radius + particle.xPosition >= self.right)
            Y_bounds = (particle.yPosition>=self.top) and (particle.yPosition<=self.bottom)
            if Right_collision or Left_collision:
                if Y_bounds:
                    particle.xVelocity=-particle.xVelocity
                    particle.newx = particle.xPosition + particle.xVelocity
                    # print('collision', particle.xPosition, particle.xVelocity)
                    return True
        else:
            Top_collision = (-particle.radius + particle.newy <=self.bottom) and (
                    -particle.radius + particle.yPosition >= self.bottom)
            Bottom_collision = (particle.radius + particle.newy >= self.top) and (
                        particle.radius + particle.yPosition <= self.top)
            X_bounds = (particle.xPosition >= self.left) and (particle.xPosition <= self.right)
            if Top_collision or Bottom_collision:
                if X_bounds:
                    particle.yVelocity=-particle.yVelocity
                    particle.newy = particle.yPosition + particle.yVelocity
                    # print('collision', particle.xPosition, particle.xVelocity)
                    return True
        return False

def collide_test(particle, wall):
    '''
    True if collision occurs, else False
    '''
    if wall.type == 'vertical':

        Right_collision = (particle.radius + particle.newx >= wall.left) and (
                particle.radius + particle.xPosition <= wall.left)
        Left_collision = (-particle.radius + particle.newx <= wall.right) and (
                -particle.radius + particle.xPosition >= wall.right)
        Y_bounds = (particle.yPosition >= wall.top) and (particle.yPosition <= wall.bottom)
        if Right_collision or Left_collision:
            if Y_bounds:
                return True
    else:
        Top_collision = (-particle.radius + particle.newy <= wall.bottom) and (
                -particle.radius + particle.yPosition >= wall.bottom)
        Bottom_collision = (particle.radius + particle.newy >= wall.top) and (
                particle.radius + particle.yPosition <= wall.top)
        X_bounds = (particle.xPosition >= wall.left) and (particle.xPosition <= wall.right)
        if Top_collision or Bottom_collision:
            if X_bounds:
                return True
    return False

def type_coll(wall):
    '''
    assumes collision occurs,
    returns True if the collision is on a vert wall, False if not
    '''
    if wall.type=='vertical':
        return True
    else:
        return False

def LR_side_of_collision(wall, particle):
    '''
    Assumes collision is vertical
    Returns True if collision was on right, False if left
    '''
    Right_collision = (particle.radius + particle.newx >= wall.left) and (
            particle.radius + particle.xPosition <= wall.left)
    if Right_collision:
        return True
    else:
        return False

def TB_side_of_collision(wall, particle):
    '''
        Assumes collision is horizontal
        Returns True if collision was on bottom, False if top
        '''
    Bottom_collision = (particle.radius + particle.newy >= wall.top) and (
            particle.radius + particle.yPosition <= wall.top)
    if Bottom_collision:
        return True
    else:
        return False

def ref_col(walls, particle):
    '''alters new x and y values to account for distance between particle and wall
    recursively calculates until no distance is left, should work to arbitrarily high numbers
    '''

    for wall in walls:
        if collide_test(particle,wall):
            if type_coll==True:    #True means vert wall collision
                if LR_side_of_collision(wall, particle):  #True means right
                    ref_x= -abs(wall.left-particle.newx)+wall.left  #projecting
                    particle.xVelocity=-particle.xVelocity

                else:
                    ref_x = abs(wall.right - particle.newx) + wall.right
                    particle.xVelocity = -particle.xVelocity
                particle.newx = ref_x
            else:
                if TB_side_of_collision(wall, particle):    #True=bottom
                    ref_y = -abs(wall.top - particle.newy) + wall.top  # projecting
                    particle.yVelocity = -particle.yVelocity
                else:
                    ref_y = abs(wall.bottom - particle.newy) + wall.bottom  # projecting
                    particle.yVelocity = -particle.yVelocity
                particle.newy = ref_y

            ref_col(walls,particle)


def col(walls, particles):
    ''' updates once after collisions whether they occurred or not'''
    for particle in particles:
        ref_col(walls, particle)
        particle.xPosition = particle.newx
        particle.yPosition = particle.newy
        particle.newx = particle.xPosition + particle.xVelocity
        particle.newy = particle.yPosition + particle.yVelocity



class Particle():
    def __init__(self, X_Pos, Y_Pos, Circle_Color, Radius, X_Velo, Y_Velo):
        self.xPosition = X_Pos
        self.yPosition = Y_Pos
        self.xVelocity = X_Velo
        self.yVelocity = Y_Velo
        self.radius = Radius
        self.color = Circle_Color
        self.newx=self.xPosition+self.xVelocity
        self.newy=self.yPosition+self.yVelocity

    def updatePos(self, timestep=1):
        self.xPosition+=self.xVelocity*timestep
        self.yPosition+=self.yVelocity*timestep
        self.newx = self.xPosition + self.xVelocity
        self.newy = self.yPosition + self.yVelocity
    def draw(self):

        pg.draw.circle(screen,'white',(self.xPosition,self.yPosition),self.radius)
    def collide(self, other):
        # Now we have to do that complicated ish math, For now everything is perfectly elastic #stealing ur code. This is not rotation though, Dot product between relative velocity of main and normal vector finds the magnitude transferred. Multiply the magnitude transferred by the normalized vector to get the effect in both directions.
        MainCircleMatrix = np.array([self.xPosition, self.yPosition])
        MainCircleVelocityMatrix = np.array([self.xVelocity, self.yVelocity])   #also why are we calling these matrices bruddah/ *crying emoji*/
        SecondaryCircleMatrix = np.array([other.xPosition, other.yPosition])
        SecondaryCircleVelocityMatrix = np.array([other.xVelocity, other.yVelocity])
        normalVector = (MainCircleMatrix - SecondaryCircleMatrix)  # Getting difference between them
        relative_velocity= MainCircleVelocityMatrix-SecondaryCircleVelocityMatrix
        normalized_Vector = normalVector / np.linalg.norm(normalVector)  # Converting it to normal vector
        # Some like math thing about rotating the interaction to be 90* hit not the actual angle of contact
        projection = np.dot(relative_velocity, normalized_Vector)
        velocity_transferred=projection*normalized_Vector
        NewMainCircleVelocityMatrix = MainCircleVelocityMatrix - velocity_transferred
        NewSecondaryCircleVelocityMatrix = SecondaryCircleVelocityMatrix + velocity_transferred
        self.xVelocity, self.yVelocity = NewMainCircleVelocityMatrix
        other.xVelocity, other.yVelocity = NewSecondaryCircleVelocityMatrix
    def display(self):
        print(self.xPosition, self.yPosition, self.xVelocity, self.yVelocity)
def particle_collisions_full(Particles, Walls):
    '''
    particles are a list of all particles and walls are well a list of all walls. This is assumed(supposed to put assumptions and things the function does in docstring but lwk don't need allat for now.
    '''
    indie=1
    total_num_particles=len(Particles)
    for circle in Particles:
        for second_circle in Particles[indie:total_num_particles]:

            dist_squared=(circle.xPosition-second_circle.xPosition)**2+(circle.yPosition-second_circle.yPosition)**2
            if dist_squared < (circle.radius+second_circle.radius)**2:     #notice, this avoids sqrt, which is computationally expensive MIT OCW LOLOLOL
                circle.collide(second_circle)
        indie+=1

    for p in Particles:


        recursive_wall_collider(p,walls)

def recursive_wall_collider(p,temp_walls):
    ''' takes in one particle and list of walls, calculates all collisions with walls for that particle'''


    for wall in temp_walls:
        wall_collision = wall.collide(p)

        if wall_collision==True:

            recursive_wall_collider(p,temp_walls)
            break

def grid_collision_checker(Particles, parameterx, parametery, width, height):  #something like a sweep or a grid checker would make collisions less expensive to compute, we will do together.
     pass

#region Wall Setup
wall_width=10

right_wall=Wall(WIDTH - wall_width, 0, wall_width, HEIGHT)
left_wall=Wall(0, 0, wall_width, HEIGHT)
bottom_wall=Wall(0, HEIGHT - wall_width, WIDTH, wall_width)
top_wall=Wall(0, 0, WIDTH, wall_width)
system_left=Wall((WIDTH*1/3),(HEIGHT/4), wall_width/2, HEIGHT/2)
system_right=Wall((WIDTH*2/3),(HEIGHT/4), wall_width/2, HEIGHT/2)
system_bottom=Wall((WIDTH*1/3),(HEIGHT*3/4)-wall_width/2, WIDTH/3+wall_width/4, wall_width/2)

walls = [
    top_wall,
    right_wall,
    left_wall,
    bottom_wall,
    # system_right,
    # system_left,
    # system_bottom
]


for thing in walls:
    thing.draw_back()
#endregion

#region particle setup
particles=[]



#endregion

pg.display.flip()
running=True
while running:
    clock.tick(5)
    screen.blit(background, (0,0))
# region
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                p=pg.mouse.get_pos()
                # particles.append(Particle(p[0], p[1], 'White', sixseven.randint(5,10), sixseven.randint(-5,1000), sixseven.randint(-5,5)))
                particles.append(Particle(p[0], p[1], 'White', 20, 10,0))
# endregion
#     particle_collisions_full(particles, walls)
    col(walls, particles)
    for thing in particles:
        thing.draw()
        # thing.display()


    pg.display.flip()

