from game_logic.engine import *
from game_logic.engine_game import *
from app import aventura_elegida

import random

def get_first_step_adventure():
    """
    Obtiene la aventura, identifica la primera pregunta.
    """

    cursor = conexion.cursor()
    query = "SELECT id_pregunta FROM pregunta FROM pregunta WHERE id_aventura = %s AND id_paso = 1"
    cursor.execute(query, (aventura_elegida,))

    resultado = jugar_pregunta(query)

    id_actual = 0
    for fila in cursor:
        id_actual = fila[0]

    cursor.close()

    while id_actual != 0:
        id_actual = jugar_pregunta(id_actual)

    # HASTA EL FINAL DL JUEGO
    return id_actual


def jugar_pregunta(id_pregunta):
    """
    Busca una pregunta, selecciona 4 opciones aleatorias de las 14 disponibles 
    y permite al usuario usuario elegir.
    """

    cursor = conexion.cursor()
    query_pregunta = "SELECT id_pregunta, texto FROM pregunta WHERE id_pregunta = %s"
    cursor.execute(query_pregunta, (id_pregunta,))

    pregunta_texto = ""
    for fila in cursor:
        pregunta_texto = fila[1]
    
    query_opciones = "SELECT id_opcion, texto, id_pregunta_final FROM opciones WHERE id_pregunta_base = %s"
    cursor.execute(query_opciones, (id_pregunta,))

    todas_opciones = []
    for fila in cursor:
        todas_opciones.append(fila)
    
    opciones_seleccionadas = []
    ids_usados = []

    while len(opciones_seleccionadas) < 4:
        ids_aleatorios = random.randint(0, 13)

        if ids_aleatorios not in ids_usados and ids_aleatorios < len(todas_opciones):
            ids_usados.append(ids_aleatorios)
            opciones_seleccionadas.append(todas_opciones[ids_aleatorios])
    
    texto_menu = "\n{}\n".format(pregunta_texto)
    decisiones = {}
    rango = []

    for i in range(len(opciones_seleccionadas)):
        num = i + 1
        opcion = opciones_seleccionadas[i]

        texto_menu += "{}) {}\n".format(num, opcion[0])

        decisiones[num] = opcion[2]
        rango.append(num)
    
    cursor.close()

    seleccion = getOpt(texto_menu, "Select your option: ", rango)

    resultado = decisiones[seleccion]

    return resultado