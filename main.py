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
    7)можно чёто придумтаь со светом,тк если горит солнечный ,то звезды в background гаснут -- ну гаснут и гаснут 
    8)придумать что то с разрешением сцены -- хз как 
    9)пофиксить справку(или нет) -- справка норм"""

def ring_for_saturn(solar_system):#еще костыли для колец сатурна
    rings_saturn=[]
    ring_saturn1=ring(pos=solar_system.planets[6].pos,axis=vector(-0.25,1,0),radius=solar_system.planets[6].radius*2,texture=('2k_saturn_ring_alpha.png'),shininess=0,thickness=solar_system.planets[6].radius/10)
    ring_saturn2=ring(pos=solar_system.planets[6].pos,axis=vector(-0.25,1,0),radius=solar_system.planets[6].radius*1.8,texture=('2k_saturn_ring_alpha.png'),shininess=0,thickness=solar_system.planets[6].radius/10)
    ring_saturn3=ring(pos=solar_system.planets[6].pos,axis=vector(-0.25,1,0),radius=solar_system.planets[6].radius*1.6,texture=('2k_saturn_ring_alpha.png'),shininess=0,thickness=solar_system.planets[6].radius/10)
    ring_saturn4=ring(pos=solar_system.planets[0].pos,axis=vector(-0.25,1,0),radius=solar_system.planets[0].radius*1.4,texture=('2k_saturn_ring_alpha.png'),shininess=0,thickness=solar_system.planets[0].radius/10)
    rings_saturn.append(ring_saturn1)
    rings_saturn.append(ring_saturn2)
    rings_saturn.append(ring_saturn3)
    rings_saturn.append(ring_saturn4)
    return rings_saturn

def update_pos_ring_saturn(solar_system,rings_saturn):#кольца следуют за Сатурном
    i=10
    for ring in rings_saturn:
        ring.pos=solar_system.planets[6].pos
        ring.rotate(angle=solar_system.planets[6].angular_velocity*i,axis=vector(-0.25,1,0),origin= ring.pos)#вращение колец вокруг оси
        i+=10

def scene_light(scene,sun_light):#включаем весь свет,выключаем солнечный
    scene.lights[0].visible=True
    scene.lights[1].visible=True
    sun_light.visible=False
    
def light_from_sun(scene,solar_system,sun_light):#свет только от солнца #?не видно задний фон
    scene.lights[0].visible=False
    scene.lights[1].visible=False
    solar_system.sphere_planets[0].emissive=True#подсвечивание сферы солнца не убираем
    sun_light.visible=True

def all_light(scene,sun_light):#включаем весь свет,выключаем солнечный
    scene.lights[0].visible=True
    scene.lights[1].visible=True
    sun_light.visible=True

def trail_off_on(scene,solar_system):
    for sphere in solar_system.sphere_planets:
        if(sphere.make_trail):
            sphere.clear_trail()
            sphere.make_trail=False
        else:
            sphere.make_trail=True

def background_scene(scene,w,h):#создаем фон у планет из звезд,можно только костыльно
    background_scene=sphere(pos=vector(0,0,0),size=vector(w,h,w),texture='2k_stars.jpg',shininess=0)#создаем сферу по центру с текстурами звезд
    scene.camera.axis=vector(0,0,-w/(0.01*h))
    scene.camera.pos=vector(0,0,w/(0.01*h))

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
    background_scene(scene,w,h)
    
    solar_system=planet.All_planet()

    solar_system.planets.append(planet.Planet('sun',695.990e6,0,1.9885e30,0,texture=('2k_sun.jpg')))#создаем солнце
    sun_light=local_light(pos=vector(0,0,0),color=color.white)#устанавливаем локальный свет в позиции 0 0 0 для солнца
    sun_light.visible=False

    def key_up(event):
        k=event.key
        nonlocal move
        if(k=='1'):
            light_from_sun(scene,solar_system,sun_light)#свет только от солнца
        elif(k=='2'):
            scene_light(scene,sun_light)#свет только сцены
        elif(k=='3'):
            all_light(scene,sun_light)#весь свет
        elif(k=='4'):#убираем/возвращаем след
            trail_off_on(scene,solar_system)
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
            solar_system.speed_up(1/speed)
            speed+=10
            if(speed==0):
                speed-=1
            solar_system.speed_up(speed)
            move=True
        elif(k=='up'):
            move=False
            solar_system.speed_up(1/speed)
            speed-=10
            solar_system.speed_up(speed)
            move=True

    scene.bind('keyup',key_up)
    scene.bind('keydown',key_down)

    solar_system.planets.append(planet.Planet('mercury',2.439e6,58e9,0.32868e24,solar_system.planets[0].mass_planet,texture=('2k_mercury.jpg')))
    solar_system.planets.append(planet.Planet('venus',6.052e6,108e9,4.81068e24,solar_system.planets[0].mass_planet,texture=('2k_venus.jpg')))
    solar_system.planets.append(planet.Planet('earth',6.37822e6,150e9,5.972e24,solar_system.planets[0].mass_planet,texture=('2k_earth.jpg')))
    solar_system.planets.append(planet.Planet('mars',3.488e6,228e9,0.63345e24,solar_system.planets[0].mass_planet,texture=('2k_mars.jpg')))
    solar_system.planets.append(planet.Planet('jupiter',71.300e6,778e9,1876.64328e24,solar_system.planets[0].mass_planet,texture=('2k_jupiter.jpg')))
    solar_system.planets.append(planet.Planet('saturn',60.100e6,1429e9,561.80376e24,solar_system.planets[0].mass_planet,texture=('2k_saturn.jpg')))
    solar_system.planets.append(planet.Planet('uranus',26.500e6,2875e9,86.05440e24,solar_system.planets[0].mass_planet,texture=('2k_uranus.jpg')))
    solar_system.planets.append(planet.Planet('neptune',24.750e6,4497e9,101.59200e24,solar_system.planets[0].mass_planet,texture=('2k_neptune.jpg')))
    
    solar_system.planets[3].spawn_satellites(1,texture=('2k_moon.jpg'))
    
    #solar_system.scale_up(h)
    for planetx in solar_system.planets:
        if(planetx.mass2==0):
            continue
        print(planetx.angular_velocity,'-----',planetx.name)


    solar_system.uravn()
    solar_system.speed_up(speed)
    solar_system.create()
    solar_system.create_satellites()

    rings_saturn=ring_for_saturn(solar_system)#создаем список из колец сатурна
    light_from_sun(scene,solar_system,sun_light)

    scene.visible=True#после создания всех объектов всё отображаем

    while True:#движение объектов
        while move:
            solar_system.update_position()
            solar_system.update_position_satellites() 
            update_pos_ring_saturn(solar_system,rings_saturn)#обновляем позицию колец Сатурна

if __name__=='__main__':
    main()