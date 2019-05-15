import serial
from phue import Bridge
import datetime
import os
import requests

def read_ip():
	try:
		with open('C:/Scrape/hue.txt', 'r') as f:
		    b = Bridge(f.read())
		    b.connect()
	except Exception as e:
	    	with open('c:/scrape/hue.txt','w') as f:
	    		   ip = requests.get('https://www.meethue.com/api/nupnp').json()[0]['internalipaddress']
	    		   f.write('{}'.format(ip))
	    		   b = Bridge(ip)
	    		   print('[new ip found]\n')
	return b
b = read_ip()
lights = b.get_light_objects('id')

serial_data = serial.Serial('com3',9600)

def print_now():
	h = datetime.datetime.now()
	agr = ('{:02d}:{:02d}:{:02d}').format(h.hour,h.minute,h.second)
	print(agr,end='')

def timer(hr,m):
	h = datetime.datetime.now()
	if (h.hour >= hr and h.minute >= m):
		return True
	else:
		return False

def scrape_ip():
	ip = requests.get('https://www.meethue.com/api/nupnp').json()[0]['internalipadress']
	with open('C:/Scrape/hue.txt','w') as f:
		f.write('{}'.format(ip))

# def read_ip():
# 	with open('C:/Scrape/hue.txt', 'r') as f:
# 	    b = Bridge(f.read())
# 	    b.connect()
# 	    return b

# b = read_ip()
# lights = b.get_light_objects('id')

now = [18,0]
def sensor():
	while True:
		if(serial_data.inWaiting() > 0): # Roda apenas se receber info do arduino
			my_data = serial_data.readline().decode().strip()
			print('[sensor ready]\n')
			if(my_data > '0'): # Distancia tem q ser > 0cm
				teto1 = b.get_light(2,'on') 
				teto2 = b.get_light(4,'on') # True = on, False = off
				tetos = [teto1,teto2]
				if (timer(now[0],now[1]) == True): # Se hora > setado, ligar/desligar
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
	usr = input('[0] info\n[1] turn on sensor\n[2] set hour\n\n>> ')
	
	if(usr == '1'): # LIGA O SENSOR
		try:
			b = read_ip()
			lights = b.get_light_objects('id')
			os.system('cls')
			sensor()
		except KeyboardInterrupt:
			os.system('cls')
			pass

	# if(usr == 2):
	# 	os.system('cls')
	# 	print('current -> ',end='')
	# 	print(*now,sep=':')
	# 	novo_now = []
	# 	novo_now.append(input('>> '))
	# 	print(*novo_now)
