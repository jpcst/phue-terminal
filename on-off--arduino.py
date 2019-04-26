import serial
from phue import Bridge

b = Bridge('192.168.15.11')
b.connect()

lights = b.get_light_objects('id')
serial_data = serial.Serial('com3',9600)

while True:
	if(serial_data.inWaiting() > 0):
		my_data = serial_data.readline()
		print(my_data)

		teto1 = b.get_light(2,'on') 
		teto2 = b.get_light(4,'on') # True = acessa, False = apagada
		tetos = [teto1,teto2]

		if(tetos[0] == True or tetos[1] == True):
			b.set_light([2,4], 'on', False, transitiontime=0)
			print('TURNING OFF')

		else:
			b.set_light([2,4], 'on', True, transitiontime=0)
			for luz in b.get_light_objects(): # = luzes
			 	luz.xy=[.3, .3]
			lights[2].brightness=254
			lights[4].brightness=254
			print('TURNING ON')

		print(tetos,'\n')
