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

        diccionario_opciones = {"l": 1, "e": 5}
        excepciones = ["l", "e", "-1"]

        # Opcion del menu principal
        opc = getOpt(menu00, "Option: ", [1,2,3,4,5], diccionario_opciones, excepciones)
            
            
        # LOGIN
        if opc == 1:
            login = False
            while not login:
                username = input("Username: ")
                password = input("Password: ")

                resultado = checkUserbdd(username, password)

                if resultado == 1:
                    user_session = username

                    flg_00 = False
                    login = True
                    flg_01 = True
                elif resultado == 0:
                    print("[!] User does not exist.")
                    input("Enter to continue")
                else:
                    print("[!] Incorrect password.")
                    input("Enter to continue")

        # CREATE USER
        elif opc == 2:
            user_valido = False

            while not user_valido:
                username = input("Username: ")

                if checkUser(username):
                    if userExits(username):
                        print("[!] There is already a user named {}".format(username))
                        input("Enter to continue")
                    else:
                        user_valido = True
            
            if user_valido:
                password_valida = False

                while not password_valida:
                    password = input("Password: ")
                    if checkPassword(password):
                        if createUserBD(username, password):
                            print("User created succesfully! Loggin in...")
                            user_session = username
                            flg_00 = False
                            flg_01 = True
                            password_valida = True
                            input("Enter to continue")
                    else:
                        input("Enter to continue")

        # EXIT
        elif opc == 5:
            flg_00 = False
            salir = True
    
    # MENU 01: JUEGO (SESION INICIADA)
    while flg_01:
        mostrar_logo()
        print(("User: {}".format(user_session)).center(ancho))

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
            print("Play")
        
        # EXIT
        if opc == 5:
            flg_01 = False
            salir = True