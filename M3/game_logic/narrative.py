from game_logic.engine import *
from game_logic.engine_game import *
from app import aventura_elegida, personaje_elegido, id_juego_actual, user_session

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
    Inserta cada elección individual en la tabal de pasos.
    """

    id_user = getUserIdBySession(user_session)

    cursor = conexion.cursor()

    query = "INSER INTO paso (id_juego, id_user, id_paso, id_opcion, id_user) VALUES (%s, %s, %s, %s)"
    datos = (idGame, id_user, actual_id_setp, id_answer)

    cursor.execute(query, datos)
    conexion.commit()
    cursor.close() 

def get_id_bystep_adventure():
    """
    Diccionario de pasos (preguntas) de la aventura seleccionada.
    """

    id_by_steps = {}
    query_preguntas = "SELECT id_pregunta, texto FROM pregunta WHERE id_aventura = " + str(aventura_elegida)
    datos_preguntas = get_table(query_preguntas)

    i = 1
    total_preguntas = len(datos_preguntas)

    while i < total_preguntas:
        fila = datos_preguntas[i]
        id_pregunta = fila[0]
        texto_pregunta = fila[1]

        query_opciones = "SELECT id_opcion FROM opcion WHERE id_pregunta_base = " + str(id_pregunta)
        datos_opciones = get_table(query_opciones)

        ids_opciones = ()
        j = 1
        total_opciones = len(datos_opciones)
        while j < total_opciones:
            id_opc_actual = datos_opciones[j][0]
            ids_opciones += (id_opc_actual,)
            j += 1
        
        es_final = 0
        num_opciones = len(ids_opciones)
        if num_opciones == 0:
            es_final = 1
        
        id_by_steps[id_pregunta] = {
            "Description": texto_pregunta,
            "answers_in_step": ids_opciones,
            "Final_Step": es_final
        }

        i += 1
    
    return id_by_steps

def get_answers_bystep_adventure():
    """
    Diccionario con repsuestas detallas.
    """

    idAnswers_ByStep_Adventure = {}

    # Query que une opcioness con sus preguntas filtrando por la aventura elegida.
    query = "SELECT o.id_opcion, o.id_pregunta_base, o.texto, o.id_pregunta_final, "
    query += "o.id_personaje_especifico, o.probabilidad_base, o.probabilidad_fuera_clas "
    query += "FROM opcion o JOIN pregunta p ON o.id_pregunta_base = p.id_pregunta "
    query += "WHERE p.id_pregunta = " + str(aventura_elegida)

    datos = get_table(query)

    i = 1
    total_respuestas = len(datos)
    while i < total_respuestas:
        id_opc = datos[i][0]
        id_base = datos[i][1]
        clave = (id_opc, id_base)

        idAnswers_ByStep_Adventure[clave] = {
            "Description": datos[i][2],
            "NexStep_Adventure": datos[i][3],
            "Resolution_Answer": datos[i][2],
            "pj_req": datos[i][4],
            "p_base": datos[i][5],
            "p_fuera": datos[i][6]
        }

        i += 1

        return idAnswers_ByStep_Adventure

def playStep(id_pregunta, dic_pasos, dic_respuestas, id_juego_actual):
    """
    Gestiona la visualización y la selección aleatoria de opciones.
    """

    paso = dic_pasos[id_pregunta]

    print("\n" + "*" * ancho)
    texto_paso = paso["Description"]
    print(texto_paso.center(ancho))
    print("*" * ancho)

    es_paso_final = paso["Final_Step"]
    if es_paso_final == 1:
        return 0

    ids_disponibles = paso["answers_in_step"]
    num_total = len(ids_disponibles)

    max_indice_random = num_total - 1

    presentar = []
    usados = []
    limite_opciones = 4
    if num_total < 4:
        limite_opciones = num_total

    while len(presentar) < limite_opciones:
        pos = random.randint(0, max_indice_random)
        if pos not in usados:
            usados.append(pos)
            id_seleccionada = ids_disponibles[pos]
            data = dic_respuestas[(id_seleccionada, id_pregunta)]
            presentar.append((id_seleccionada, data))
    
    texto = ""
    opciones_validas = []
    idx = 0

    while idx < len(presentar):
        num = idx + 1
        texto += str(num) + ")" + presentar[idx][1]["Description"] + "\n"
        opciones_validas.append(num)
        idx += 1

    texto += "\n0) Save & Continue\n-1) Save & Exit"
    opciones_validas.append(0, -1)

    eleccion = getOpt(texto, "Option: ", opciones_validas)

    if eleccion == -1:
        print("\n" + "[!] Exiting and saving progress...".center(ancho))
        return -1
    
    if eleccion == 0:
        print("\n" + "[!] OK Progress saved. Choose an action to continue: ".center(ancho))
        resultado = playStep(id_pregunta, dic_pasos, dic_respuestas, id_juego_actual)
        return resultado

    id_paso = presentar["id_paso"]
    id_opcion_elegida = presentar[eleccion -1][0]
    info_opc = presentar[eleccion -1][1]

    paso_registrar = (id_paso, id_opcion_elegida)
    getChoices

    insertCurrentChoice(id_juego_actual, id_paso, id_opcion_elegida)
    
    siguiente_paso = info_opc["NextStep_Adventure"]

    pj_espefico = info_opc["pj_req"]

    if pj_espefico != 0 and pj_espefico != "":
        proba_exito = info_opc["p_fuera"]

        if pj_espefico == personaje_elegido:
            proba_exito = info_opc["p_base"]
        
        tirada = random.randint(1, 100)

        if tirada > proba_exito:
            print("Muerte")
            siguiente_paso = 0
    
    return siguiente_paso

def get_first_step_adventure():
    """
    Enceuntra el primer paso y ejecuta el bucle del juego.
    """

    pasos = get_first_step_adventure()
    respuestas = get_answers_bystep_adventure()

    cursor = conexion.cursor()
    query = "SELECT id_pregunta FROM pregunta FROM pregunta WHERE id_aventura = " + str(aventura_elegida)
    datos = get_table(query)

    id_actual = 0
    if len(datos) > 1:
        id_actual = datos[1][0]
    
    while id_actual != 0:
        id_actual = playStep(id_actual, pasos, respuestas)
        input("Enter to continue... ")

    cursor.close()

    return 1