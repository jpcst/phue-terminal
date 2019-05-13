import serial
from phue import Bridge
import datetime

def print_now():
	h = datetime.datetime.now()
	agr = ('{}:{}:{}').format(h.hour,h.minute,h.second)
	print(agr,end='')

def timer():
	h = datetime.datetime.now()
	agr = ('{}:{}:{}').format(h.hour,h.minute,h.second)
	if (agr > '18:29:59'):
		return True
	else:
		return False

with open('C:/Scrape/hue.txt', 'r') as f:
    b = Bridge(f.read())
    b.connect()

lights = b.get_light_objects('id')
serial_data = serial.Serial('com3',9600)

while True:

	if(serial_data.inWaiting() > 0): # Roda apenas se receber info do arduino
		my_data = serial_data.readline().decode().strip()
	
		if(my_data > '0'): # Distancia tem q ser > 0cm
			teto1 = b.get_light(2,'on') 
			teto2 = b.get_light(4,'on') # True = on, False = off
			tetos = [teto1,teto2]

			if (timer() == True):

				if(tetos[0] == True or tetos[1] == True):
					lights[2].brightness=254
					lights[4].brightness=254
					b.set_light([2,4], 'on', False, transitiontime=0)
					print_now()
					print(' ->',my_data,'cm [off]')
				else:
					b.set_light([2,4], 'on', True, transitiontime=0)
					lights[2].xy = [.3,.3]
					lights[4].xy = [.3,.3]
					lights[2].brightness=254
					lights[4].brightness=254
					print_now()
					print(' ->',my_data,'cm [on]')

			else:
				print_now()
				print(' -> sol')
				pass
