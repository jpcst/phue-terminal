#!/usr/bin/python3

import serial
import os
import datetime
import requests
from tkinter import *
from phue import Bridge

# Path do .txt
dirWin = 'C:/phue/ip.txt'
dirLin = '/home/jp/pha/ip.txt'


def sysc(c=0):  # Retorna o tipo de OS; Se c = 1, clear terminal.
	if (c == 0):
		if (os.name == 'nt'):
			return 'win'
		else:
			return 'lin'
	else:
		if (os.name == 'nt'):
			os.system('cls')
			return 'win'
		else:
			os.system('clear')
			return 'lin'

def read_ip():  # Le o ip no .txt e salva na var b ou scrapa ip novo e salva na var b.
	try:
		if (sysc() == 'win'):  # Windows
			with open(dirWin, 'r') as f:
				b = Bridge(f.read())
				b.connect()
				# print('ip ok (win)')
		else:  # Linux
			with open(dirLin, 'r') as f:
				b = Bridge(f.read())
				b.connect()
				# print('ip ok (lin)')
	except Exception as e:  # Se erro no IP, scrapar novo da API
		if (sysc() == 'win'):  # Windows
			with open(dirWin, 'w') as f:
				ip = requests.get('https://www.meethue.com/api/nupnp').json()[0]['internalipaddress']
				f.write('{}'.format(ip))
				b = Bridge(ip)
				# print('new ip (win)')
		else:  # Linux
			with open(dirLin, 'w') as f:
				# API com o ip da Bridge
				ip = requests.get('https://www.meethue.com/api/nupnp').json()[0]['internalipaddress']
				f.write('{}'.format(ip))
				b = Bridge(ip)
				# print('new ip (lin)')
	return b


b = read_ip()
lights = b.get_light_objects('id')  # Lista das luzes [1,2,3,4]

# def change_color(luz, cor):
# 	cores = ['red', 'green']
# 	if cor == 1:
# 		lights[luz].xy = [.6, .3]
# 	if cor == 2:
# 		lights[luz].xy = [.1, .7]
#
# change_color(3, 1)

# Conecta o arduino com Python
if (sysc() == 'win'):
	serial_data = serial.Serial('COM3', 9600)
	# print('COM3\n')
else: # Linux
	serial_data = serial.Serial('/dev/ttyACM0', 9600)
	# print('/dev/ttyACM0/\n')

def do_light(bd=0, c1=0, d=0, c2=0, brilho=254, tt=0, c=0):
	list = [bd, c1, d, c2]
	list_t = []  # Lista das luzes p alterar
	cond = 1

	for i in range(len(list)):
		if(list[i] != 0):
			i += 1
			list_t.append(i) # Cria as lista das luzes p/ alterar

	for j in range(len(list_t)): # Loopa sobre as luzes selecionadas
		if (b.get_light(list_t[j], 'on') == True): # Detecta ON
			b.set_light(list_t[j], 'on', False, transitiontime=tt) # Apaga as acessas
			if(cond): # Se cond == 1
				cond = 0
		elif (j == len(list_t)-1): # J é o ultimo loop
			if(cond):
				for i in range(len(list_t)): # Loopa dnv
					b.set_light(list_t[i], 'on', True, transitiontime=tt) # Liga as apagadas
					lights[list_t[i]].brightness=brilho

	# sysc(1)
	#
	perc = brilho / 254 * 100
	return list_t, brilho, perc, tt


def print_light(bd=0, c1=0, d=0, c2=0, brilho=254, tt=0, c=0):
	x = do_light(bd, c1, d, c2, brilho, tt, c)
	print(x[0], ' [', round(x[2]), '%] [', x[3], ']', sep='')


def gui():
	root = Tk()
	root.title('Hue')
	frame = Frame(root, width=350, height=350)
	frame.pack()

	for n in lights:
		hFrame = Frame(frame)
		hFrame.pack(side=LEFT)

	def all():
		do_light(1, 1, 1, 1)

	def cei():
		do_light(c1=1, c2=1)

	def bed():
		do_light(bd=1)
		# if (b.get_light(1,'on') == True):
		# 	lights[1].hue = 33
		# 	lights[1].saturation = 20
		# 	lights[1].brightness = 254
		# else:
		# 	do_light(bd=1)

	def desk():
		do_light(d=1)
	# def desk():
		# if (b.get_light(3,'on') == True):

	btnCei = Button(root, text='cei', command=cei)
	btnBed = Button(root, text='bed', command=bed)
	btnDesk = Button(root, text='dsk', command=desk)
	btnAll = Button(root, text='all', command=all)
	btnCei.pack(side=LEFT)
	btnBed.pack(side=LEFT)
	btnDesk.pack(side=LEFT)
	btnAll.pack(side=LEFT)

	root.mainloop()


def check_state():
	pass


# do_light(d=1,brilho=254,c=0)
# print_light(d=1,c=0)
# sysc(1)
# 18000 = 30 min
# b.set_light([2,4], command)
# command =  {'transitiontime' : 300, 'on' : True, 'bri' : 254}

while True:
	usr = input(
		'\nVersion 2\n┌─┐\n│0├─ info\n│1├─ sensor\n│2├─ set hour\n│3├─ controller\n│4├─ gui\n└─┘\n\n>> ')
	v = usr.split(' ')

	if (len(v) == 1):  # Input de tamanho 1

		##  Comandos para ligar as luzes  ##

		if (usr == 'c'):  # Tetos
			sysc(1)
			print_light(c1=1, c2=1)

		elif (usr == 'b'):  # Bed
			sysc(1)
			print_light(d=1) ### TEMPORARIO

		# elif (usr == 'd'):  # Desk
		# 	sysc(1)
		# 	print_light(d=1)

		elif (usr == 'all'):  # Todas
			sysc(1)
			print_light(1, 1, 1, 1)

		elif (usr == '4'):  # Abre a GUI
			sysc(1)
			gui()

		else:
			sysc(1)
			print(v[0], 'not defined')

	elif (len(v) == 2):  # Input de tam 2

		try:

			# Roda se input é [str, float] <=> [luz, brilho]
			if (type(v[0]) == str and type(float(v[1])) == float):
				x = 254 * float(v[1])

				if (v[0] == 'b'):  # Controla bed e brilho

					if (b.get_light(3, 'on') == True):  # Se bed on
						sysc(1)
						lights[3].brightness = int(x)
					else: # Se cama off
						sysc(1)
						print_light(d=1, brilho=int(x)) ### TEMPORARIO

				elif (v[0] == 'c'): # Controla tetos e brilhos

					if (b.get_light(2,'on') == True or b.get_light(4,'on') == True): # Se teto on
						sysc(1)
						lights[2].brightness = int(x)
						lights[4].brightness = int(x)
					else: # Se teto off
						sysc(1)
						print_light(c1=1, c2=1, brilho=int(x))

				elif (v[0] == 'all'):

					if (b.get_light(1,'on') == True or b.get_light(2,'on') == True or b.get_light(3,'on') == True or b.get_light(4,'on') == True):
						sysc(1)
						lights[1].brightness = int(x)
						lights[2].brightness = int(x)
						lights[3].brightness = int(x)
						lights[4].brightness = int(x)
					else:
						sysc(1)
						print_light(1,1,1,1, brilho=int(x))

				else:
					sysc(1)
					print(v[0], v[1], 'not defined')

		except ValueError:  # Roda se input é [str, str] <=> [luz, cor]

				if (v[0] == 'c' and v[1] == 'br'): # Liga/desliga tetos em branco
					if (b.get_light(2,'on') == True or b.get_light(4,'on') == True):
						sysc(1)
						lights[2].xy = [.3, .3]
						lights[4].xy = [.3, .3] # Tetos em branco
					else:
						sysc(1)
						print_light(c1=1, c2=1)
						lights[2].xy = [.3, .3]
						lights[4].xy = [.3, .3]

				elif (v[0] == 'b' and v[1] == 'br'): # Liga/desliga bed em branco
					if (b.get_light(3,'on') == True):
						sysc(1)
						lights[3].xy = [.3, .3]
					else:
						sysc(1)
						print_light(d=1)
						lights[3].xy = [.3, .3]

				elif (v[0] == 'b' and v[1] == 'am'): # Liga/desliga bed em amarelo ### TEMPORARIO
					if (b.get_light(3,'on') == True):
						sysc(1)
						lights[3].hue = 33
						lights[3].saturation = 20
					else:
						sysc(1)
						print_light(d=1)
						lights[3].hue = 33
						lights[3].saturation = 20

				else:
					sysc(1)
					print(v[0], v[1], 'not defined')
