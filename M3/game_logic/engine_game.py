from game_logic.engine import conexion

def get_adventures_with_chars():
    """
    Devuelve un diccionario con ID i Nombre de cada aventura.
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

    print(aventures)
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

    print(characters)
    return characters