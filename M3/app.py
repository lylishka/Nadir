from game_logic.engine import *
from game_logic.engine_game import *
from game_logic.narrative import *

# FLAGS
salir = False            # EXIT
flg_00 = True            # MENU DE INICIO (NO LOGUEADO)
flg_01 = False           # MENU DE USUARIO (LOGUEADO)
user_session = ""        # EL USUARIO ACTUAL

while not salir:

    # MENU 00: ACCESO Y REGISTRO
    while flg_00:
        mostrar_logo()

        diccionario_opciones = {"l": 1, "e": 4}
        excepciones = ["l", "e", "-1"]

        # Opcion del menu principal
        opc = getOpt(menu00, "Option: ", [1,2,3,4], diccionario_opciones, excepciones)
            
            
        # LOGIN
        if opc == 1:
            login = False
            while not login:
                print("\n" * 6 + ">> SISTEMA NADIR [Modulo: Seguridad/Acceso]".center(ancho))
                print("-" * ancho)
                print("(Escribe 'exit' para cancelar)".center(ancho))
                print("\n    Iniciando secuencia de identificacion...")

                username = input("    Username: ")
                
                if username.lower() == "exit":
                    login = True
                    break

                password = input("    Password: ")

                resultado = checkUserbdd(username, password)

                if resultado == 1:
                    user_session = username

                    flg_00 = False
                    login = True
                    flg_01 = True
                elif resultado == 0:
                    print("    [!] User does not exist.")
                    input("    Enter to continue")
                else:
                    print("    [!] Incorrect password.")
                    input("    Enter to continue")

                print("-" * ancho)

        # CREATE USER
        elif opc == 2:
            registro = False

            while not registro:
                print("\n" * 6 + ">> SISTEMA NADIR [Modulo: Gestion/Registro]".center(ancho))
                print("-" * ancho)
                print("(Escribe 'exit' para cancelar)".center(ancho))
                print("\n    Registrando nueva cuenta de usuario...")

                username = input("    Username: ")

                if username.lower() == "exit":
                    registro = True
                    break

                if checkUser(username):
                    if userExits(username):
                        print("    [!] There is already a user named {}".format(username))
                        input("    Enter to continue")
                    else:
                        registro = True
            
            if registro:
                password_valida = False

                while not password_valida:
                    password = input("    Password: ")
                    if checkPassword(password):
                        if createUserBD(username, password):
                            print("    [OK] User created succesfully! Loggin in...")
                            user_session = username
                            flg_00 = False
                            flg_01 = True
                            password_valida = True
                            input("    Enter to continue")
                    else:
                        input("    Enter to continue")

        # EXIT
        elif opc == 4:
            flg_00 = False
            salir = True
    
    # MENU 01: JUEGO (SESION INICIADA)
    while flg_01:
        mostrar_logo()  
        print((">> SESION INICIADA: {}".format(user_session)).center(ancho))
        print("-" * ancho)

        diccionario_opciones = {"l": 1, "p": 2, "e": 5}
        excepciones = ["l", "p", "e", "-1"]

        opc = getOpt(menu01, "Option: ", [1,2,3,4,5], diccionario_opciones, excepciones)

        # LOGOUT
        if opc == 1: 
            flg_01 = False
            flg_00 = True
            user_session = ""

        # PLAY
        if opc == 2:
            adventures = get_adventures_with_chars()
            print(getFormatedAdventures(adventures))

            opc_adv = getOpt("", "Select Adventure ID (or 0 to go back): ", list(adventures.keys()), {}, ["0"])

            if opc_adv != 0:
                aventura_elegida = opc_adv

                nombre_aventura = adventures[opc_adv]["Name"]

                todos_personajes = get_characters()

                ids_filtrados = adventures[opc_adv]["characters"]
                personajes_tabla = {}
                
                for id_character in ids_filtrados:
                    personajes_tabla[id_character] = todos_personajes[id_character]

                print(getFormatedCharacters(personajes_tabla, nombre_aventura))

                character = get_characters
                
                opc_pj = getOpt("", "Select Characters ID (or 0 to go back): ", list(character.keys()), {}, ["0"])

                if opc_pj != 0:
                    personaje_elegido = opc_pj

                    id_juego_actual = setIdGame()

                    get_first_step_adventure()

                    
            else:
                flg_01 = False
                flg_00 = True
        # EXIT
        if opc == 5:
            flg_01 = False
            salir = True