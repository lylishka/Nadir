import random

def getChoices(id_juego):
    """
    Gestiona el historial de la partida actual con tuple de tuples. 
    """

    import game_logic.engine as engine

    query = "SELECT id_paso, id_opcion " 
    query += "FROM paso "
    query += "WHERE id_juego = {} AND id_opcion > 0 ORDER BY id_paso ASC".format(id_juego)
    datos = engine.get_table(query)

    historial = ()
    for i in range(1, len(datos)):
        id_paso = datos[i][0]
        id_opcion = datos[i][1]
        historial += (id_paso, id_opcion)
    
    return historial
    
def insertCurrentChoice(idGame, id_aventura, actual_id_setp, id_answer, id_user, es_final):
    """
    Inserta o actualizar cada elección en la tabla de pasos.
    """

    import game_logic.engine as engine

    cursor = engine.conexion.cursor()

    query = "INSERT INTO paso (id_juego, id_aventura, id_usuario, id_paso, id_opcion, es_final)"
    query += "VALUES (%s, %s, %s, %s, %s, %s)"
    query += "ON DUPLICATE KEY UPDATE id_paso = %s, id_opcion = %s, es_final = %s"

    valores = (idGame, id_aventura, id_user, actual_id_setp, id_answer, es_final, actual_id_setp, id_answer, es_final)

    cursor.execute(query, valores)
    engine.conexion.commit()
    cursor.close()

def get_id_bystep_adventure(id_aventura):
    """
    Diccionario de pasos (preguntas) de la aventura seleccionada.
    """

    import game_logic.engine as engine

    id_by_steps = {}

    query_pregunta_incio = "SELECT id_pregunta FROM pregunta_aventura WHERE id_aventura = {} LIMIT 1".format(id_aventura)
    datos_preguntas_inico = engine.get_table(query_pregunta_incio)

    datos = datos_preguntas_inico[1][0]
    preguntas_pend = [datos]
    preguntas_vista = []
    
    for id_actual in preguntas_pend:
        vista = False
        for vistas in preguntas_vista:
            if vistas == id_actual:
                vista = True

        if vista:
            continue

        query_preguntas_texto = "SELECT texto FROM pregunta WHERE id_pregunta = {}".format(id_actual)
        datos_preguntas_texto = engine.get_table(query_preguntas_texto)
        texto_pregunta = datos_preguntas_texto[1][0]

        query_opciones = "SELECT id_opcion, id_pregunta_siguiente FROM opcion WHERE id_pregunta_base = {}".format(id_actual)
        datos_opciones = engine.get_table(query_opciones)

        ids_opciones = ()
        es_final = 1
        if len(datos_opciones) > 1:
            es_final = 0
            for j in range(1, len(datos_opciones)):
                id_opc = datos_opciones[j][0]
                id_pregunta_siguiente = datos_opciones[j][1]

                ids_opciones += (id_opc,)

                if id_pregunta_siguiente > 0:
                    lista = False
                    for pendiente in preguntas_pend:
                        if pendiente == id_pregunta_siguiente:
                            lista = True
                        
                    if not lista:
                        preguntas_pend.append(id_pregunta_siguiente)
        
        id_by_steps[id_actual] = {
            "Description": texto_pregunta,
            "answers_in_step": ids_opciones,
            "Final_Step": es_final
        }

        preguntas_vista.append(id_actual)
    
    return id_by_steps

def get_answers_bystep_adventure(id_aventura):
    """
    Diccionario con repsuestas detallas.
    """

    import game_logic.engine as engine

    idAnswers_ByStep_Adventure = {}

    # Query que une opcioness con sus preguntas filtrando por la aventura elegida.
    query = "SELECT o.id_opcion, o.id_pregunta_base, o.texto, o.id_pregunta_siguiente, "
    query += "o.id_personaje_especifico, o.probabilidad_base, o.probabilidad_fuera_clase, "
    query += "p.texto "
    query += "FROM opcion o "
    query += "JOIN pregunta p ON o.id_pregunta_base = p.id_pregunta "

    datos = engine.get_table(query)

    for i in range(1, len(datos)):
        id_opc = datos[i][0]
        id_pregunta_base = datos[i][1]
        clave = (id_opc, id_pregunta_base)

        idAnswers_ByStep_Adventure[clave] = {
            "Description": datos[i][7],
            "Resolution_Answer": datos[i][2],
            "NextStep_Adventure": datos[i][3],
            "pj_req": datos[i][4],
            "p_base": datos[i][5],
            "p_fuera": datos[i][6]
        }

    return idAnswers_ByStep_Adventure

def playStep(id_pregunta, id_juego_actual, id_aventura, id_personaje, id_user):
    """
    Muestra el paso actual, sus 5 opciones y gestiona la progresión o muerte.
    """

    import game_logic.engine as engine
    import game_logic.engine_game as engine_game

    paso = get_id_bystep_adventure(id_aventura)
    respuestas = get_answers_bystep_adventure(id_aventura)

    query_nom = "SELECT nombre FROM aventura WHERE id_aventura = {}".format(id_aventura)
    respuesta_nom = engine.get_table(query_nom)

    nombre_aventura = respuesta_nom[1][0]
    engine.getHeader(nombre_aventura)

    texto_paso = paso[id_pregunta]["Description"]
    print("\n" + texto_paso + "\nOptions:\n")

    es_paso_final = paso[id_pregunta]["Final_Step"]
    if es_paso_final == 1:
        print("FIN")
        insertCurrentChoice(id_juego_actual, id_aventura, id_pregunta, 0, id_user, 1)
        return 0

    ids_disponibles = paso[id_pregunta]["answers_in_step"]
    opciones = []
    texto_opciones = ""
    opciones_validas = []
    
    for i in range(len(ids_disponibles)):
        id_opciones = ids_disponibles[i]
        clave = (id_opciones, id_pregunta)

        if clave in respuestas:
            datos_respuestas = respuestas[clave]

            num = len(opciones) + 1
            texto_opciones += engine_game.getFormatedAnswers(num, datos_respuestas["Resolution_Answer"], 60, 3) + "\n"
            opciones.append(id_opciones)
            opciones_validas.append(num)

    num_salir = len(opciones) + 1
    texto_opciones += "{})    Save & Exit to Menu".format(num_salir)
    opciones_validas.append(num)

    eleccion = engine.getOpt(texto_opciones, "Select Option: ", opciones_validas)

    if eleccion == num:
        return -1

    id_opcion_elegida = opciones[eleccion - 1]
    datos_opciones = respuestas[(id_opcion_elegida, id_pregunta)]

    insertCurrentChoice(id_juego_actual, id_aventura, id_pregunta, id_opcion_elegida, id_user, 0)
    
    pj_espefico = datos_opciones["pj_req"]

    if str(pj_espefico).isdigit():
        pj_espefico = int(pj_espefico)

        if pj_espefico > 0:
            probabilidad = datos_opciones["p_fuera"]

            if pj_espefico == int(id_personaje):
                probabilidad = datos_opciones["p_base"]
            
            tirada = random.randint(1, 100)
            if tirada > probabilidad:
                print("Muerte")
                insertCurrentChoice(id_juego_actual, id_aventura, id_pregunta, id_opcion_elegida, id_user, -1)
                return 0
    
    siguiente_paso = datos_opciones["NextStep_Adventure"]

    return siguiente_paso

def get_first_step_adventure(id_aventura, id_juego, id_personaje, user_session):
    """
    Enceuntra el primer paso y ejecuta el bucle del juego.
    """

    import game_logic.engine as engine

    id_user = engine.getUserIdBySession(user_session)

    query = "SELECT id_pregunta FROM pregunta_aventura WHERE id_aventura = {} LIMIT 1".format(id_aventura)
    datos = engine.get_table(query)

    id_actual = 0
    if len(datos) > 1:
        id_actual = datos[1][0]
    
    if id_actual == 0:
        return 0

    while id_actual != 0 and id_actual != -1:
        id_actual = playStep(id_actual, id_juego, id_aventura, id_personaje, id_user)
        input("\n\nEnter to continue... ")
        print("\n" * 3)

    return 1

def replay(choices):
    """
    Reproduce una aventura paso a paso basándose en una tupla.
    """

    import game_logic.engine as engine

    id_paso = choices[0][0]
    id_opcion = choices[0][1]

    query = "SELECT id_juego, id_aventura, id_personaje, id_usuario "
    query += "FROM paso "
    query += "WHERE id_paso = {} ADN id_opcion {} LIMIT 1 ".format(id_paso, id_opcion)

    info = engine.get_table(query, id_paso, id_opcion)

    id_juego = info[1][0]
    id_aventura = info[1][1]
    id_personaje = info[1][2]
    id_user = info[1][3]

    pasos = get_id_bystep_adventure(id_aventura)
    respuestas = get_answers_bystep_adventure(id_aventura)

    id_actual = 0

    for registro in choices:
        id_paso = registro[0]
        id_opcion = registro[1]

        texto_paso = pasos[id_paso]["Description"]
        clave = (id_opcion, id_paso)
        texto_opcion = respuestas[clave]["Resolution_Answer"]

        datos_opciones = respuestas[(id_opcion, id_paso)]
        id_actual = datos_opciones["NextStep_Adventure"]
        
        input("\nEnter to continue history...")

    while id_actual != 0 and id_actual != -1:
        id_actual = playStep(id_actual, id_juego, id_aventura, id_personaje, id_user)
        input("\n\nEnter to continue... ")
        print("\n" * 3) 