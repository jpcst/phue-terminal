import serial
from phue import Bridge
import datetime
import os

serial_data = serial.Serial('com3',9600)

def print_now():
	h = datetime.datetime.now()
	agr = ('{}:{}:{}').format(h.hour,h.minute,h.second)
	print(agr,end='')

def timer(hr,m,sec):
	h = datetime.datetime.now()
	# agr = ('{}:{}:{}').format(h.hour,h.minute,h.second)
	if (h.hour > hr):
		return True
	elif (h.hour > hr and h.minute > m):
		return True
	elif (h.hour > hr and h.minute < m):
		return True
	elif (h.hour > hr and h.minute > m and h.second > sec):
		return True
	elif (h.hour > hr and h.minute < m and h.second < sec):
		return True
	elif (h.hour > hr and h.minute < m and h.second > sec):
		return True
	elif (h.hour > hr and h.minute > m and h.second < sec):
		return True
	else:
		return False

def read_ip():
	with open('C:/Scrape/hue.txt', 'r') as f:
	    b = Bridge(f.read())
	    b.connect()
	    return b

b = read_ip()
lights = b.get_light_objects('id')

now = [17,59,59]
def sensor():
	while True:
		if(serial_data.inWaiting() > 0): # Roda apenas se receber info do arduino
			my_data = serial_data.readline().decode().strip()

			if(my_data > '0'): # Distancia tem q ser > 0cm
				teto1 = b.get_light(2,'on') 
				teto2 = b.get_light(4,'on') # True = on, False = off
				tetos = [teto1,teto2]
				# now = [18,9,0] # h:m:s
				if (timer(now[0],now[1],now[2]) == True): # Se hora > setado, ligar/desligar
					if(tetos[0] == True or tetos[1] == True): # on -> off
						lights[2].brightness=254
						lights[4].brightness=254
						b.set_light([2,4], 'on', False, transitiontime=0)
						print_now()
						print(' ->',my_data,'cm [off]')
					else: # off -> on
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
while True:
	usr = int(input('[0]: info\n[1]: turn on sensor\n[2]: set hour\n[3]: scrape new ip\n\n>> '))
	
	if(usr == 1): # LIGA O SENSOR
		try:
			os.system('cls')
			sensor()
		except KeyboardInterrupt:
			os.system('cls')
			pass

	# if(usr == 2):
	# 	try:
	# 		os.system('cls')
	# 		print('current -> ',end='')
	# 		print(*now,sep=':')
	# 		input()

	# 	except KeyboardInterrupt:
	# 		os.system('cls')
	# 		pass

