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


def sys():  # Retorna o tipo de OS;
	if (os.name == 'nt'):
		return 'win'
	else:
		return 'lin'
	
myOs = sys()

def clear():	# Clear terminal
	if myOs = 'win':
		os.system('cls')
	else:
		os.system('clear')

def read_ip():  # Le o ip no .txt e salva na var b ou scrapa ip novo e salva na var b.
	try:
		if (myOs == 'win'):  # Windows
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
		if (myOs == 'win'):  # Windows
			with open(dirWin, 'w') as f:
				ip = requests.get(
					'https://www.meethue.com/api/nupnp').json()[0]['internalipaddress']
				f.write('{}'.format(ip))
				b = Bridge(ip)
				# print('new ip (win)')
		else:  # Linux
			with open(dirLin, 'w') as f:
				# API com o ip da Bridge
				ip = requests.get(
					'https://www.meethue.com/api/nupnp').json()[0]['internalipaddress']
				f.write('{}'.format(ip))
				b = Bridge(ip)
				# print('new ip (lin)')
	return b


b = read_ip()
lights = b.get_light_objects('id')  # Lista das luzes [1,2,3,4]

# Conecta o arduino com Python
if (myOs == 'win'):
	serial_data = serial.Serial('COM3', 9600)
	# print('COM3\n')
else:
	serial_data = serial.Serial('/dev/ttyACM0', 9600)
	# print('/dev/ttyACM0/\n')


def do_light(bd=0, c1=0, d=0, c2=0, brilho=254, tt=0, fb=True, c=0):
	list = [bd, c1, d, c2]
	list_t = []  # Lista das luzes p alterar
	cond = 1

	for i in range(len(list)):
		if(list[i] != 0):
			i += 1
			list_t.append(i)

	for j in range(len(list_t)):
		if (b.get_light(list_t[j], 'on') == True): # Desliga as luzes
			b.set_light(list_t[j], 'on', False, transitiontime=tt)
			if(cond):
				cond = 0
		elif (j == len(list_t)-1): # J é o ultimo loop
			if(cond): # Liga as luzes
				for i in range(len(list_t)):
					b.set_light(list_t[i], 'on', True, transitiontime=tt)
					lights[list_t[i]].brightness=brilho

	# sys(1)
	perc = brilho / 254 * 100
	return list_t, brilho, perc, fb, tt


def print_light(bd=0, c1=0, d=0, c2=0, brilho=254, tt=0, fb=True, c=0):
	x = do_light(bd, c1, d, c2, brilho, tt, fb, c)
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
clear()
# 18000 = 30 min
# b.set_light([2,4], command)
# command =  {'transitiontime' : 300, 'on' : True, 'bri' : 254}

while True:
	usr = input(
		'\n┌─┐\n│0├─ info\n│1├─ sensor\n│2├─ set hour\n│3├─ controller\n│4├─ gui\n└─┘\n\n>> ')
	v = usr.split(' ')

	if (len(v) == 1):  # Input de tamanho 1

		##  Comandos para ligar as luzes  ##

		if (usr == 'c'):  # Tetos
			clear()
			print_light(c1=1, c2=1)

		elif (usr == 'b'):  # Bed
			clear()
			print_light(bd=1)

		elif (usr == 'd'):  # Desk
			clear()
			print_light(d=1)

		elif (usr == 'all'):  # Todas
			clear()
			print_light(1, 1, 1, 1)

		elif (usr == '4'):  # Abre a GUI
			clear()
			gui()

	elif (len(v) == 2):  # Input de tam 2

		try:

			# Roda se input é [str, float] <=> [luz, brilho]
			if (type(v[0]) == str and type(float(v[1])) == float):
				x = 254 * float(v[1])

				if (v[0] == 'b'):  # Controla bed e brilho

					if (b.get_light(1, 'on') == True):  # Se cama on
						clear()
						lights[1].brightness = int(x)
					else:
						clear()
						print_light(bd=1, brilho=int(x))

		except ValueError:  # Roda se input é [str, str]
			pass
