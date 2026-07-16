import SimpleCircleVis as SCV

def enthalpy(particles, vertices):
    '''
    region is a polygon where enthalpy is stored and the change over a timestep is output.
    vertices, list, are in order of lines ex, [v1,v2,v3,v4] would be a rectangle.
    '''
    inside_particles=[]
    outside_particles=[]

    for point in particles:
        if inside(SCV.point.xPosistion, vertices):
            inside_particles.append(point)
        else:
            outside_particles.append(point)

    total_inside_velo=0
    for p in inside_particles:
        total_inside_velo+= SCV.p.xVelocity + SCV.p.yVelocity
    print(total_inside_velo)




def right_ray_trace(point,v1,v2):

    contact = False
    a,b=point

    x1, y1 = v1

    x2, y2 = v2

    if (y1<=b)!=(y2<=b):
        if (y2-y1==0):
            if (b==y1):
                return True
            else:
                return False
        else:
            x=(x2-x1)/(y2-y1)*(b-y2)+x2
            if a<x:
                return True

    return False


def inside(point, vertices):
    in_shape=False
    for v, vertice in enumerate(vertices):
        passthrough = right_ray_trace(point, vertice, vertices[(v+1)%len(vertices)])
        if passthrough:
            in_shape=not in_shape
    return in_shape


