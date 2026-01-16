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
def getOpt(textOpts = "", inputOptText = "", rangeList = [], dictionary = {}, exceptions = []):
    """
    Gestiona la entrada: centra el menú, valida que la opción esté dentro del rango permitido
    o sea una excepcion o atajos (diccionario).
    """

    largo = 0
    linea_actual = 0

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


# CONEXIÓN A LA BASE DE DATOS

def conectar_db():
    """
    Establece conexion con la base de datos.
    """
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="developer",
            password="P@ssw0rd",
            database="nadir"
        )
        return conexion
    except:
        print("[!] Error connecting to the database.")
        input("Enter to Continue")
        return False   

# Validacion Global de Conexion
conexion = conectar_db()

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