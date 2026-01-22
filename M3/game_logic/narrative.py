from game_logic.engine import *
from game_logic.engine_game import *

import random

historial_tupla = ()
paso_registrar = ()

def getChoices():
    """
    Gestiona el historial de la partida actual con tuple de tuples. 
    """

    if paso_registrar != ():
        lista_aux = []
        for elemnto in historial_tupla:
            lista_aux.append(elemnto)
        
        lista_aux.append(paso_registrar)

        nuevo_paso = ()
        for item in lista_aux:
            nuevo_paso += (item,)
        
        historial_tupla = nuevo_paso
        paso_registrar = ()
    
    return historial_tupla
    
def insertCurrentChoice(idGame, actual_id_setp, id_answer):
    """
    Inserta cada elección en la tabla de pasos.
    """

    from app import user_session

    pasos = get_id_bystep_adventure()

    es_final = 0
    if actual_id_setp in pasos:
        if pasos[actual_id_setp]["Final_Step"] == 1:
            es_final = 1


    id_user = getUserIdBySession(user_session)

    cursor = conexion.cursor()

    query = "INSERT INTO paso (id_juego, id_user, id_paso, id_opcion, es_final) "
    query += "VALUES (%s, %s, %s, %s)"
    query += "ON DUPLICATE KEY UPDATE id_opcion = %s, es_final = %s"

    datos = (idGame, id_user, actual_id_setp, id_answer, es_final)

    cursor.execute(query, datos)
    conexion.commit()
    cursor.close() 

def get_id_bystep_adventure():
    """
    Diccionario de pasos (preguntas) de la aventura seleccionada.
    """

    from app import aventura_elegida

    id_by_steps = {}

    query_preguntas = "SELECT id_pregunta, texto FROM pregunta WHERE id_aventura = " + str(aventura_elegida)
    datos_preguntas = get_table(query_preguntas)

    for i in range(1, len(datos_preguntas)):
        id_pregunta = datos_preguntas[i][0]
        texto_pregunta = datos_preguntas[i][1]

        query_opciones = "SELECT id_opcion FROM opcion WHERE id_pregunta_base = " + str(id_pregunta)
        datos_opciones = get_table(query_opciones)

        ids_opciones = ()
        
        for j in range(1, len(datos_opciones)):
            id_opc_actual = datos_opciones[j][0]
            ids_opciones += (id_opc_actual,)
        
        es_final = 1
        
        if len(ids_opciones) == 0:
            es_final = 0
        
        id_by_steps[id_pregunta] = {
            "Description": texto_pregunta,
            "answers_in_step": ids_opciones,
            "Final_Step": es_final
        }
    
    
    return id_by_steps

def get_answers_bystep_adventure():
    """
    Diccionario con repsuestas detallas.
    """

    from app import aventura_elegida

    idAnswers_ByStep_Adventure = {}

    # Query que une opcioness con sus preguntas filtrando por la aventura elegida.
    query = "SELECT o.id_opcion, o.id_pregunta_base, o.texto, o.id_pregunta_siguiente, "
    query += "o.id_personaje_especifico, o.probabilidad_base, o.probabilidad_fuera_clase "
    query += "FROM opcion o JOIN pregunta p ON o.id_pregunta_base = p.id_pregunta "
    query += "WHERE p.id_pregunta = " + str(aventura_elegida)

    datos = get_table(query)

    for i in range(1, len(datos)):
        id_opc = datos[i][0]
        id_base = datos[i][1]
        clave = (id_opc, id_base)

        idAnswers_ByStep_Adventure[clave] = {
            "Description": datos[i][2],
            "Nexttep_Adventure": datos[i][3],
            "Resolution_Answer": datos[i][2],
            "pj_req": datos[i][4],
            "p_base": datos[i][5],
            "p_fuera": datos[i][6]
        }

    return idAnswers_ByStep_Adventure

def playStep(id_pregunta, dic_pasos, dic_respuestas, id_juego_actual):
    """
    Muestra el paso actual, sus 5 opciones y gestiona la progresión o muerte.
    """

    from app import personaje_elegido

    paso = dic_pasos[id_pregunta]
    texto_paso = paso["Description"]
    getHeader(texto_paso)

    es_paso_final = paso["Final_Step"]
    if es_paso_final == 1:
        insertCurrentChoice(id_juego_actual, id_pregunta, 0)
        return 0

    ids_disponibles = paso["answers_in_step"]
    presentar = []
    texto_opciones = ""
    opciones_validas = []
    
    for i in range(len(ids_disponibles)):
        id_respuestas = ids_disponibles[i]
        datos_respuestas = dic_respuestas[(id_respuestas, id_pregunta)]
        presentar.append((id_respuestas, datos_respuestas))

        num = i + 1
        texto_opciones += "{}) {}\n".format(num, datos_respuestas["Description"])
        opciones_validas.append(num)

    texto_opciones += "\n6) Save & Exit to Menu"
    opciones_validas.append(6)

    eleccion = getOpt(texto_opciones, "Option: ", opciones_validas)

    if eleccion == 6:
        insertCurrentChoice(id_juego_actual, id_pregunta, 0)
        return -1

    id_opcion_elegida = presentar[eleccion - 1]
    id_opcion_real = id_opcion_elegida[0]
    datos_opcion = id_opcion_elegida[1]

    insertCurrentChoice(id_juego_actual, id_pregunta, id_opcion_real)
    
    siguiente_paso = datos_opcion["NextStep_Adventure"]
    pj_espefico = datos_opcion["pj_req"]

    if pj_espefico != 0 and pj_espefico != "":
        probabilidad = datos_opcion["p_fuera"]

        if int(pj_espefico) == int(personaje_elegido):
            probabilidad = datos_opcion["p_base"]
        
        tirada = random.randint(1, 100)
        if tirada > probabilidad:
            print("Muerte")
            return 0
    
    return siguiente_paso

def get_first_step_adventure():
    """
    Enceuntra el primer paso y ejecuta el bucle del juego.
    """

    from app import aventura_elegida, id_juego_actual

    pasos = get_id_bystep_adventure()
    respuestas = get_answers_bystep_adventure()

    query = "SELECT id_pregunta FROM pregunta_aventura WHERE id_aventura = {}".format(aventura_elegida)
    datos = get_table(query)

    id_actual = 0
    if len(datos) > 1:
        id_actual = datos[1][0]
    
    while id_actual != 0 and id_actual != -1:
        id_actual = playStep(id_actual, pasos, respuestas, id_juego_actual)
        input("Enter to continue... ")

    return 1

def replay(choices):
    """
    Reproduce una aventura paso a paso basándose en una tupla.
    """

    from app import aventura_elegida, id_juego_actual

    pasos = get_id_bystep_adventure()
    respuestas = get_answers_bystep_adventure()

    elecciones = {}

    for registro in choices:
        id_pregunta = registro[0]
        id_opcion = registro[1]
        elecciones[id_pregunta] = id_opcion

    id_actual = 0
    if len(choices) > 0:
        id_actual = choices[0][0]
    
    while id_actual != 0 and id_actual in elecciones:
        paso = pasos[id_actual]
        id_opcion_elegida = elecciones[id_actual]

        getHeader(aventura_elegida)
        print("\n" + paso["Description"] + "\n")

        ids_disponibles = paso["answers_in_step"]
        num_elegido = 0

        contador = 1
        for i in range(len(ids_disponibles)):
            id_respuesta = ids_disponibles[i]
            datos_respuestas = respuestas[(id_opcion_elegida, id_actual)]
            print("{}) {}".format(contador, datos_respuestas["Description"]))

            if id_respuesta == id_opcion_elegida:
                num_elegido = i + 1
            
            contador += 1

        datos_elegidos = respuestas[(id_opcion_elegida, id_actual)]
        print("Chosen Option: {}".format(num_elegido))

        id_actual = datos_elegidos["NextStep_Adventure"]

        input("Enter to continue... ")

    if id_actual != 0:
        while id_actual != 0 and id_actual != -1:
            id_actual = playStep(id_actual, pasos, respuestas, id_juego_actual)
            input("Enter to continue... ")
