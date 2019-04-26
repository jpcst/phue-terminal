# ARRUMAR
#	Ignorar ERROR

import serial
from phue import Bridge
import os
import datetime
now = datetime.datetime.now()

with open('C:/Scrape/hue.txt', 'r') as f:
    b = Bridge(f.read())
    b.connect()

lights = b.get_light_objects('id')
serial_data = serial.Serial('com3',9600)

while True:
	if(serial_data.inWaiting() > 0):
		my_data = serial_data.readline().decode().strip()
		print(my_data)

		teto1 = b.get_light(2,'on') 
		teto2 = b.get_light(4,'on') # True = acessa, False = apagada
		tetos = [teto1,teto2]

		if(tetos[0] == True or tetos[1] == True):
			b.set_light([2,4], 'on', False, transitiontime=0)
			print(now.hour,':',now.minute,' -> OFF',sep='')

		else:
			b.set_light([2,4], 'on', True, transitiontime=0)
			for luz in b.get_light_objects(): # = luzes
			 	luz.xy=[.3, .3]
			lights[2].brightness=254
			lights[4].brightness=254
			print(now.hour,':',now.minute,' -> ON',sep='')

		# print(tetos,'\n')
