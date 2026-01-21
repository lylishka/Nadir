from app import user_session
import mysql.connector
# python -m pip install mysql-connector-python

# CONFIGURACION GLOBAL
ancho = 100


# INTERFAZ Y MENUS

def mostrar_logo():
    """
    Imprime el logo 'NADIR' centrado en la pantalla utilizando
    el ancho global definido para la interfaz.
    """

    nadir = [
        " ___   __    ________   ______    ________  ______       ",
        "/__/\\ /__/\\ /_______/\\ /_____/\\  /_______/\\/_____/\\      ",
        "\\::\\_\\\\  \\ \\\\::: _  \\ \\\\:::_ \\ \\ \\__.::._\\/\\:::_ \\ \\     ",
        " \\:. `-\\  \\ \\\\::(_)  \\ \\\\:\\ \\ \\ \\   \\::\\ \\  \\:(_) ) )_   ",
        "  \\:. _    \\ \\\\:: __  \\ \\\\:\\ \\ \\ \\  _\\::\\ \\__\\: __ `\\ \\  ",
        "   \\. \\`-\\  \\ \\\\:.\\ \\  \\ \\\\:\\/.:| |/__\\::\\__/\\\\ \\ `\\ \\ \\ ",
        "   \\__\\/ \\__\\/ \\__\\/\\__\\/ \\____/_/\\________\\/ \\_\\/ \\_\\/"
    ]

    print(("\n" * 6) + ("*" * ancho))

    for linea in nadir:
        print(linea.center(ancho))

    print("\n" + ("*" * ancho))

# Textos de los menus
menu00 = "\n1)Login\n2)Create User\n3)Reports\n4)Exit"
menu01 = "\n1)Logout\n2)Play\n3)Replay Adventure\n4)Reports\n5)Exit"

# CREADOR DE MENUS
def getOpt(textOpts= "", inputOptText= "", rangeList= [], dictionary= {}, exceptions= []):
    """
    Gestiona la entrada: centra el menú, valida que la opción esté dentro del rango permitido
    o sea una excepcion o atajos (diccionario).
    """

    largo = 0
    linea_actual = 0

    if textOpts == "":
        margen = 0
    else:
        # Calculo para centrar el menu
        for opcion in textOpts:
            if opcion == "\n":
                if linea_actual > largo:
                    largo = linea_actual
                linea_actual = 0
            else:
                linea_actual += 1
        if linea_actual > largo:
            largo = linea_actual

        margen = (ancho - largo) // 2
    espacio = " " * margen

    menu_centrado = espacio + textOpts.replace("\n", "\n" + espacio)

    while True:
        print("\n" + menu_centrado + "\n")
        opc = input(espacio + inputOptText)

        valida = False
        
        try:
            # Validacion numerica
            if opc.isdigit():
                opc_num = int(opc)
                if opc_num in rangeList:
                   valida = True
                   resultado = opc_num
        except ValueError:
            print("\n")

        # Validacion de atajos (diccionario) o excepciones
        if opc in dictionary:
            valida = True
            resultado = dictionary[opc]
        
        if not valida:
            for ex in exceptions:
                if str(ex) == opc:
                    valida = True
                    resultado = opc
        
        if valida:
            return resultado

        else:
            print(espacio + "[!] Option doesn't exist.")
            input(espacio + "Enter to Continue")

def getHeader(text):
    """
    Devuelve una cabecera con el texto centrado entre decoraciones.
    """

    linea_ast = "*" * ancho

    linea_igual = (ancho - len(text)) // 2

    linea_central = "=" * linea_igual + text + "=" * (ancho - linea_igual - len(text))

    header = ("{}\n{}\n{}".format(linea_ast, linea_central, linea_ast))

    print(header)

def formatText(text,lenLine,split):
    text_format = ""
    linia_actual = ""
    palabra_actual = ""

    text = text + " "

    for palabra in range(len(text)):
        caracter = text[palabra]

        if caracter != " ":
            palabra_actual += caracter
        else:
            if palabra_actual != "":
                longitud_afegim = len(palabra_actual)
                if linia_actual != "":
                    longitud_afegim += 1
                longitud_afegim += len(palabra_actual)

                if len(linia_actual) + longitud_afegim <= lenLine:
                    if linia_actual == "":
                        linia_actual = palabra_actual
                    else:
                        linia_actual += " " + palabra_actual
                else:
                    if text_format == "":
                        text_format = linia_actual
                    else:
                        text_format += split + linia_actual
                    linia_actual = palabra_actual  
                
                palabra_actual = ""            
    
    if linia_actual != "":
        if text_format == "":
            text_format = linia_actual
        else:
            text_format += split + linia_actual
    return text_format

def getHeadeForTableFromTuples(t_name_columns,t_size_columns,title=""):
    ancho_total = 0
    margen = 2
    for medida in t_size_columns:
        ancho_total += medida
    
    ancho_total += (len(t_name_columns) - 1) * 2

    if title != "":
        libre = ancho_total -len(title)
        lado = libre // 2

        resto_iguales = lado * "="
        linia_iguals = resto_iguales + title + resto_iguales
    else:
        linia_iguals = "=" * ancho_total
    

    linea_estrellas = "*" * ancho_total

    columnas = ""
    for i in range(len(t_name_columns)):
        nombre = t_name_columns[i]

        while len(nombre) < t_size_columns[i]:
            nombre += " "
        
        if columnas == "":
            columnas = nombre
        else:
            for j in range(margen):
                columnas += " "
            columnas += nombre
    

    resultado = linia_iguals + "\n" + columnas + "\n" + linea_estrellas

    return resultado

def getFormatedBodyColumns(tupla_texts,tupla_sizes,margin=0):
    columnas = []
    longitud = 0

    for i in range(len(tupla_texts)):
        columna = formatText(tupla_texts[i], tupla_sizes[i], "\n")
        
        if columna != "":
            columna += "\n"
        
        linias = []
        temp = ""
        for caracter in columna:
            if caracter != "\n":
                temp += caracter
            else:
                linias.append(temp)
                temp = ""

        columnas.append(linias)
        if len(linias) > longitud:
            longitud = len(linias)
    
    resultado = ""
    for i in range(longitud):
        fila = ""
        for j in range(len(columnas)):
            if i < len(columnas[j]):
                text_linia = columnas[j][i]
            else:
                text_linia = ""
            
            while len(text_linia) < tupla_sizes[j]:
                text_linia += " "
            
            if j < len(columnas) - 1:
                for n in range(margin):
                    text_linia += " "
            
            fila += text_linia
        
        if resultado == "":
            resultado = fila
        else:
            resultado += "\n" + fila
    
    return resultado

# def getFormatedTable(queryTable,title=""):

# CONEXIÓN A LA BASE DE DATOS

def conectar_db():
    """
    Establece conexion con la base de datos.
    """
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            port=3307,
            user="super",
            password="1234",
            database="nadir"
        )
        return conexion
    except:
        print("[!] Error connecting to the database.")
        input("Enter to Continue")
        return False   

# Validacion Global de Conexion
conexion = conectar_db()

def get_table(query):
    """
    Ejecuta una query y devuelve una tupla de tuplas.
    La tupla[0] contiene los nombres de la columna.
    """
    
    resultado = ()
    cursor = conexion.cursor()
    cursor.execute(query)

    columnas = ()
    descripciones = cursor.description
    indice_col = 0
    limites_cols = len(descripciones)

    while indice_col < limites_cols:
        columna_info = descripciones[indice_col]
        nombre_col = columna_info[0]
        columnas += (nombre_col,)
        indice_col += 1
    
    resultado = (columnas,)

    for fila in cursor:
        resultado += (fila,)
    
    cursor.close()

    return resultado
    
def getUsers():
    """
    Consulta la base de datos y genera un diccionario estructurado:
    {'Username': {'password': 'password_user', 'idUser': 'idUser_user'}}
    """

    usuarios = {}

    if conexion:
        cursor = conexion.cursor()  
        cursor.execute("SELECT id_usuario, username, password FROM usuario")
            
        for fila in cursor:
            usuarios[fila[1]] = {"password": fila[2], "idUser": fila[0]}
            
        cursor.close()
          
    return usuarios

def createUserBD(user, password):
    """
    Inserta un nuevo registro de usuario en la tabla 'usuario'.
    """
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO usuario (username, password) VALUES (%s, %s)"
        cursor.execute(sql, (user, password))
        conexion.commit()
        cursor.close()

        return True
    
    except:
        return False


# VALIDACIONES

def checkUser(user):
    """
    Valida el formato del nombre de usuario.
    """

    if not (6 <= len(user) <= 10):
        print("[!] The user must be from 6 to 10 characteres.")
        return False

    if not user.isalnum():
        print("[!] The user can only have letters and numbers.")
        return False

    return True

def checkPassword(password):
    """
    Valida la complejidad de la contraseña.
    """

    mayusculas = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "Ñ",
                  "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    minusculas = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "ñ",
                  "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    especiales = ["!", "@", "#", "$", "%", "&", "/", "(", ")", "=", "?", "¿",
                             "'", "!", "¡", "^", "`", "´", "*", "[", "]", "{", "}", ",", 
                             ";", ":", ".", "_", "-", "~", "€", "¬", "\\", "+"]
    num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    if not (8 <= len(password) <= 12):
          print("[!] The password must be from 8 to 12 characteres.")
          return False
    
    tiene_espacios = False
    tiene_mayusculas = 0
    tiene_minusculas = 0
    tiene_nums = 0
    tiene_especiales = 0

    for caracter in password:
        if caracter == " ":
            tiene_espacios = True
            break
        elif caracter in mayusculas:
            tiene_mayusculas += 1
        elif caracter in minusculas:
            tiene_minusculas += 1
        elif caracter in especiales:
            tiene_especiales += 1
        elif caracter in num:
            tiene_nums += 1

    if tiene_espacios == True or tiene_mayusculas == 0 or tiene_minusculas == 0 or tiene_especiales == 0 or tiene_nums == 0:
        print("[!] Incorrect Format. The password must include capital letters, small letters, numbers and symbols. and mustn't contain spaces.")
        return False 

    return True
    
def userExits(user):
    """
    Verifica la existencia de un usuario recoriendo el diccionario de getUsers.
    """

    usuarios = getUsers()
    existe = False
    
    for nombre in usuarios:
        if nombre == user:
            existe = True

    return existe


def checkUserbdd(user, password):
    """
    Valida credenciales para el login.
    """

    usuarios = getUsers()

    if user not in usuarios:
        return 0
    
    if usuarios[user]["password"] == password:
        return 1
    else:
        return -1

def getUsersIds():
    """
    Genera una estructura de listas separados por nombres e IDs.
    """

    usuarios = getUsers()
    nombres = []
    ids = []

    for nombre in usuarios:
        datos = usuarios[nombre]
        nombres.append(nombre)
        ids.append(datos["idUser"])
    
    resultado = [nombres, ids]

    return resultado

def getUserIdBySession(user):
    """
    Busca el id_usuario correspondiente al username utilizando getUsersIds.
    """

    lista_ids = getUsersIds()
    nombres = lista_ids[0]
    ids = lista_ids[1]

    id_encontrado = 0
    i = 0
    limite = len(nombres)

    while i < limite:
        if nombres[i] == user_session:
            id_encontrado = ids[i]
        
        i += 1
    
    return id_encontrado

