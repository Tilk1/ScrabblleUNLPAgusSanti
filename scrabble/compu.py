import time
import random
import combinaciones
import funcionesFichas
import os
import funciones

cwd = os.getcwd()

def colocar(coord_x, coord_y, tamaño, window, tF, formada):
	"""
    COloca las fichas de la maquina en el tablero, actualiza la interfaz con las imagenes, creo un diccionario puestas para 
	saber que fichas colocó en cada casilla, de esa manera se puede luego calcular el puntaje.

    """
	puestas=dict()
	for i in range(tamaño):
		coord = coord_x, i + coord_y
		window[(coord)].update(image_filename=(
			os.path.join(cwd,'imagenes', (formada[i] + '.png'))))
		tF.update({coord:formada[i] + '.png'})
		puestas[coord]=formada[i]+'.png'
	return puestas

def turno_maquina(tr,puntaje,coordPlay, tableroIm, tableroFichas, letrasM, window, colores, bolsa, copia,nivel):
	""" 
	Se encarga de todo el turno de la computadora en general. Esto incluye:
	1. Gif animado para simular que la computadora esta procesando
	2. obtener palabra apartir de las que tiene en la mano y formar con combinaciones.py una palabra
	3. intentar ubicarla en el tablero
	4. En caso de formar palabra y poder ubicarla entonces quitar las letras usadas de la mano
	5. robar nuevas fichas 

	"""
	botones_disable = True
	funciones.activar_desactivar_Botones_basicos(window, botones_disable)
	window['-TURNO-'].update('Turno:Compu')
	if nivel == 'Nivel fácil': # estos intentos deben setearse segun la dificultad
		intentos_formar = 3  
		intentos_ubicar = 5
	if nivel == 'Nivel medio':
		intentos_formar = 10  
		intentos_ubicar = 15
	if nivel == 'Nivel difícil':
		intentos_formar = 20  
		intentos_ubicar = 30

	#intentos_formar = 10 habia quedado fijo ups
	#intentos_ubicar = 15
	image = window['gifcompu']

	print('TENGO ESTAS FICHAS:')
	print(letrasM)

	### une las letras del diccionario en un solo string para obtener la palabra ###
	string_letras_maquina = ''
	for i in letrasM.items():
		string_letras_maquina = string_letras_maquina + i[1].split('.')[0][0]
		print('-----------LETRITA---------------')
		print(i[1].split('.')[0][0])

	# Obtiene la palabra que puede formar
	print('PUEDO FORMAR LA PALABRA:')
	palabras_candidatas = []

	for x in range(intentos_formar):  # intento 20 veces formar palabras
		window.read(1)
		# carga el gif porq esto puede ser lento
		image.update_animation(os.path.join(cwd,'imagenes', 'robot.gif'), 150)
		formada = (combinaciones.intenta_las_combinaciones_quitando_una_letra(string_letras_maquina))
		if formada != 'no_encontro':
			palabras_candidatas.append(formada)
		print('INTENTO NUMERO:', x)

	# deja la imagen estatica de la compu carita feliz
	image.update(os.path.join(cwd,'imagenes', 'robot.gif'))
	print(palabras_candidatas)
	if not palabras_candidatas:  # si esta vacia la lista es porq no pudimos formar nada
		formada = 'no_encontro'
	else:
		formada = max(palabras_candidatas, key=len)  # tomo la mas grande

	tamaño = len(formada)
	print('la palabra formada es: ', formada, 'de tamaño: ', tamaño)

	# si no encuentra palabra tira todas sus fichas a la basura (esto podria hacerse funcion)

	if formada != ('no_encontro'):
		# se para en una posicion al azar de libres
		# comprueba que las casillas no esten ocupadas osea que no este en tableroFichas.Keys
		# Pero tambien debo verificar que existan esas posiciones en el tablero, para q no se vaya a la cuarta dimension
		# Tiene cierta cantidad de intentos para ubicar su palabara en el tablero, sino pasa de turno
		if(tableroFichas == {}):
			puestas=colocar(coordPlay[0], coordPlay[1], tamaño,
					window, tableroFichas, formada)
			todas_disponibles = True
		else:
			while intentos_ubicar > 0:
				pos_elegida = (random.choice(list(tableroIm)))
				coord_x = pos_elegida[0]
				print('cordenada X : ', coord_x)
				coord_y = pos_elegida[1]
				print('cordenada Y : ', coord_y)
				todas_disponibles = True
				print('OCUPADAS POR EL MOMENTO: ', tableroFichas.keys())
				for i in range(tamaño):
					if ((coord_x, i + coord_y) not in tableroFichas.keys()) & ((coord_x, i + coord_y) in tableroIm):
						print('esta pos esta disponible: ',
							  coord_x, i + coord_y)
					else:
						print('esta pos NO esta disponible: ',
							  coord_x, i + coord_y)
						todas_disponibles = False
						break
				if todas_disponibles == False:
					intentos_ubicar -= 1
				else:
					break
			if todas_disponibles == True: 											# si estan disponibles entonces las dibujo
				# tambien agrego al diccionario de ocupadas
				puestas=colocar(coord_x, coord_y, tamaño,
						window, tableroFichas, formada)
				print(letrasM)
		if(todas_disponibles == True):
			valor=funciones.calcularPuntaje(puestas,tableroIm, copia)
			puntaje=puntaje+valor
			tr = tr + '\n' + 'Maquina: ' + funciones.tipoPalabra(puestas) + ' ' + funciones.obtener_palabra(puestas) + ' ' +  str(valor) + ' puntos'  # /n es un espacio
			window["reporte"].update(tr)
			window['puntM'].update('Puntaje:'+str(puntaje))
			for i in formada:
				print(i)
				for key, value in letrasM.items():
					if (letrasM[key].split('.')[0]) == i:
						print('Eliminando letra: ', letrasM[key])
						letrasM[key] = ''
						break
	if(formada == 'no_encontro' or todas_disponibles == False):
		print('no he podido formar o ubicar la palabra. Shame on me, paso turno')
		funcionesFichas.intercambiarFichas(
			letrasM, bolsa, copia, window, 7)  # robo nuevas fichas
		print(letrasM)

	botones_disable = False
	funciones.activar_desactivar_Botones_basicos(window, botones_disable)

	# vuelve a robar fichas de a cuerdo a las que le faltan
	fin = funcionesFichas.repartir(letrasM, bolsa, window)
	window['-TURNO-'].update('Turno:Usuario')
	return fin,puntaje, tr
