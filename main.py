from vpython import sphere, vector, color, rotate,scene,textures,canvas,local_light,distant_light,box,ring,label

import math
import planet
from ctypes  import *


""" 1)Вращение планет вокруг себя -- вроде работает (надо расчитать другую скорость)
    2)Кольца Сатурну saturn=ring(pos=vector(0,0,0),axis=vector(0,1,0),radius=2,texture=('2k_saturn_ring_alpha.png')) -- вроде есть
    3)кнопки ебаные (не надо,будут события клавиатуры,нажатия клавиш) -- работает 
    4)добавить фон сцене- работает костыльно
    5)придумать что то с масштабом 
    6)свет от солнца -- работает
    7)можно чёто придумтаь со светом,тк если горит солнечный ,то звезды в background+scene гаснут -- ну гаснут и гаснут 
    8)придумать что то с разрешением сцены -- хз как 
    9)пофиксить справку(или нет) -- справка норм
    10) какое то черное пространство по центру сферы внутри"""

def ring_for_saturn(saturn):#еще костыли для колец сатурна
    rings_saturn=[]
    #ring_saturn1=ring(pos=saturn.pos,axis=vector(-0.25,1,0),radius=saturn.radius*1,texture=('2k_saturn_ring_alpha.png'),shininess=0,thickness=saturn.radius/20)
    ring_saturn2=ring(pos=saturn.pos,axis=vector(-0.25,1,0),radius=saturn.radius*0.9,texture=('2k_saturn_ring_alpha.png'),shininess=0,thickness=saturn.radius/20)
    ring_saturn3=ring(pos=saturn.pos,axis=vector(-0.25,1,0),radius=saturn.radius*0.8,texture=('2k_saturn_ring_alpha.png'),shininess=0,thickness=saturn.radius/20)
    ring_saturn4=ring(pos=saturn.pos,axis=vector(-0.25,1,0),radius=saturn.radius*0.7,texture=('2k_saturn_ring_alpha.png'),shininess=0,thickness=saturn.radius/20)
    #rings_saturn.append(ring_saturn1)
    rings_saturn.append(ring_saturn2)
    rings_saturn.append(ring_saturn3)
    rings_saturn.append(ring_saturn4)
    return rings_saturn

def update_pos_ring_saturn(saturn,rings_saturn):#кольца следуют за Сатурном
    i=10
    for ring in rings_saturn:
        ring.pos=saturn.pos
        ring.rotate(angle=saturn.angular_velocity*i,axis=vector(-0.25,1,0),origin= ring.pos)#вращение колец вокруг оси
        i+=10

def scene_light(scene,sun_light):#включаем весь свет,выключаем солнечный
    scene.lights[0].visible=True
    scene.lights[1].visible=True
    sun_light.visible=False
    
def light_from_sun(scene,planet,sun_light):#свет только от солнца #?не видно задний фон
    scene.lights[0].visible=False
    scene.lights[1].visible=False
    planet.sphere.emissive=True#подсвечивание сферы солнца не убираем
    sun_light.visible=True

def all_light(scene,sun_light):#включаем весь свет,выключаем солнечный
    scene.lights[0].visible=True
    scene.lights[1].visible=True
    sun_light.visible=True

def trail_off_on(scene,planet):
    for satellite in planet.satellites:
        if(satellite.sphere.make_trail):
            satellite.sphere.clear_trail()
            satellite.sphere.make_trail=False
        else:
            satellite.sphere.make_trail=True
        if(len(satellite.satellites)!=0):
            trail_off_on(scene,satellite)

def create_background_scene(scene,w):#создаем фон у планет из звезд,можно только костыльно
    
    s=1000
    background_scene=sphere(pos=vector(0,0,0),size=vector(w*s,w*s,w*s),shininess=0,texture='2k_stars.jpg',opacity=1)#создаем сферу по центру с текстурами звезд
    scene.camera.axis=vector(0,0,-w/(0.00001*s))
    scene.camera.pos=vector(0,0,w/(0.00001*s))
    print(scene.camera.axis)
    print(scene.camera.pos)

    return background_scene

def create_info():
    text1='''
            Клавиши 1,2,3 - управление светом\n
            Клавиша 4 - убрать/добавить след от планет\n
            Клавиша 5 - поставить/снять паузу\n
            Клавиша 6 - открыть/закрыть справку\n
            Клавиши up/down - увеличить/уменьшить скорость вращения планет\n
            Клавиша shift+левая кнопка - \n
            Правая кнопка мыши - \n
            Вращение колесика - увеличение/уменьшение масштаба\n
        '''
    l1=label( pos=vector(0,0,0), text=text1,align='center',box=False)
    l1.visible=False
    return l1

def pause(move):#ставим движение на паузу
    if(move):
        return False
    else:
        return True

def main():
    move=True#продолжаем обновление движения,пока тру
    w=windll.user32.GetSystemMetrics(0)#получаем размеры окна
    h=windll.user32.GetSystemMetrics(1)#
    
    s=50
    speed=-200#! макс значение 200 если отрицательное-по часовой,положительное-против часовой

    scene=canvas(width=w,height=h,center=vector(0,0,0))#создаем сцену по размерам окна
    label_info=create_info()#создаем метку со справкой

    scene.visible=False#пока ничего не показываем,ждем создания объектов

    sun_light=local_light(pos=vector(0,0,0),color=color.white)#устанавливаем локальный свет в позиции 0 0 0 для солнца
    sun_light.visible=False

    def key_up(event):
        k=event.key
        nonlocal move
        if(k=='1'):
            light_from_sun(scene,sun,sun_light)#свет только от солнца
        elif(k=='2'):
            scene_light(scene,sun)#свет только сцены
        elif(k=='3'):
            all_light(scene,sun)#весь свет
        elif(k=='4'):#убираем/возвращаем след
            trail_off_on(scene,sun)
        elif(k=='5'):#ставим на паузу
            move=pause(move)
        elif(k=='6'):#показываем справку,очень костыльно,потом пофиксить(или нет)
            if(label_info.visible):
                label_info.visible=False
            else:
                label_info.visible=True
        
    def key_down(event):
        k=event.key
        nonlocal move
        nonlocal speed
        if(k=='down'):
            move=False
            draw_planet.speed_up(sun,1/speed)
            speed+=10
            if(speed==0):
                speed-=1
            draw_planet.speed_up(sun,speed)
            move=True
        elif(k=='up'):
            move=False
            draw_planet.speed_up(sun,1/speed)
            speed-=10
            draw_planet.speed_up(sun,speed)
            move=True

    scene.bind('keyup',key_up)
    scene.bind('keydown',key_down)

    sun=planet.SkyBody('sun',695.990e6,1.9885e30,texture=('2k_sun.jpg'))#создаем солнце

    sun.spawn_satellites(name='mercury',radius=2.439e6,distance=58e9,mass_planet=0.32868e24,texture=('2k_mercury.jpg'))#добавляем спутники солнцу
    sun.spawn_satellites(name='venus',radius=6.052e6,distance=108e9,mass_planet=4.81068e24,texture=('2k_venus.jpg'))
    sun.spawn_satellites(name='earth',radius=6.37822e6,distance=150e9,mass_planet=5.972e24,texture=('2k_earth.jpg'))
    sun.spawn_satellites(name='mars',radius=3.488e6,distance=228e9,mass_planet=0.63345e24,texture=('2k_mars.jpg'))
    sun.spawn_satellites(name='jupiter',radius=71.300e6,distance=778e9,mass_planet=1876.64328e24,texture=('2k_jupiter.jpg'))
    sun.spawn_satellites(name='saturn',radius=60.100e6,distance=1429e9,mass_planet=561.80376e24,texture=('2k_saturn.jpg'))
    sun.spawn_satellites(name='uranus',radius=26.500e6,distance=2875e9,mass_planet=86.05440e24,texture=('2k_uranus.jpg'))
    sun.spawn_satellites(name='neptune',radius=24.750e6,distance=4497e9,mass_planet=101.59200e24,texture=('2k_neptune.jpg'))
    
    sun.satellites[2].spawn_satellites(1,name='moon',radius=1737.1e3,distance=384.4e6,mass_planet=7.348e22,texture=('2k_moon.jpg'))#третьему спутнику солнца(земле) добавляем спутник луну
    
    background_scene=create_background_scene(scene,sun.radius)#создаем задний фон вокруг солнца

    draw_planet=planet.DrawSkyBody()#создаем класс драв планет и отрисовываем планету солнце
    
    #draw_planet.uravn(sun)

    sun.radius=sun.radius*(s/5)#делаем приближение для наглядности
    draw_planet.scale_up(sun,s)#делаем приближение для наглядности 
    
    draw_planet.draw_planet(sun)
    draw_planet.draw_satellites(sun)
    draw_planet.speed_up(sun,speed)

    rings_saturn=ring_for_saturn(sun)#создаем список из колец сатурна
    scene.visible=True#после создания всех объектов всё отображаем

    while True:#движение объектов
        while move:
            draw_planet.update_position(sun)
            update_pos_ring_saturn(sun.satellites[5],rings_saturn)#обновляем позицию колец Сатурна

if __name__=='__main__':
    main()