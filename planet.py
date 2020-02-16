from vpython import sphere, vector, color, rotate,textures
import random
import math

G = 6.667e-11#гравитационная постоянная 
#!можно хранить sphere в классе и переписать класс All_planet(так вроде лучше)
class Planet:
    def __init__(self,name,radius,distance,mass_planet,mass2,texture):#?-mass2 масса планеты,вокруг которой происходит вращение
        self.name=name
        self.radius=radius#радисус планеты
        self.distance=distance#дистанция до планеты,вокруг которой происходит вращение
        self.mass_planet=mass_planet#масса планеты
        self.mass2=mass2#масса планеты,вокруг которой происходит вращение
        self.satellites=[]#список спутников
        self.pos=vector(0,0,0)#позиция объекта по отношению к объекту вращения,т.е. чтобы получить позицию на экране,надо прибавить позицию планеты вращения
        self.texture=texture#хранит текущую текстуру 
        if(distance!=0):
            self.force=(G*mass_planet*mass2)/(distance**2)#гравитационная сила между планетами
            self.angular_velocity=math.sqrt(self.force/(mass_planet*distance))

    def spawn_satellites(self,total,radius=0,distance=0,mass_planet=0,texture={'file':textures.rough}):
        for i in range(total):
            if(radius==0):
                r=self.radius/6
            c=0.01
            if(distance==0):
                d=self.distance*c+(i*10)*1e6
            if(mass_planet==0):
                m=self.mass_planet*c
            self.satellites.append(Planet(i,r,d,m,self.mass_planet,texture))

    def set_pos(self):
        self.pos=rotate(self.pos,angle=self.angular_velocity,axis=vector(0,0,1))

    def get_pos(self):
        return self.pos


class All_planet():
    def __init__(self):
        self.planets=[]#список всех планет
        self.sphere_planets=[]#список всех сфер
        self.sphere_satellites=[]#список всех сфер спутников,если их нет,то пустой список, подсписки равны по длинне Planet.satellites
        """ длинна всех трех списков должна быть одинаковой """


    def create(self):#создает все планеты
        for planet in self.planets:
            show_planet=sphere(pos=vector(planet.distance,0,0),radius=planet.radius,texture=planet.texture,shininess=0,make_trail=True)
            planet.pos=show_planet.pos
            self.sphere_planets.append(show_planet)
    
    def create_satellites(self):#создает все спутники
        for planet in self.planets:
            sphere_satelite=[]
            for satellite in planet.satellites:
                show_planet=sphere(pos=vector(satellite.distance+planet.radius,0,0),radius=satellite.radius,texture=satellite.texture,shininess=0)#?возможно тут два радиуса 
                satellite.pos=show_planet.pos
                sphere_satelite.append(show_planet)
            else:
                self.sphere_satellites.append(sphere_satelite)
    
    def scale_up(self,h):#увеличививаем радиус,Уменьшаем дистанцию 
        for planet in self.planets:
            if(planet.mass2==0):
                planet.radius=planet.radius*(h/10)
                continue
            planet.radius=planet.radius*h
            planet.distance=planet.distance/h
            for satellite in planet.satellites:  
                if(planet.mass2==0):
                    continue
                satellite.radius=satellite.radius*h
                satellite.distance=satellite.distance/h

    def speed_up(self,speed):#увеличиваем угловую скорость планет
        for planet in self.planets:
            if(planet.mass2==0):
                continue
            planet.angular_velocity=planet.angular_velocity*speed
            for satellite in planet.satellites:
                satellite.angular_velocity=planet.angular_velocity*speed

    def update_position(self):#обновляет позицию всех планет
        for i in range(0,len(self.planets)):
            if(self.planets[i].mass2==0):
                continue
            self.sphere_planets[i].pos=rotate(self.sphere_planets[i].pos,angle=self.planets[i].angular_velocity,axis=vector(0,0,1))
            self.sphere_planets[i].rotate(angle=self.planets[i].angular_velocity,axis=vector(0,1,0),origin= self.sphere_planets[i].pos)#вращение вокруг своей оси
            self.planets[i].set_pos()

    def update_position_satellites(self):#обновляет позицию всех спутников всех планет 
        for i in range(0,len(self.sphere_satellites)):
            for j in range(0,len(self.sphere_satellites[i])):
                self.planets[i].satellites[j].set_pos()
                self.sphere_satellites[i][j].pos=self.planets[i].satellites[j].pos+self.planets[i].pos

    def uravn(self):
        i=0
        for planet in self.planets:
            planet.radius=3
            planet.distance=i
            for satellite in planet.satellites:
                j=0 
                satellite.radius=planet.radius/10
                satellite.distance=1+j
                j+=0.1
            i+=10
