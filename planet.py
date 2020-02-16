from vpython import sphere, vector, color, rotate,textures
import random
import math

G = 6.667e-11#гравитационная постоянная
class SkyBody:#класс тела,вокруг которого происходит вращение
    def __init__(self,name,radius,mass_planet,texture):
        self.name=name
        self.radius=radius#радисус планеты
        self.mass_planet=mass_planet#масса планеты
        self.texture=texture#хранит текущую текстуру
        
        self.satellites=[]#список спутников
        self.sphere=None#отображение сферы на экране
        self.pos=vector(0,0,0)#позиция объекта по отношению к объекту вращения,т.е. чтобы получить позицию на экране,надо прибавить позицию планеты вращения
    
    def spawn_satellites(self,name,radius,distance,mass_planet,texture={'file':textures.rough}):#создаем спутники класса Planet 
            d=distance
            n=name
            r=radius
            m=mass_planet
            self.satellites.append(Planet(n,r,m,texture,d,self.mass_planet))

class Planet(SkyBody):
    def __init__(self,name,radius,mass_planet,texture,distance,mass2):#?-mass2 масса планеты,вокруг которой происходит вращение
        self.name=name
        self.radius=radius#радисус планеты
        self.mass_planet=mass_planet#масса планеты
        self.texture=texture#хранит текущую текстуру
        self.distance=distance#дистанция до планеты,вокруг которой происходит вращение
        self.mass2=mass2#масса планеты,вокруг которой происходит вращение
        
        self.satellites=[]#список спутников
        self.sphere=None#отображение сферы на экране
        self.pos=vector(0,0,0)#позиция объекта по отношению к объекту вращения,т.е. чтобы получить позицию на экране,надо прибавить позицию планеты вращения
        self.force=(G*mass_planet*mass2)/(distance**2)#гравитационная сила между планетами
        self.angular_velocity=math.sqrt(self.force/(mass_planet*distance))


    def spawn_satellites(self,total,name='',radius=0,distance=0,mass_planet=0,texture={'file':textures.rough}):#создаем спутники класса Planet 
        for i in range(total):
            
            if(name==''):#? если передаем имя,то оно будет одинаково у всех спутников
                name=i
            else:
                n=name
            if(radius==0):
                r=self.radius/6
            else:
                r=radius
            c=0.01
            if(distance==0):
                d=self.distance*c+(i*10)*1e6
            else:
                d=distance
            if(mass_planet==0):
                m=self.mass_planet*c
            else:
                m=mass_planet
            self.satellites.append(Planet(n,r,m,texture,d,self.mass_planet))

    def change_pos(self):
        self.pos=rotate(self.pos,angle=self.angular_velocity,axis=vector(0,0,1))

    def get_pos(self):
        return self.pos

class DrawSkyBody():

    def uravn(self,planet):
        i=10
        for satellite in planet.satellites:
            satellite.radius=planet.radius/3
            satellite.distance=planet.radius+satellite.radius*i
            if(len(satellite.satellites)!=0):
                self.uravn(satellite)
            i+=10

    def scale_up(self,planet,s):#увеличививаем радиус,уменьшаем дистанцию
        for satellite in planet.satellites:
            satellite.radius=satellite.radius*s
            satellite.distance=satellite.distance/s
            if(len(satellite.satellites)!=0):
                self.scale_up(satellite,s)

    def draw_planet(self,planet):#рисуем планету
        planet.sphere=sphere(pos=vector(0,0,0),radius=planet.radius,texture=planet.texture,shininess=0)
        planet.pos=planet.sphere.pos

    def draw_satellites(self,planet):#создаем все спутники(вообще все)
        for satellite in planet.satellites:
            satellite.sphere=sphere(pos=vector(satellite.distance+planet.radius+satellite.radius,0,0),radius=satellite.radius,texture=satellite.texture,shininess=0,make_trail=False)#?возможно тут два радиуса
            satellite.pos=satellite.sphere.pos
            if(len(satellite.satellites)!=0):
                self.draw_satellites(satellite)

    def speed_up(self,planet,speed):#увеличиваем угловую скорость всех спутников
        for satellite in planet.satellites:
            satellite.angular_velocity=satellite.angular_velocity*speed
            if(len(satellite.satellites)!=0):
                self.speed_up(satellite,speed)
                
    def update_position(self,planet):#обновляет позицию всех спутников относительно планеты
        for satellite in planet.satellites:
            satellite.change_pos()
            satellite.sphere.pos=satellite.pos+planet.pos
            satellite.sphere.rotate(angle=satellite.angular_velocity,axis=vector(0,1,0),origin=satellite.sphere.pos)#вращение вокруг своей оси
            if(len(satellite.satellites)!=0):
                self.update_position(satellite)
