# !/usr/bin/python3

import os
import requests
from phue import Bridge

# 1 - c1
# 2 - c2
# 3 - desk

os.system('mode con cols=50 lines=20')
size = os.get_terminal_size().columns

file = 'C:/GitHub/ip.txt'

ceiling = [1,1,0]
desk = [0,0,1]
cei1 = [1,0,0]
cei2 = [0,1,0]
all = [1,1,1]

# CIE 1931
white = [0.3, 0.3]
yellow = [0.39, 0.4]
yellow_relax = [0.5019, 0.4152]
yellow_bed = [0.5203, 0.4141]
# red = [0.6401, 0.33]
# green = [0.3, 0.6]
# blue = [0.15, 0.06]

def clean():
    if (os.name == 'nt'): # Windows
        os.system('cls')
    else: # Linux
        os.system('clear')

def ip():
    try:
        with open(file, 'r') as f:
            b = Bridge(f.read())
    except Exception as _:
        print('SCRAPING...')
        ip = requests.get('https://discovery.meethue.com/').json()[0]['internalipaddress']
        with open(file, 'w') as f:
            f.write('{}'.format(ip))
            b = Bridge(ip)
        print("SAVED NEW IP", ip)
    b.connect()
    return b

b = ip()
lights = b.get_light_objects('id')

def list_of_lights():
    lights_list = []
    for i in lights:
        lights_list.append(i) # List with all lights [1..n]
    return lights_list

l = list_of_lights()

def is_on(*lights_list): # Returns list [Bool] for each light (TO FIX)
    lights_on = []
    lights_list = list_of_lights()
        
    for i in range(len(lights_list)):
        if (b.get_light(lights_list[i], 'on') == True):
            # lights_on.append(True)
            lights_on.append(1)
        else:
            # lights_on.append(False)
            lights_on.append(0)
    return lights_on

def lights_bri(*lights_list): # Returns list [Float] for each light
    lights_bri = []
    lights_list = list_of_lights()

    for i in range(len(lights_list)):
        if (b.get_light(lights_list[i], 'on') == False):
            lights_bri.append(0.0)
        else:
            bri = b.get_light(lights_list[i], 'bri')
            bri = round(bri / 254 * 100, 2)
            lights_bri.append(bri)
    return lights_bri

def lights_name(*lights_list):
    name = []
    lights_list = list_of_lights()
    for i in lights_list:
        name.append(b.get_light(i, 'name'))
    return name

def do_light(bri=254, tt=0, *lights_list):
    list_t = []
    for i in range(len(lights_list)):
        if lights_list[i] != 0 or lights_list[i] != False:
            i += 1
            list_t.append(i)
    for i in range(len(list_t)):
        # if is_on(list_t[i]) == True:
        if (b.get_light(list_t[i], 'on') == True):
            b.set_light(list_t[i], 'on', False, transitiontime=tt)
        elif i == len(list_t) - 1:
            for i in range(len(list_t)):
                b.set_light(list_t[i], 'on', True, transitiontime=tt)
                lights[list_t[i]].brightness = bri
    return list_t

def is_digit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def rgb_color(r, g, b):
	x = 0.4124*r + 0.3576*g + 0.1805*b
	y = 0.2126*r + 0.7152*g + 0.0722*b
	z = 0.0193*r + 0.1192*g + 0.9505*b
	x_hat = x / (x+y+z)
	y_hat = y / (x+y+z)
	return round(x_hat,4), round(y_hat,4)

names = lights_name()

while True:
    print_on = is_on()
    print_bri = lights_bri()
    print('\n     ', "LIGHTS".center(size//4), "ON/OFF".center(size//5), "BRIGHTNESS (%)".center(size//4), '\n')
    for i in range(len(names)):
        print('     ', names[i].center(size//4), str(bool(print_on[i])).center(size//5), str(print_bri[i]).center(size//4), '\n')
    
    list = is_on()
    list[:0] = [0]
    usr = input('\n\n=> ')
    v = usr.split(' ')

    if len(v) == 1:
        clean()

        if is_digit(v[0]) == True: # Changes bri only for lights ON
            bri = 254 * float(v[0])
            for i in range(len(list)):
                if list[i] == 1:
                    lights[i+1].brightness = int(bri)

        elif usr == 'c':
            do_light(254, 0, *ceiling)
        
        elif usr == 'd':
            do_light(254, 0, *desk)

        elif usr == 'c1':
            do_light(254, 0, *cei1)        

        elif usr == 'c2':
            do_light(254, 0, *cei2)  

        elif usr == 'all' or usr == 'on' or usr == '':
            do_light(254, 0, *all)
    
        elif usr == 'nox' or usr == 'off':
            do_light(254, 0, *list)

        else:
            print(v[0], 'NOT DEFINED.')
    
    elif len(v) == 2:
        clean()

        if is_digit(v[0]) == False and is_digit(v[1]) == True: # Input format: (str, float) ie (light, bri)
            bri = 254 * float(v[1])

            if v[0] == 'c':

                if list[0] == 1 and list[1] == 1:
                    lights[1].brigthness = int(bri)
                    lights[2].brigthness = int(bri)
                
                elif list[0] == 0 and list[1] == 1:
                    do_light(int(bri), 0, *cei1)
                    lights[2].brigthness = int(bri)
                
                elif list[0] == 1 and list[0] == 0:
                    do_light(int(bri), 0, *cei2)
                    lights[1].brigthness = int(bri)
                
                else:
                    do_light(int(bri), 0, ceiling)
            
            elif v[0] == 'd':
                if list[2] == 1:
                    lights[3].brightness = int(bri)
                else:
                    do_light(int(bri), 0, *desk)
        
        elif is_digit(v[0]) == False and is_digit(v[1]) == False:

            if v[0] == 'd' and v[1] == 'br':
                if list[4] == 1:
                    lights[5].xy = white
                else:
                    do_light(254, 0, *desk)
                    lights[5].xy = white
            
            elif v[0] == 'd' and v[1] == 'am':
                if list[4] == 1:
                    lights[5].xy = yellow_relax
                else:
                    do_light(254, 0, *desk)
                    lights[5].xy = yellow_relax

            elif v[0] == 'c' and v[1] == 'br':

                if list[0] == 1 and list[1] == 1:
                    pass
                
                elif list[0] == 0 and list[1] == 1:
                    do_light(254, 0, *cei1)
                
                elif list[0] == 1 and list[1] == 0:
                    do_light(254, 0, *cei2)
                
                else:
                    do_light(254, 0, *ceiling)
                
                lights[1].xy = white
                lights[2].xy = white
                lights[3].xy = white

            elif v[0] == 'c' and v[1] == 'am':

                if list[0] == 1 and list[1] == 1:
                    pass
                
                elif list[0] == 0 and list[1] == 1:
                    do_light(254, 0, *cei1)
                
                elif list[0] == 1 and list[1] == 0:
                    do_light(254, 0, *cei2)
                
                else:
                    do_light(254, 0, *ceiling)
                
                lights[1].xy = yellow
                lights[2].xy = yellow
                lights[3].xy = yellow
            
            else:
                print(v[0], v[1], 'NOT DEFINED.')
    
    elif len(v) == 3:
        clean()

        if is_digit(v[0]) == True and is_digit(v[1]) == True and is_digit(v[2]) == True:
            color = rgb_color(float(v[0]), float(v[1]), float(v[2]))
            print(v, '->',color)
            for i in range(len(list)):
                if list[i] == 1:
                    lights[i+1].xy = [color[0], color[1]]
