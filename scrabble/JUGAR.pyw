import funciones
import PySimpleGUI as sg
import funcionesFichas as colocar
import random
import configuraciones as con
import os
import json
import time
from multiprocessing import Process, Lock, Value
from ctypes import c_bool
import compu
from concurrent.futures import ThreadPoolExecutor as Executor
cwd = os.getcwd()



def usuario(cantInter,hide,texto_reporte,puntajeU,estadoBolsa,tableroIm, tableroFichas, letrasU, colores, inicio, bolsa, bolsaCopia, palabras, popinter, window):
	"""
	Turno del usuario. Coloca la ficha, en caso de intercambiar se realiza en intercambio, se actualiza el puntaje en la interfaz y las palabras que colocó.

	"""
	event='comenzar'
	puestas=dict() #Fichas que voy poniendo en el tablero en esa jugada
	event, valor = colocar.colocarFicha(cantInter,tableroIm, tableroFichas, letrasU, window, colores, inicio, bolsaCopia, puestas,palabras)  # comienza la jugada
	if(event == 'palabra'):
		puntajeU = puntajeU+valor
		texto_reporte = texto_reporte + '\n' + 'Usuario: ' + funciones.tipoPalabra(puestas) + ' ' + funciones.obtener_palabra(puestas) + ' ' +  str(valor) + ' puntos'  # /n es un espacio
		window["reporte"].update(texto_reporte)
		window['puntU'].update('Puntaje:'+str(puntajeU))
		# vuelvo a repartir, si hay fichas restantes, van a quedar en el atril
		estadoBolsa=colocar.repartir(letrasU, bolsa, window)
	if(event == 'intercambiar'):
		if(hide):
			popinter.UnHide()
		event, values = popinter.read()
		popinter.Hide()
		hide = True
		cantInter=cantInter+1
		colocar.intercambiarFichas(letrasU, bolsa, bolsaCopia, window, values['cant'])
	return estadoBolsa, event, puntajeU,texto_reporte, hide, cantInter

def timer(n, lock,tiempo_dificultad,fin_tiempo,window):
	ii = tiempo_dificultad
	image3 = window['relojito']
	while n.value == False:  # ESPERA EL MENSAJE DE ROBOT1
		time.sleep(0.10) 
	comienza = n.value
	while comienza == True:  #  RECIBO MENSAJE ENTONCES COMIENZO
		time.sleep(0.01) 
		window['temporizador'].update('{:02d}:{:02d}'.format((ii // 100) // 60, (ii // 100) % 60))
		ii = ii - 1
		image3.update_animation(os.path.join(cwd,'imagenes','relojito.gif'), 150)
		if ii == 0:
			fin_tiempo = True
			break
	funciones.cargar(puntajeU,name,nivel)
	window.hide()
	funciones.mostrar_fin_partida(puntajeU,puntajeM)

global name
if __name__ == '__main__':
	turno=['compu','usuario']
	turno = random.choice(turno)
	name = sg.popup_get_text('Ingresa tu nombre para jugar', 'ScrabbleAR')
	executor = Executor()
	n = Value(c_bool, False) # Mensaje de robots para comenzar o parar timer
	lock = Lock()

	sg.theme_background_color(color='White')
	sg.theme_button_color(color=('Black', 'White'))
	sg.theme_element_background_color(color='White')
	puntajeM = 0  # inicializacion puntaje usuario y maquina
	puntajeU = 0
	# diccionario con la imagen correspondiente a cada coordenada segun el tablero
	# fichas colocadas en el tablero de forma definitiva, es decir, palabras que fueron confirmadas
	tableroFichas = dict()
	bolsa = {'A.png': {'cant': 0, 'valor': 0},
			'B.png': {'cant': 0, 'valor': 0},
			'C.png': {'cant': 0, 'valor': 0},
			'D.png': {'cant': 0, 'valor': 0},
			'E.png': {'cant': 0, 'valor': 0},
			'F.png': {'cant': 0, 'valor': 0},
			'G.png': {'cant': 0, 'valor': 0},
			'H.png': {'cant': 0, 'valor': 0},
			'I.png': {'cant': 0, 'valor': 0},
			'J.png': {'cant': 0, 'valor': 0},
			'K.png': {'cant': 0, 'valor': 0},
			'L.png': {'cant': 0, 'valor': 0},
			'M.png': {'cant': 0, 'valor': 0},
			'N.png': {'cant': 0, 'valor': 0},
			'Ñ.png': {'cant': 0, 'valor': 0},
			'O.png': {'cant': 0, 'valor': 0},
			'P.png': {'cant': 0, 'valor': 0},
			'Q.png': {'cant': 0, 'valor': 0},
			'R.png': {'cant': 0, 'valor': 0},
			'S.png': {'cant': 0, 'valor': 0},
			'T.png': {'cant': 0, 'valor': 0},
			'U.png': {'cant': 0, 'valor': 0},
			'V.png': {'cant': 0, 'valor': 0},
			'W.png': {'cant': 0, 'valor': 0},
			'X.png': {'cant': 0, 'valor': 0},
			'Y.png': {'cant': 0, 'valor': 0},
			'Z.png': {'cant': 0, 'valor': 0},
			'LL.png': {'cant': 0, 'valor': 0},
			'RR.png': {'cant': 0, 'valor': 0}}
	# diccionario que lleva la cuenta de que iagen(letra) se encuentra en cada posicion del atril a todo momento
	letrasU = {'u0': '', 'u1': '', 'u2': '',
			'u3': '', 'u4': '', 'u5': '', 'u6': ''}
	letrasM = {'m0': '', 'm1': '', 'm2': '',
			'm3': '', 'm4': '', 'm5': '', 'm6': ''}
	columna = [
		[sg.Text('', background_color='white')],
		[sg.Button(image_filename=(os.path.join(cwd,'imagenes','bolsachica.png')), border_width=0,key='intercambiar', disabled=True)],
		[sg.Button(image_filename=(os.path.join(cwd,'imagenes','palabra.png')), border_width=0,key='palabra', disabled=True)],
		[sg.Button(image_filename=(os.path.join(cwd,'imagenes','sacar.png')), border_width=0,key='sacar', disabled=True)]
	]
	column1 = [
		[sg.Image(os.path.join(cwd,'imagenes','robot.gif'), key = 'gifcompu'), sg.Text('Puntaje:0  ', font=('Fixedsys', 17), text_color='orange', background_color='white', key='puntM'),sg.Image(os.path.join('imagenes','relojito.gif'), key='relojito', background_color= 'White', visible= True), sg.Button(image_filename=os.path.join('imagenes','inicio.png'), border_width=0, key='comenzar'), sg.Text('00:00', font=('Fixedsys', 30), justification='center', text_color='orange',key='temporizador', background_color='white',visible= False)],
		[sg.Button('', image_filename=os.path.join(cwd,'imagenes','color1.png'), image_size=(46, 46), key='m0', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color2.png'), image_size=(46, 46), key='m1', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color3.png'), image_size=(46, 46), key='m2', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color4.png'), image_size=(46, 46), key='m3', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color5.png'), image_size=(46, 46), key='m4', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color1.png'), image_size=(46, 46), key='m5', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color2.png'), image_size=(46, 46), key='m6', disabled=True)],
		[sg.Column([[sg.Text('', text_color='black', key='reporte',justification= 'center', background_color='lightblue', size=(30, 500))]], scrollable= True, vertical_scroll_only= True, size = (250,400)), sg.Column(columna)],
		[sg.Image(os.path.join(cwd,'imagenes','jugador.png')), sg.Text(text='Puntaje:0  ', font=('Fixedsys', 17), text_color='orange', background_color='white', key='puntU')],
		[sg.Button('', image_filename=os.path.join(cwd,'imagenes','color1.png'), image_size=(46, 46), key='u0', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color2.png'), image_size=(46, 46), key='u1', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color3.png'), image_size=(46, 46), key='u2', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color4.png'), image_size=(46, 46), key='u3', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color5.png'), image_size=(46, 46), key='u4', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color1.png'), image_size=(46, 46), key='u5', disabled=True), sg.Button('', image_filename=os.path.join(cwd,'imagenes','color2.png'), image_size=(46, 46), key='u6', disabled=True)],
		[sg.Button(image_filename=os.path.join(cwd,'imagenes','terminar.png'), key='exit', border_width=0), sg.Text('  ', background_color='white'), sg.Button(image_filename=os.path.join(cwd,'imagenes','posponer.png'), key='posponer', border_width=0)]
	]
	
	intercambiar = [
		[sg.Text('Cant de fichas a intercambiar')],
		[sg.Spin([i for i in range(1, 8)], initial_value=1, key='cant')],
		[sg.Button('Seleccionar cuales')]
	]

	val = con.val1
	cant = con.cant1
	layoutmenu = [
		[sg.Image(os.path.join('imagenes','scrabblelogo.png'))],
		[sg.Combo(['Nivel fácil', 'Nivel medio', 'Nivel difícil'], font=('Fixedsys', 17), text_color='salmon',background_color='white', key='niveles', enable_events=True, default_value='Nivel fácil')],
		[sg.Text('Tiempo: ', font=('Fixedsys', 15), text_color='salmon', background_color='white'), sg.Text('8min', key='tiempo', font=('Fixedsys', 15), text_color='purple', background_color='white')],
		[sg.Text('Palabras posibles: ', font=('Fixedsys', 15), text_color='pink3', background_color='white'), sg.Text('sustantivos/adjetivos/verbos', key='palabras', font=('Fixedsys', 10), text_color='orange', background_color='white')],
		[sg.Text('Puntaje Letras: ', font=('Fixedsys', 15), text_color='lightblue', background_color='white'), sg.Combo(values=list(val.keys()),enable_events=True, default_value=list(val.keys())[0], key='pun', font=('Fixedsys', 15), text_color='salmon', background_color='white'),sg.Text(val['A'],key='punV',font=('Fixedsys', 15), text_color='salmon', background_color='white')],
		[sg.Text('Cant letras: ', font=('Fixedsys', 15), text_color='orange', background_color='white'), sg.Combo(values=list(cant.keys()),enable_events=True, default_value=list(cant.keys())[0], key='cant', font=('Fixedsys', 15), text_color='pink3', background_color='white'),sg.Text(cant['A'],key='cantV',font=('Fixedsys', 15), text_color='pink3',background_color='white')],
		[sg.Text('Tablero: ', font=('Fixedsys', 15), text_color='purple', background_color='white'), sg.Text('15x15', key='tab', font=('Fixedsys', 15), text_color='lightblue4', background_color='white')],
		[sg.Button('JUGAR', font=('Fixedsys', 18), button_color=('orange', 'White'), key='jugar'), sg.Button('CONFIGURAR', font=('Fixedsys', 18), button_color=('salmon', 'White'), key='configurar'), sg.Button('TOP10', font=('Fixedsys', 18), button_color=('lightblue', 'White'), key='top10')]
	]
	row1 = [sg.Text('    ',font=('Fixedsys',12),text_color='white', background_color='white'),sg.Image(os.path.join(cwd,'imagenes','letras.png'), background_color='white')]
	row2 = [sg.Text('valor',font=('Fixedsys',12),text_color='pink3', background_color='white')]
	row3 = [sg.Text('cant ',font=('Fixedsys',12),text_color='lightblue', background_color='white')]
	for y in val.keys():
		row2.append(sg.Combo(values=[x for x in range(1, 21)],default_value=1, key='valor', font=('Fixedsys', 15), text_color='purple', background_color='white'))
		row3.append(sg.Combo(values=[x for x in range(1, 21)],default_value=1, key='cant', font=('Fixedsys', 15), text_color='purple', background_color='white'))
	config = [
		[sg.Image(os.path.join(cwd,'imagenes','configtitulo.png'))],    
		row1,
		row2,
		row3,
		[sg.Text('Tiempo: ', font=('Fixedsys', 15), text_color='orange', background_color='white'), sg.Combo(values=[x for x in range(1, 61)], default_value=1,key='time', font=('Fixedsys', 15), text_color='purple', background_color='white'),sg.Text('min', font=('Fixedsys', 15), text_color='salmon', background_color='white')],
		[sg.Text('Palabras posibles: ', font=('Fixedsys', 15), text_color='salmon', background_color='white'), sg.Combo(values=['adjetivos','sustantivos','verbos','adjetivos/sustantivos/verbos', 'sustantivos/verbos','adjetivos/sustantivos','adjetivos/verbos'],default_value='adjetivo', key='tiposP', font=('Fixedsys', 15), text_color='purple', background_color='white')],
		[sg.Text('Tablero: ', font=('Fixedsys', 15), text_color='purple', background_color='white'), sg.Combo(values=[(15,15),(15,17),(15,20)],default_value=(15,15), key='table', font=('Fixedsys', 15), text_color='purple', background_color='white')],
		[sg.Button('JUGAR', font=('Fixedsys', 18), button_color=('orange', 'White'), key='jugar')]
	]   
	# parte de abajo de las fichas, cuando comieza el juego o se quito la ficha para usarla
	menuJugar = [
		[sg.Button('Nueva Partida', font=('Fixedsys', 18), button_color=('orange', 'White'), key='nuevaP'),sg.Button('Partida Vieja', font=('Fixedsys', 18), button_color=('Salmon', 'White'), key='viejaP')]   
	]
	# parte de abajo de las fichas, cuando comieza el juego o se quito la ficha para usarla
	colores = ['color1.png','color2.png',
			'color3.png','color4.png','color5.png']

	popinter = sg.Window('intercambio', intercambiar, force_toplevel= True, disable_close = True)
	menu = sg.Window('MENU', layoutmenu)
	configuracion = sg.Window('config', config)
	partidaW = sg.Window('partida',menuJugar, disable_close = True)
	

	#turno= 'usuario' aca iba antes
	tableroIm = dict()
	# llama a elegirNivel me permite poder ver la configuracion predeterminada de los niveles en la interfaz
	if(name!=None):
		event,t,palabras,tab,nivel = con.elegirNivel(menu, bolsa)
		texto_reporte = '¡Bienvenido a ScrabbleAR! \n'+str(nivel)+ '\n Tiempo: '+str(t)+'\n Palabras validas: '+str(palabras)+'\n Tienes que formar palabras	\n en el tablero usando las fichas	\n de tu atril.\n Tienes solo 3 intentos para intercambiar\n Cada vez que lo hagas pasaras\n el turno.\n Debes vencer a la computadora\n y lograr la mayor cantidad de\n puntos. Presta atencion a las\n casillas especiales, pueden\n restar o sumar puntos adicionales.\n La primera palabra debera pasar\n por el inicio\n ----------------------------------------- \n'
		menu.Hide()
		bolsaCopia=bolsa.copy()
		palabras=palabras.split('/')
		posponer=True
		# funcion para crear tablero, las coordenadas dependen de el tablero elegido en configuracion
		cantIntercambios=0
		hide = False  # Para cunado necesito esconder la ventana de intercambio de fichas
		hideTop10= False
		estadoBolsa='sigo'
		#funciones.mostrar_fin_partida()
		viejaP=False
		if(event=='configurar'):
			configB=True
		else:
			configB=False
		while(not event in (None, 'exit') and estadoBolsa=='sigo' and posponer):
			print(event)
			if(event=='volver'):
				menu.UnHide()
				event,t,palabras,tab,nivel = con.elegirNivel(menu, bolsa)
				texto_reporte = '¡Bienvenido a ScrabbleAR! \n'+str(nivel)+ '\n Tiempo: '+str(t)+'\n Palabras validas: '+str(palabras)+'\n Tienes que formar palabras	\n en el tablero usando las fichas	\n de tu atril.\n Tienes solo 3 intentos para intercambiar\n Cada vez que lo hagas pasaras\n el turno.\n Debes vencer a la computadora\n y lograr la mayor cantidad de\n puntos. Presta atencion a las\n casillas especiales, pueden\n restar o sumar puntos adicionales.\n La primera palabra debera pasar\n por el inicio\n ----------------------------------------- \n'
				menu.Hide()
			elif(event == 'jugar'):
				if(configB!=True):
					event, values = partidaW.read()
					if(event=='viejaP'):
						viejaP=True
						try:
							with open(os.path.join(cwd,'posponer.txt'),'r') as archivo:
								datos = json.load(archivo)
								tableroFichas=funciones.tuplasInter(datos['tableroFichas'])
								#tableroIm=funciones.tuplasInter(datos['tableroIm'])
								inicio, window=con.cofigtab(tuple(datos['tab']),column1,tableroIm)
								bolsa=datos['bolsa']
								bolsaCopia=datos['bolsaCopia']
								t=datos['tiempo']
								palabras=datos['palabras']
								turno=datos['turno']
								cantIntercambios=datos['cantInter']
								letrasU=datos['letrasU']
								letrasM=datos['letrasM']
								puntajeM=datos['puntajeM']
								puntajeU=datos['puntajeU']
								texto_reporte=datos['texto_reporte']
						except FileNotFoundError:
							sg.popup('No se han guardado partidas anteriormente, comenzará una partida nueva')
					elif(event=='nuevaP'):
						inicio, window=con.cofigtab(tab,column1,tableroIm)
						viejaP=False
					partidaW.close()
				else:
					configuracion.close()
				event, values = window.read()
				if(event == 'comenzar'):
					if(viejaP):
						for x in tableroFichas:
							window[x].update(image_filename=os.path.join(cwd,'imagenes',tableroFichas[x]))
						window['puntU'].update('Puntaje:'+str(puntajeU))
						window['puntM'].update('Puntaje:'+str(puntajeM))
						for y in letrasU:
							window[y].update(image_filename=os.path.join(cwd,'imagenes',letrasU[y]))
					window["reporte"].update(texto_reporte)
					
					#------ segundo proceso timer-------
					fin_tiempo = False
					tiempo_dificultad = 6000*t     # TENGO que mandarle el tiempo segun la dificultad
					executor.submit(timer,n,lock,tiempo_dificultad,fin_tiempo,window)
					with lock:   # mando mensaje para comenzar timer
						n.value = True
					#----------------------------------	
					
					estadoBolsa=colocar.repartir(letrasU, bolsa, window) # reparto fichas al usuario
					estadoBolsa=colocar.repartir(letrasM, bolsa, window) # reparto fichas a la maquina
					funciones.activarBotones(window)
					while(not event in (None, 'exit','posponer') and estadoBolsa=='sigo'):
						if(turno=='usuario'):
							estadoBolsa,event,puntajeU,texto_reporte,hide,cantIntercambios=usuario(cantIntercambios,hide,texto_reporte,puntajeU,estadoBolsa,tableroIm, tableroFichas, letrasU, colores, inicio, bolsa, bolsaCopia, palabras, popinter, window)
							estadoBolsa,puntajeM,texto_reporte=compu.turno_maquina(texto_reporte,puntajeM,inicio,tableroIm, tableroFichas, letrasM, window, colores, bolsa, bolsaCopia,nivel)
						else:
							estadoBolsa,puntajeM,texto_reporte=compu.turno_maquina(texto_reporte,puntajeM,inicio,tableroIm, tableroFichas, letrasM, window, colores, bolsa, bolsaCopia,nivel)
							estadoBolsa,event,puntajeU,texto_reporte,hide,cantIntercambios=usuario(cantIntercambios,hide,texto_reporte,puntajeU,estadoBolsa,tableroIm, tableroFichas, letrasU, colores, inicio, bolsa, bolsaCopia, palabras, popinter, window)
					if(estadoBolsa=='vacio'):
						sg.popup('No quedan mas fichas en la bolsa, fin del juego')
						window.close()
						funciones.cargar(puntajeU, name, nivel)
						funciones.mostrar_fin_partida(puntajeU,puntajeM)
				elif(event == 'terminar'):
					window.close()
				else:
					event, values = window.read()
			elif(event =='configurar'):
				menu.close()
				event, values = configuracion.read()
				while(event!='jugar'):
					event, values = configuracion.read()
				configuracion.Hide()
				con.configcustom(bolsa, -1, list(val.keys()), values, 'valor')
				con.configcustom(bolsa, 27, list(cant.keys()), values, 'cant')
				tab=values['table']
				inicio, window=con.cofigtab(tab,column1,tableroIm)
				t=values['time']
				palabras=values['tiposP']
				palabras=palabras.split('/')
				bolsaCopia=bolsa.copy()
				estadoBolsa='sigo'
				configB=True
				texto_reporte = '¡Bienvenido a ScrabbleAR! \n'+str(nivel)+ '\n Tiempo: '+str(t)+'\n Palabras validas: '+str(palabras)+'\n Tienes que formar palabras	\n en el tablero usando las fichas	\n de tu atril.\n Tienes solo 3 intentos para intercambiar\n Cada vez que lo hagas pasaras\n el turno.\n Debes vencer a la computadora\n y lograr la mayor cantidad de\n puntos. Presta atencion a las\n casillas especiales, pueden\n restar o sumar puntos adicionales.\n La primera palabra debera pasar\n por el inicio\n ----------------------------------------- \n'
			elif(event=='posponer'):
				with open('posponer.txt','w') as archivo:
					tb=funciones.tuplasString(tableroIm)
					tF=funciones.tuplasString(tableroFichas)
					datos={'texto_reporte':texto_reporte,'bolsaCopia':bolsaCopia,'tableroFichas':tF,'tableroIm':tb,'tab':tab,'inicio':inicio,'bolsa':bolsa,'tiempo':t,'palabras':palabras,'turno':turno,'cantInter':cantIntercambios,'letrasU':letrasU,'letrasM':letrasM,'puntajeM':puntajeM,'puntajeU':puntajeU}
					json.dump(datos, archivo)
					posponer=False
			elif(event == 'top10'):
				try:
					with open((os.path.join(cwd,"puntajes.json"))) as arc:
						datos = json.load(arc)
						if not datos:
							sg.popup('Archivo de puntajes no encontrado')
						else:
							puntajes = sorted(datos, reverse=True, key=lambda x: x[1])
							hideTop10,event=funciones.mostrar_top10(hideTop10,puntajes,menu)
							print('hola')

				except FileNotFoundError:
					sg.popup('Archivo de puntajes no encontrado')