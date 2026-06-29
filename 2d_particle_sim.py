import pygame as pg
pg.init()
width=1200
height=800
Clock=pg.time.Clock()
dt=1
radius=height/15

screen=pg.display.set_mode((width,height))
pg.display.set_caption('676767676767676776766767767676776')
screen.fill('purple')
pg.draw.line(screen,'black',(0,height/2),(width,height/2))

class particle():
    def __init__(self, velocity, position):
        self.v=velocity
        self.p=position
    def get_v(self):
        return self.v
    def get_p(self):
        return self.p
    def update(self, v, p):
        self.v=v
        self.p=p
    def collide(self, other):
        (self.v,other.v)=(other.v,self.v)
running=True
FirstParticleFlyer=particle(2,width/3)
SecondParticle=particle(4, width*(2/3))

while running:

    p= FirstParticleFlyer.get_p()  #p1
    v= FirstParticleFlyer.get_v()
    if (p+radius)>=width or (p-radius)<=0:
        FirstParticleFlyer.update(-v,p)
    new_p=FirstParticleFlyer.get_p()+dt*FirstParticleFlyer.get_v()
    FirstParticleFlyer.update(FirstParticleFlyer.get_v(),new_p)

    temp_velo = SecondParticle.get_v()
    temp_pos = SecondParticle.get_p()
    if (temp_pos + radius) >= width or (temp_pos - radius) <= 0: #p2
        SecondParticle.update(-temp_velo, temp_pos)
    new_p2 = SecondParticle.get_p() + dt * SecondParticle.get_v()
    SecondParticle.update(SecondParticle.get_v(), new_p2)

    dist=abs(FirstParticleFlyer.get_p()-SecondParticle.get_p())-radius*2
    if dist<=0:
        FirstParticleFlyer.collide(SecondParticle)



    screen.fill('purple')
    pg.draw.line(screen, 'black', (0, height / 2), (width, height / 2))
    pg.draw.circle(screen,'black', (FirstParticleFlyer.get_p(),height/2),radius)
    pg.draw.circle(screen, 'black', (SecondParticle.get_p(), height / 2), radius)
    pg.draw.line(screen,'white', (FirstParticleFlyer.get_p(), height/2),
                 ((FirstParticleFlyer.get_p()+FirstParticleFlyer.get_v()*radius*dt), (height/2)))
    pg.draw.line(screen, 'white', (SecondParticle.get_p(), height / 2),
                 ((SecondParticle.get_p() + SecondParticle.get_v() * radius * dt), (height / 2)))
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    Clock.tick(60)
