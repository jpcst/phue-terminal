#!/usr/bin/python3
from tkinter import *
from phue import Bridge
import requests

try:
    with open('/home/jp/pha/ip.txt', 'r') as f:
        b = Bridge(f.read())  # Scrapa o ip do .txt no arg
        b.connect()
        print('IP FROM HUE.TXT')

except Exception as read_err:
    print(str(read_err))
    print('IP FROM MEETHUE.COM')
    ip = requests.get('https://www.meethue.com/api/nupnp') \
        .json()[0]['internalipaddress']  # Scrapa o ip da API
    with open('/home/jp/pha/ip.txt', 'w') as f:
        f.write('{}'.format(ip))  # Salva o ip em hue.txt
        b = Bridge(ip)
        b.connect()
else:
    pass
finally:
    with open('/home/jp/pha/ip.txt', 'r') as f:
        print(f.read())

root = Tk()
horizontal_frame = Frame(root)
horizontal_frame.pack()

lights = b.get_light_objects('id')

def tres():
	b.set_light(3, 'on', True, transitiontime=0)
	lights[3].brightness=254
	#luzes = b.get_light_objects()
	for luz in b.get_light_objects(): # = luzes
		luz.xy=[.3, .3] # https://www.ledtuning.nl/en/cie-convertor
		# luz.ct=100 # https://www.ledtuning.nl/en/cie-convertor
def off():
	b.set_light([1,2,3,4], 'on', False, transitiontime=0) # Lista de luzes = [1,2,3,4]

def cor():
	b.set_light(1, 'on', True, transitiontime=0)
	lights[3].brightness=254
	for luz in b.get_light_objects():
         # luz.xy=[.7, .75]
         # luz.xy=[0.6,0.5]
         luz.hue=33
         luz.saturation = 20
def teto():
	teto1 = b.get_light(2,'on')
	teto2 = b.get_light(4,'on') # True = on, False = off
	tetos = [teto1,teto2]
	if(tetos[0] == True or tetos[1] == True):
		lights[2].brightness=254
		lights[4].brightness=254
		b.set_light([2,4], 'on', False, transitiontime=0)
	else:
		b.set_light([2,4], 'on', True, transitiontime=0)
		lights[2].xy = [.3,.3]
		lights[4].xy = [.3,.3]
		lights[2].brightness=254
		lights[4].brightness=254
		b.set_light()

for light_id in lights:
	channel_frame = Frame(horizontal_frame)
	channel_frame.pack(side = LEFT)

	scale_command = lambda x, light_id=light_id: b.set_light(light_id,{'bri': int(x), 'transitiontime': 0})
	scale = Scale(channel_frame, from_ = 254, to = 0, command = scale_command, length = 200, showvalue = 1)
	scale.set(b.get_light(light_id,'bri'))
	scale.pack()

	button_var = BooleanVar()
	button_var.set(b.get_light(light_id, 'on'))
	button_command = lambda button_var=button_var, light_id=light_id: b.set_light(light_id, 'on', button_var.get())
	button = Checkbutton(channel_frame, variable = button_var, command = button_command)
	button.pack()

	label = Label(channel_frame)
	label.config(text = b.get_light(light_id,'name'))
	label.pack()

action = Button(root, text=('1.A'), command=cor)
action.pack(side = 'left')
action = Button(root, text=('3.B'), command=tres)
action.pack(side = 'left')
action = Button(root, text=('OFF'), command=off)
action.pack(side = 'left')
action = Button(root, text=('C.ON'), command=teto)
action.pack(side = 'left')

root.mainloop()
