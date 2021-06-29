# !/usr/bin/python3
# Edit 01/11/20

# 1: Bed (off line)
# 2: C1
# 3: Desk
# 4: C2

import os
import requests
from phue import Bridge

os.system('mode con cols=50 lines=25')
# os.system('mode con cols=15 lines=5')
size = os.get_terminal_size().columns

dir_win = 'C:/GitHub/phue-terminal-master/ip.txt'
dir_lin = '/home/jp/phue/ip.txt'

def os_type(): # Detecta tipo de OS
	if(os.name == 'nt'):
		return 'win'
	else:
		return 'lin'

def clean(): # Limpa o terminal
	if(os_type() == 'win'):
		os.system('cls')
	else:
		os.system('clear')

# def arduino(): # Conecta o arduino com python
# 	import serial
# 	if (os_type() == 'win'):
# 		serial_data = serial.Serial('COM3', 9600)
# 	else:
# 		serial_data = serial.Serial('/dev/ttyACM0', 9600)
# 	return serial_data

def read_ip(): # Le o ip no .txt e conecta na brigde
	try: # Conecta na bridge se ip está ok
		if (os_type() == 'win'): # Windows
			with open(dir_win, 'r') as f:
				b = Bridge(f.read())
				b.connect()
		else: # Linux
			with open(dir_lin, 'r') as f:
				b = Bridge(f.read())
				b.connect()
		# print('* IP OK *'.center(size))
	except Exception as e: # Erro no ip, scrape novo
		ip = requests.get('https://discovery.meethue.com/').json()[0]['internalipaddress']
		if (os_type() ==  'win'): # Windows
			with open(dir_win, 'w') as f:
				f.write('{}'.format(ip))
				b = Bridge(ip)
		else: # Linux
			with open(dir_lin, 'w') as f:
				f.write('{}'.format(ip))
				b = Bridge(ip)
		print('* NEW IP *'.center(size))
	return b

b = read_ip()
lights = b.get_light_objects('id')

lights_list = []
for i in lights:
	lights_list.append(i) # Cria lista com as luzes do app

def is_on(*lights_list): # Return a matrix with the state of all lights and brightness
	lights_list = []
	for i in lights:
		lights_list.append(i)

	lights_on = [] # Return which lights are on
	lights_bri = [] # Return each brightness

	for i in range(len(lights_list)):
		try:
			if (b.get_light(lights_list[i], 'on') == True):
				lights_on.append(True)
				bri = b.get_light(lights_list[i], 'bri')
				bri = round(bri / 254 * 100, 2)
				lights_bri.append(bri)
			else:
				lights_on.append(False)
				lights_bri.append(0)
		except Exception as e: ## ARRUMAR ISSO QND TIRAR LUZ
			lights_on.insert(0,False)
			lights_bri.insert(0,0)
	return lights_on, lights_bri

def do_light(brilho=254, tt=0, *lights_list):
	# cond = 1
	list_t = []
	for i in range(len(lights_list)):
		if(lights_list[i] != 0):
			i+=1
			list_t.append(i) # Cria a lista das luzes para alterar

	for i in range(len(list_t)): # Loopa sobre as luzes selecionadas
		if (b.get_light(list_t[i], 'on') == True): # Detecta ON
			b.set_light(list_t[i], 'on', False, transitiontime=tt) # Apaga as acessas
			# if(cond): # Se cond == 1
				# cond = 0
		elif (i == len(list_t)-1): # J é o ultimo loop
			# if(cond):
			for i in range(len(list_t)): # Loopa dnv
				b.set_light(list_t[i], 'on', True, transitiontime=tt) # Liga as apagadas
				lights[list_t[i]].brightness=brilho

	# perc = brilho / 254 * 100
	# return list_t, brilho, perc, tt
	return list_t

def do_light_beta(mode=1, brilho=254, tt=0, *lights_list): # Se mode = off, apenas apaga; se mode = on, apenas acende
	list_t = []
	for i in range(len(lights_list)):
		if(lights_list[i] != 0):
			i+=1
			list_t.append(i) # Cria a lista das luzes para alterar

	if mode == 1:
		for i in range(len(list_t)): # Loopa sobre as luzes selecionadas
			if (b.get_light(list_t[i], 'on') == True): # Detecta ON
				b.set_light(list_t[i], 'on', False, transitiontime=tt) # Apaga as acessas
				# if(cond): # Se cond == 1
					# cond = 0
			elif (i == len(list_t)-1): # J é o ultimo loop
				# if(cond):
				for i in range(len(list_t)): # Loopa dnv
					b.set_light(list_t[i], 'on', True, transitiontime=tt) # Liga as apagadas
					lights[list_t[i]].brightness=brilho

	elif mode == 'off':
		for i in range(len(list_t)): # Loopa sobre as luzes selecionadas
			if (b.get_light(list_t[i], 'on') == True): # Detecta ON
				b.set_light(list_t[i], 'on', False, transitiontime=tt) # Apaga as acessas



	# perc = brilho / 254 * 100
	# return list_t, brilho, perc, tt
	return list_t

def rgb_color(r, g, b):
	x = 0.4124*r + 0.3576*g + 0.1805*b
	y = 0.2126*r + 0.7152*g + 0.0722*b
	z = 0.0193*r + 0.1192*g + 0.9505*b
	x_hat = x / (x+y+z)
	y_hat = y / (x+y+z)
	return round(x_hat,4), round(y_hat,4)

def get_light_names(*lights_list): # Return light names from phone app
	lights_list = []
	for i in lights:
		lights_list.append(i)

	lights_name = []
	for i in lights_list:
		lights_name.append(b.get_light(i, 'name'))
	return lights_name


print_names = get_light_names()
print_names[:0] = ['LIGHTS']

########################################################################################### Main Loop ############################################################################################

def mainloop():

	print('\n')
	on = is_on()
	print_on = is_on()
	print_on[0][:0] = ['ON/OFF']
	print_on[1][:0] = ['BRIGHTNESS (%)']
	# print(on, '\n\n\n') # Debug
	# print(on[0][2])
	# print('\n\n\n'.center(size))
	for i in range(len(print_names)):
		print('     ', print_names[i].center(size//4), str(print_on[0][i]).center(size//5), str(print_on[1][i]).center(size//4),'\n')

	# print('{: ^50}'.format('Version 3\n'))
	# print('* VERSION 3 *\n'.center(size))
	# usr = input('-> '.center(os.get_terminal_size().columns))
	usr = input('\n\n\n\n-> ')
	v = usr.split(' ')

	## COMANDOS PARA CONTROLAR AS LUZES ##

	if (len(v) == 1): # Input de tamanho 1 <=> eg: 'c', 'all'
		clean()

		if (usr == 'c'): # Teto 1 e 2
			# do_light(254,0,0,1,0,1)
			do_light_beta(1,254,0,0,1,0,1)

		elif (usr == 'c1'): # Teto 1
			do_light(254,0,0,1,0,0)

		elif (usr == 'b'): # Cama (desk)
			do_light(254,0,0,0,1,0)

		elif (usr == 'c2'): # Teto 2
			do_light(254,0,0,0,0,1)

		elif (usr == 'all'): # Todas
			do_light(254,0,1,1,1,1)

		elif (usr == 'nox'): # Apaga todas acessas
			do_light_beta('off',254,0, 1,1,1,1)

		elif (usr == 'party'):
			from random import randrange
			from time import sleep
			# while True:
			# 	try:
			# 		# for i in ligadas:
			# 		# 	color = rgb_color(randrange(255),randrange(255),randrange(255))
			# 		# 	lights[i].xy = [color[0], color[1]
			# 		color1 = rgb_color(randrange(255),randrange(255),randrange(255))
			# 		color2 = rgb_color(randrange(255),randrange(255),randrange(255))
			# 		color3 = rgb_color(randrange(255),randrange(255),randrange(255))
			# 		lights[2].xy = [color1[0], color1[1]]
			# 		lights[3].xy = [color2[0], color2[1]]
			# 		lights[4].xy = [color3[0], color3[1]]
			# 		sleep(1)
			# 	except KeyboardInterrupt:
			# 		break
			while True:
				ligadas = [i for i, y in enumerate(on) if y == True]
				# print(ligadas)
				try:
					for i in range(len(ligadas)):
						color = rgb_color(randrange(255),randrange(255),randrange(255))
						luz = ligadas[i] + 1
						lights[luz].xy = [color[0], color[1]]
						# sleep(1)
				except KeyboardInterrupt:
					break

		else:
			print(v[0], 'is not defined.')

		# print(is_on())

	elif (len(v) == 2): # Input de tamanho 2
		clean()

		try:

			if (type(v[0]) == str and type(float(v[1])) == float): # Roda se input é [str,float] <=> eg: [luz, brilho]
				x = 254 * float(v[1])

				if (v[0] == 'b'): # Controla desk (bed) e brilho

					if (on[0][2] == True): # Se on, up brightness
					# if (b.get_light(3,'on') == True):
						lights[3].brightness = int(x)
					else: # Se off, ligar e up brightness
						do_light(int(x),0,0,0,1,0)

				elif (v[0] == 'c'): # Controla teto e brilho

					if (on[1] == True and on[3] == True): # Se todas on, mudar brilho
					# if (b.get_light(2,'on') == True or b.get_light(4,'on') == True):
						lights[2].brightness = int(x)
						lights[4].brightness = int(x)
					elif (on[1] == True and on[3] == False): # Se uma off, mudar brilho e ligar outra
						lights[2].brightness = int(x)
						do_light(int(x),0,0,0,0,1)
					elif (on[1] == False and on[3] == True): # Idem cima
						lights[4].brightness = int(x)
						do_light(int(x),0,0,1,0,0)
					else: # Se todas off, ligar todas e mudar brilho
						do_light(int(x),0,0,1,0,1)

				else:
					print(v[0], v[1], 'are not defined.')

		except ValueError: # Roda se input é str, str <=> eg [c, red], [c, b]

			if (v[0] == 'c' and v[1] == 'br'): # Muda teto para branco

					if (on[0][1] == True and on[0][3] == True): # Se todas on, mudar cor
						lights[2].xy = [.3, .3]
						lights[4].xy = [.3, .3]
					elif (on[0][1] == True and on[0][3] == False): # Se uma off, mudar cor e ligar outra
						lights[2].xy = [.3, .3]
						do_light(254,0,0,0,0,1)
						lights[4].xy = [.3, .3]
					elif (on[0][1] == False and on[0][3] == True): # Idem cima
						lights[4].xy = [.3, .3]
						do_light(254,0,0,1,0,0)
						lights[2].xy = [.3, .3]
					else: # Se todas off, ligar todas e mudar brilho
						do_light(254,0,0,1,0,1)
						lights[2].xy = [.3, .3]
						lights[4].xy = [.3, .3]

			elif (v[0] == 'c' and v[1] == 'am'): # Muda teto para amarelo

				# am = rgb_color(0,0,255)
				am = rgb_color(255,225,122)
				if (on[0][1] == True and on[0][3] == True): # Se todas on, mudar cor
					lights[2].xy = [am[0], am[1]]
					lights[4].xy = [am[0], am[1]]
				elif (on[0][1] == True and on[0][3] == False): # Se uma off, mudar cor e ligar outra
					lights[2].xy = [am[0], am[1]]
					do_light(254,0,0,0,0,1)
					lights[4].xy = [am[0], am[1]]
				elif (on[0][1] == False and on[0][3] == True): # Idem cima
					lights[4].xy = [am[0], am[1]]
					do_light(254,0,0,1,0,0)
					lights[2].xy = [am[0], am[1]]
				else: # Se todas off, ligar todas e mudar brilho
					do_light(254,0,0,1,0,1)
					lights[2].xy = [am[0], am[1]]
					lights[4].xy = [am[0], am[1]]

			elif (v[0] == 'b' and v[1] == 'am'): # Muda cama para amarelo

				am = rgb_color(255,225,122)
				if(on[2] == True):
					lights[3].xy = [am[0], am[1]]
				else:
					do_light(254,0,0,0,1,0)
					lights[3].xy = [am[0], am[1]]

			elif (v[0] == 'b' and v[1] == 'br'): # Muda cama para branco

				if(on[2] == True):
					lights[3].xy = [.3, .3]
				else:
					do_light(254,0,0,0,1,0)
					lights[3].xy = [.3, .3]

if __name__ == '__main__':
	while True:
		mainloop()
