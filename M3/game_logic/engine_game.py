from game_logic.engine import *

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
   
