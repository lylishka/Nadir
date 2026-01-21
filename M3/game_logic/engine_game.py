from game_logic.engine import *
from game_logic.narrative import get_id_bystep_adventure, get_answers_bystep_adventure

def get_adventures_with_chars():
    """
    Devuelve un diccionario con ID, Nombre de cada aventura y la ID de los Personajes de cada aventura.
    """

    cursor = conexion.cursor()
    query = "SELECT id_aventura, nombre, descripcion FROM aventura"
    cursor.execute(query)

    aventures = {}
    for fila in cursor:
        id_aventura = fila[0]
        aventures[id_aventura] = {
            "Name": fila[1], 
            "Description": fila[2], 
            "characters": []}

    cursor.close()

    cursor_chars = conexion.cursor()
    query_characters = "SELECT id_personaje, id_aventura FROM personaje_aventura"
    cursor_chars.execute(query_characters)

    for fila_pa in cursor_chars:
        id_personaje_pa = fila_pa[0]
        id_aventura_pa = fila_pa[1]

        if id_aventura_pa in aventures:
            aventures[id_aventura_pa]["characters"].append(id_personaje_pa)
        
    cursor_chars.close()

    return aventures

def get_characters():
    """
    Devuelve un diccionario con ID i Nombre de cada personaje.
    """

    cursor = conexion.cursor()
    query = "SELECT id_personaje, nombre FROM personaje"
    cursor.execute(query)

    characters = {}
    for fila in cursor:
        characters[fila[0]] = fila[1]

    cursor.close

    return characters

def getFormatedAdventures(adventures):
    """
    Le damos el diccionario de adventures i devuelve el encavezado y las ids, titulos y descripción de cada aventura.
    """

    nombre_cols = ("ID Adventure", "Adventure", "Description")
    medidas_cols = (15, 25, 50)
    margen_comun = 2

    resultado = "\n" * 5 + getHeadeForTableFromTuples(nombre_cols, medidas_cols, "Adventures")

    for id_adventure in adventures:

        textos = (str(id_adventure)), adventures[id_adventure]["Name"], adventures[id_adventure]["Description"]

        fila_formateada = getFormatedBodyColumns(textos, medidas_cols, margen_comun)

        resultado += "\n" + fila_formateada
    
    return resultado
   
def getFormatedCharacters(characters, adventure_game):
    """
    Le damos el diccionario de characters i devuelve el encavezado y las ids, titulos y descripción de cada aventura.
    """

    nombre_cols = ("ID Character", "Name", "Description")
    medidas_cols = (15, 25, 55)
    margen_comun = 2

    titulo ="Characters from {}".format(adventure_game)
    resultado = "\n" * 5 + getHeadeForTableFromTuples(nombre_cols, medidas_cols, titulo)

    for id_personaje in characters:
        cursor = conexion.cursor()
        query = "SELECT descripcion FROM personaje WHERE id_personaje = %s"
        cursor.execute(query, (id_personaje,))

        for fila in cursor:
            descripcion = fila[0]
        
        nombre_personaje = characters[id_personaje]

        textos = (str(id_personaje), nombre_personaje, descripcion) 
        fila_formateada = getFormatedBodyColumns(textos, medidas_cols, margen_comun)

        resultado += "\n" + fila_formateada
        cursor.close()
    
    return resultado
   
def getIdGames():
    """
    Devuelve una tupla con todos los id_juegos que existen en la tabla juego.
    """

    lista_ids = ()

    cursor = conexion.cursor()
    query = "SELECT id_juego FROM juego"
    cursor.execute(query)

    for fila in cursor:
        id_actual = fila[0]
        lista_ids += (id_actual,)
    
    cursor.close()

    return lista_ids

def getNextGameId():
    """
    Calcula el ID más alto existente y le suma 1.
    """

    ids_existentes = getIdGames

    max_id = 0

    for id_juego in ids_existentes:
        if id_juego > max_id:
            max_id = id_juego
    
    proximo_id = max_id + 1
    return proximo_id

def insertCurrentGame(idGame, idUser, idChar, idAdventure):
    """
    Inserta un nuevo registro de juego a la base de datos.
    """

    cursor = conexion.cursor()

    query = "INSERT INTO juego (id_juego, id_aventura, id_personaje, id_usuario) VALUES (%s, %s, %s, %s)"
    datos = (idGame, idAdventure, idChar, idUser)

    cursor.execute(query, datos)
    conexion.commit()
    cursor.close()

def setIdGame():
    """
    Cordinar la busqueda de IDs y la insercion del nuevo juego.
    """

    from app import user_session, aventura_elegida, personaje_elegido

    ids_existentes = getIdGames()
    
    maximo = 0

    for i in ids_existentes:
        if i > maximo:
            maximo = i
    nueva_id = maximo + 1

    id_user = getUserIdBySession(user_session)

    insertCurrentGame(nueva_id, id_user, personaje_elegido, aventura_elegida)

def getFormatedAnswers(idAnswer, text, lenLine, leftMargin):
    """
    Formatea el texto de una respuesta con un margen izquierdo.
    """

    texto = formatText(text, lenLine, "\n")

    margen = " " * leftMargin
    resultado = margen + text.replace("\n", "\n" + margen)

    resultado_final = "{}) {}".format(idAnswer, resultado)

    return resultado_final

def replay(choices):
    """
    Reproduce una aventura paso a paso basándose en una tupla.
    """

    from app import aventura_elegida

    dic_pasos = get_id_bystep_adventure()
    dic_respuestas = get_answers_bystep_adventure()

    for paso in choices:
        id_paso = paso[0]
        id_opcion_elegida = paso[1]

        id_pregunta = 0
        for id_p in dic_pasos:
            if dic_pasos[id_p]["id_paso"] == id_paso:
                id_pregunta = id_p
        
        getHeader(aventura_elegida)

        paso = dic_pasos[id_pregunta]
        descripcion_paso = paso["Description"]
        print("\n" + descripcion_paso.center(ancho))

        respuesta = dic_respuestas[(id_opcion_elegida, id_pregunta)]
        respuesta_final = respuesta["Description"]
        print("\n" + getFormatedAnswers(id_opcion_elegida, respuesta_final, 60, 5))
        
        input("\n[ Enter to Continue... ]")

def getReplayAdventures():
    """
    Consulta el historial de partidas del usuario actual y devuelve un diccionario de las partidas jugadas.
    """

    from app import user_session

    id_user = getUserIdBySession(user_session)

    replayAdventures = {}
    cursor = conexion.cursor()

    query = "SELECT j.id_juego, j.id_usuario, u.username, "
    query += "j.id_aventura, a.nombre, j.id_personaje, p.nombre "
    query += "FROM juego j "
    query += "JOIN usuario u ON j.id_usuario = u.id_usuario "
    query += "JOIN aventura a ON j.id_aventura = a.id_aventura "
    query += "JOIN personaje p ON j.id_persoanje = p.id_personaje "
    query += "WHERE j.id_usuario = " + str(id_user)

    cursor.execute(query)

    for fila in cursor:
        replayAdventures[fila[0]] = {
            "idUser": fila[1],
            "Username": fila[2],
            "idAventure": fila[3],
            "Name": fila[4],
            "idCharacter": fila[5],
            "CharacterName": fila[6]
        }
    
    cursor.close()

    return  replayAdventures