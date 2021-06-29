#!/usr/bin/python3
import serial, datetime, os, requests
from phue import Bridge
from tkinter import *

def read_ip():
	try:
		if (os.name == 'nt'): # windows
			with open('C:/phue/ip.txt','r') as f:
				b = Bridge(f.read())
				b.connect()
		else: # linux
			with open('/home/jp/pha/ip.txt', 'r') as f:
				b = Bridge(f.read())
				b.connect()
	except Exception as e: # se erro no IP, scrapar novo
		if (os.name == 'nt'): # windows
			with open('C:/phue/ip.txt','w') as f:
				ip = requests.get('https://www.meethue.com/api/nupnp').json()[0]['internalipaddress']
				f.write('{}'.format(ip))
				b = Bridge(ip)
				print('new ip (ignore)\n')
		else: # linux
			with open('/home/jp/pha/ip.txt','w') as f:
				ip = requests.get('https://www.meethue.com/api/nupnp').json()[0]['internalipaddress']
				f.write('{}'.format(ip))
				b = Bridge(ip)
				print('new ip (ignore)\n')
	return b

b = read_ip()
lights = b.get_light_objects('id') # lista das luzes
if (os.name == 'nt'): # windows
	serial_data = serial.Serial('COM3',9600)
else: # linux
	serial_data = serial.Serial('/dev/ttyACM0',9600)
h = datetime.datetime.now()

def print_now():
	agr = ('{:02d}:{:02d}:{:02d}').format(h.hour,h.minute,h.second)
	print(agr,end='')

def now():
	hr = [int(i) for i in [h.hour,h.minute]]
	return hr

def timer(hr,m):
	if (h.hour >= hr and h.minute >= m):
		return True
	else:
		return False

def sensor(hr=18,m=0):
	while True:
		if(serial_data.inWaiting() > 0): # Roda apenas se receber info do arduino
			my_data = serial_data.readline().decode().strip()
			if(my_data > '0'): # Distancia tem q ser > 0cm
				teto1 = b.get_light(2,'on')
				teto2 = b.get_light(4,'on') # True = on, False = off
				tetos = [teto1,teto2]
				if (timer(hr,m) == True): # Se hora > setado, ligar/desligar
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
					print('sol')

list_t = [b.get_light(1,'on'), b.get_light(2,'on'), b.get_light(3,'on'), b.get_light(4,'on')]

def do_light(bd=0,c1=0,d=0,c2=0,brilho=254,tt=0,set=True):
	list = [bd,c1,d,c2]
	list_t = []
	for i in range(len(list)):
		if(list[i] != 0):
			i+=1
			list_t.append(i)
	# print('selected',list_t,end='\n')
	if (len(list_t) == 1):
		if (b.get_light(list_t[0], 'on') == True):
			b.set_light(list_t[0], 'on', False, transitiontime=tt)
			set = False
		else:
			b.set_light(list_t[0], 'on', True, transitiontime=tt)
			lights[list_t[0]].brightness=brilho

	elif (len(list_t) == 2):
		if (b.get_light(list_t[0],'on') == True or b.get_light(list_t[1]) == True):
			b.set_light(list_t[0],'on', False, transitiontime=tt)
			b.set_light(list_t[1],'on', False, transitiontime=tt)
			set = False
		else:
			b.set_light(list_t[0],'on', True, transitiontime=tt)
			b.set_light(list_t[1],'on', True, transitiontime=tt)
			lights[list_t[0]].brightness=brilho
			lights[list_t[1]].brightness=brilho

	elif (len(list_t) == 3):
		if (b.get_light(list_t[0],'on') == True or b.get_light(list_t[1]) == True or b.get_light(list_t[2]) == True):
			b.set_light(list_t[0],'on', False, transitiontime=tt)
			b.set_light(list_t[1],'on', False, transitiontime=tt)
			b.set_light(list_t[2],'on', False, transitiontime=tt)
			set = False
		else:
			b.set_light(list_t[0],'on', True, transitiontime=tt)
			b.set_light(list_t[1],'on', True, transitiontime=tt)
			b.set_light(list_t[2],'on', True, transitiontime=tt)
			lights[list_t[0]].brightness=brilho
			lights[list_t[1]].brightness=brilho
			lights[list_t[2]].brightness=brilho

	elif (len(list_t) == 4):
		if(b.get_light(list_t[0],'on') == True or b.get_light(list_t[1],'on') == True or b.get_light(list_t[2],'on') == True or b.get_light(list_t[3],'on') == True):
			b.set_light(list_t[0],'on', False, transitiontime=tt)
			b.set_light(list_t[1],'on', False, transitiontime=tt)
			b.set_light(list_t[2],'on', False, transitiontime=tt)
			b.set_light(list_t[3],'on', False, transitiontime=tt)
			set = False
		else:
			b.set_light(list_t[0],'on', True, transitiontime=tt)
			b.set_light(list_t[1],'on', True, transitiontime=tt)
			b.set_light(list_t[2],'on', True, transitiontime=tt)
			b.set_light(list_t[3],'on', True, transitiontime=tt)
			lights[list_t[0]].brightness=brilho
			lights[list_t[1]].brightness=brilho
			lights[list_t[2]].brightness=brilho
			lights[list_t[3]].brightness=brilho
	os.system('cls' if os.name == 'nt' else 'clear')
	perc = brilho/254 * 100
	return list_t, brilho, perc, set, tt

def print_light(bd=0,c1=0,d=0,c2=0,brilho=254,tt=0,set=True):
	x = do_light(bd,c1,d,c2,brilho,tt,set)
	print(x[0],' at ',round(x[2]),'% (',x[1],') ',x[3],sep='')

def controle():
	while True:
		if (serial_data.inWaiting() > 0):
			my_data = serial_data.readline().decode().strip()
			print('controller:\n1 bed, 2 ceiling, 3 desk, 4 all\nPB bed yellow, AUTO on white, [][] on 100%','\n',my_data)
			if (my_data == '3810010624.0000000000000000' or my_data == '16753245.0000000000000000' or my_data == '1110306816.0000000000000000'): # Numero 1 - bed
				print_light(1)
			elif (my_data == '5316027.0000000000000000' or my_data == '16736925.0000000000000000' or my_data == '217272064.0000000000000000'): # Numero 2 - teto
				print_light(c1=1,c2=1)
			elif (my_data == '793245056.0000000000000000'): # Numero 3 - dek
				print_light(d=1)
			elif (my_data == '2427810048.0000000000000000'): # NUmero 4 - liga tudo
				print_light(1,1,1,1)
			elif (my_data == '3515284992.0000000000000000'): # PB - seta bed em amarelo
				if (b.get_light(1,'on') == True):
					lights[1].hue = 33
					lights[1].saturation = 20
				else:
					do_light(1)
					lights[1].hue = 33
					lights[1].saturation = 20
			elif (my_data == '4091398400.0000000000000000'): # AUTO - seta ligadas em branco
				for l in range(len(list_t)):
					if (list_t[l] == True):
						l+=1
						list_t2 = []
						list_t2.append(l)
						print(list_t2)
						for i in range(len(list_t2)):
							lights[list_t2[i]].xy = [.3,.3]
							# lights[list_t2[i]].brightness = 254
			elif (my_data == '3584051968.0000000000000000'): # EM BAIXO DE AUTO - seta ligadas em 254
				for l in range(len(list_t)):
					if (list_t[l] == True):
						l+=1
						list_t2 = []
						list_t2.append(l)
						print(list_t2)
						for i in range(len(list_t2)):
							lights[list_t2[i]].brightness = 254

			elif (my_data == '3770708992.0000000000000000'): # + BRILHO
				for l in range(len(list_t)):
					if (list_t[l] == True):
						l+=1
						list_t2 = []
						list_t2.append(l)
						# print(list_t2)
						for i in range(len(list_t2)):
							print(list_t2)
							lights[list_t2[i]].brightness += 30
							print(lights[list_t2[i]].brightness)
			elif (my_data == 'ovf'): # - BRILHO
				for l in range(len(list_t)):
					if (list_t[l] == True):
						l+=1
						list_t2 = []
						list_t2.append(l)
						print(list_t2)
						for i in range(len(list_t2)):
							lights[list_t2[i]].brightness -= 25
							print(lights[list_t2[i]].brightness)
			print('controller:\n1 bed, 2 ceiling, 3 desk, 4 all\nPB bed yellow, AUTO on white, [][] on 100%')

def gui():
	root = Tk()
	horizontal_frame = Frame(root)
	horizontal_frame.pack()
	def all(): # desliga/liga todas em branco
		do_light(1,1,1,1)
		lights[1].xy = [.3, .3]
		lights[2].xy = [.3, .3]
		lights[3].xy = [.3, .3]
		lights[4].xy = [.3, .3]
	def cln(): # desliga/liga teto
		do_light(c1=1,c2=1)
	def desk(): # liga/desliga desk
		do_light(d=1)
		lights[3].xy = [.3, .3] # seta 1 em branco
	def bed():
		if (b.get_light(1,'on') == 'True'):
			lights[1].hue = 33
			lights[1].saturation = 20
		else:
			do_light(1)
			lights[1].hue = 33
			lights[1].saturation = 20
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

	action = Button(root,text=('cei'),command=cln)
	action.pack(side='left')
	action = Button(root,text=('bed'),command=bed)
	action.pack(side='left')
	action = Button(root,text=('dsk'),command=desk)
	action.pack(side='left')
	action = Button(root,text=('all'),command=all)
	action.pack(side='left')
	root.mainloop()

# def make_cor(bd=0,c1=0,d=0,c2=0):
# integrar essa func em do_light

os.system('cls' if os.name == 'nt' else 'clear')
while True:
	usr = input('\n┌─┐\n│0├─ info\n│1├─ sensor\n│2├─ set hour\n│3├─ controller\n│4├─ gui\n└─┘\n\n>> ')
	v = usr.split(' ')
	if (len(v) == 1): # RODA SE INPUT = [0]
		if(usr == '0'):
			os.system('cls' if os.name == 'nt' else 'clear')
			print('len 1: c, d, b, c1, c2, all\n\nlen 2: c [bright], d [bright], b [bright],\n       b [am], b [br], c [br], d [br],\n       b d, d b\n\nlen 3: c tt [time]\n') # 7 espaços
		elif(usr == '1'): # LIGA O SENSOR NA HORA DEFAULT
			try:
				b = read_ip()
				lights = b.get_light_objects('id')
				os.system('cls' if os.name == 'nt' else 'clear')
				sensor()
			except KeyboardInterrupt:
				os.system('cls' if os.name == 'nt' else 'clear')
				pass

		elif(usr == '2'): # ALTERA A HORA E LIGA SENSOR
			try:
				os.system('cls' if os.name == 'nt' else 'clear')
				hr = int(input('>> h: '))
				mi = int(input('>> m: '))
				print('ok')
				os.system('cls' if os.name == 'nt' else 'clear')
				sensor(hr,mi)
			except KeyboardInterrupt:
				os.system('cls' if os.name == 'nt' else 'clear')
				pass
		elif(usr == '3'):
			try:
				os.system('cls' if os.name == 'nt' else 'clear')
				controle()
			except KeyboardInterrupt:
				os.system('cls' if os.name == 'nt' else 'clear')
				pass

		elif(usr == '4'):
			try:
				os.system('cls' if os.name == 'nt' else 'clear')
				gui()
				os.system('cls' if os.name == 'nt' else 'clear')
			except KeyboardInterrupt:
				os.system('cls' if os.name == 'nt' else 'clear')
				pass
		# LIGA APENAS UM GRUPO DE LUZ NO BRILHO E TT DEFAULT
		elif(usr == 'c'): # LIGA ALL TETO
			# os.system('cls' if os.name == 'nt' else 'clear')
			print_light(c1=1,c2=1)
		elif(usr == 'b'): # LIGA BED
			# os.system('cls' if os.name == 'nt' else 'clear')
			print_light(bd=1)
		elif(usr == 'd'): # LIGA DESK
			# os.system('cls' if os.name == 'nt' else 'clear')
			print_light(d=1)
		elif(usr == 'c1'): # LIGA TETO 1
			# os.system('cls' if os.name == 'nt' else 'clear')
			print_light(c1=1)
		elif(usr == 'c2'): # LIGA TETO 2
			# os.system('cls' if os.name == 'nt' else 'clear')
			print_light(c2=1)
		elif(usr == 'all'): # LIGA TODAS
			print_light(1,1,1,1)
			# os.system('cls' if os.name == 'nt' else 'clear')
		else:
			os.system('cls' if os.name == 'nt' else 'clear')
			print(usr, 'is not defined')

	elif (len(v) == 2): # RODA SE INPUT = [0,1]
		try:
			if (type(v[0]) == str and type(float(v[1])) == float): # SE INPUT = [d, float] -> luz e brilho
				x = 254 * float(v[1])
				if (v[0] == 'b'): # CONTROLA CAMA E SEU BRILHO
					if (b.get_light(1,'on') == True): # qnd cama on
						os.system('cls' if os.name == 'nt' else 'clear')
						print(v[0],' -> ',int(x),', ',float(v[1]) * 100,'%',sep='')
						lights[1].brightness = int(x)
						# fazer para outras combinacoes
					else: # qnd cama off
						os.system('cls' if os.name == 'nt' else 'clear')
						print(v[0],' -> ',int(x),', ',float(v[1]) * 100,'%',sep='')
						# print(do_light(bd=1,brilho=int(x)))
						print_light(bd=1,brilho=int(x))
						# lights[1].brightness = int(x)
				if (v[0] == 'c'): # CONTROLA ALL TETO E SEU BRILHO
					if (b.get_light(2,'on') == True or b.get_light(4,'on') == True):
						os.system('cls' if os.name == 'nt' else 'clear')
						print(v[0],' -> ',int(x),', ',float(v[1]) * 100,'%',sep='')
						lights[2].brightness = int(x)
						lights[4].brightness = int(x)
					else:
						os.system('cls' if os.name == 'nt' else 'clear')
						print(v[0],' -> ',int(x),', ',float(v[1]) * 100,'%',sep='')
						print(do_light(c1=1,c2=1,brilho=int(x)))
				if (v[0] == 'd'): # CONTROLA DESJ E SEU BRILHO
					if (b.get_light(3,'on') == True): # qnd cama on
						os.system('cls' if os.name == 'nt' else 'clear')
						print(v[0],' -> ',int(x),', ',float(v[1]) * 100,'%',sep='')
						lights[3].brightness = int(x)
						# fazer para outras combinacoes
					else: # qnd cama off
						os.system('cls' if os.name == 'nt' else 'clear')
						print(v[0],' -> ',int(x),', ',float(v[1]) * 100,'%',sep='')
						# print(do_light(bd=1,brilho=int(x)))
						print_light(d=1,brilho=int(x))
						# lights[1].brightness = int(x)

		except ValueError:
			if (type(v[0]) == str and type(v[1]) == str): # SE INPUT = [d, b] -> luz e luz, brilho default
				if (v[0] == 'b' and v[1] == 'd' or v[0] == 'd' and v[1] == 'b'): # liga/desliga bed e desk
					print_light(bd=1,d=1)
					# do_light(bd=1,d=1)
				elif (v[0] == 'b' and v[1] == 'am'): # liga/desliga bed em amarelo
					if (b.get_light(1,'on') == True):
						os.system('cls' if os.name == 'nt' else 'clear')
						lights[1].hue = 33
						lights[1].saturation = 20
						# print_light(bd=1,set=False)
					else:
						# os.system('cls' if os.name == 'nt' else 'clear')
						print_light(bd=1)
						lights[1].hue = 33
						lights[1].saturation = 20
				elif (v[0] == 'b' and v[1] == 'br'): # liga/desliga bed em branco
					if (b.get_light(1,'on') == True):
						os.system('cls' if os.name == 'nt' else 'clear')
						lights[1].xy = [.3, .3] # seta 1 em branco
						# print_light(bd=1,set=False)
					else:
						os.system('cls' if os.name == 'nt' else 'clear')
						print_light(bd=1)
						lights[1].xy = [.3, .3]
				elif (v[0] == 'c' and v[1] == 'br'): # liga/desliga bed em branco
					if (b.get_light(2,'on') == True or b.get_light(4, 'on') == True):
						os.system('cls' if os.name == 'nt' else 'clear')
						lights[2].xy = [.3, .3] # seta ceiling em branco
						lights[4].xy = [.3, .3]
						print_light(bd=1,set=False)
					else:
						os.system('cls' if os.name == 'nt' else 'clear')
						# do_light(c1=1,c2=1)
						print_light(c1=1,c2=1)
						lights[2].xy = [.3, .3]
						lights[4].xy = [.3, .3]
				elif (v[0] == 'd' and v[1] == 'br'): #liga/desliga deks em branco
					if (b.get_light(3,'on') == True):
						os.system('cls' if os.name == 'nt' else 'clear')
						lights[3].xy = [.3, .3]
					else:
						os.system('cls' if os.name == 'nt' else 'clear')
						print_light(d=3)
						lights[3].xy = [.3, .3]
				#fazer para as outras combinacoes
				else:
					os.system('cls' if os.name == 'nt' else 'clear')
					print(v[0],v[1],'is not defined')

	elif (len(v) == 3):
		pass


	elif (len(v) == 4):
		pass





# se len(usr) == 2 -> c [brilho]
