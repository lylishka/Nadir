from game_logic.engine import *
from game_logic.engine_game import *
from game_logic.narrative import *

# FLAGS
salir = False            # EXIT
flg_00 = True            # MENU DE INICIO (NO LOGUEADO)
flg_01 = False           # MENU DE USUARIO (LOGUEADO)
flg_02 = False           # MENU DE REPORTS
flg_03 = False           # MENU DE PLAY
user_session = ""        # EL USUARIO ACTUAL
aventura_elegida = 0     # AVENTURA ELEGIDA
personaje_elegido = 0    # PERSONAJE ELEGIDO
id_juego_actual = 0      # ID JUEGO ACTUAL



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

        # REPORTS    
        elif opc == 3: 
            flg_00 = False
            flg_02 = True
    
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
        elif opc == 2:
            flg_01 = False
            flg_03 = True
        
        # REPLAY ADVENTURE
        elif opc == 3:
            datos = getReplayAdventures()

            if not datos:
                print("\n" + "[!] No games found to replay.".center(ancho))
                input("Enter to continue...")
            else:
                texto = ("ID", "Username", "Adventure Name", "Character", "Date")
                anchos = (6, 15, 35)
                keys_mostrar = ("Username", "Name", "CharacterName")

                print("\n" * 2)
                cabecera = getHeadeForTableFromTuples(texto, anchos, "YOUR REPLAYS")
                print(cabecera)

                cuerpo = getTableFromDict(keys_mostrar, anchos, datos)
                print(cuerpo)

                ids_validas = list(datos.keys())
                eleccion = getOpt("", "what adventure do you want to repay? (0 Go back): ")

                if eleccion != "0":
                    print("[ Loading Game {}...]".format(eleccion))

        # REPORTS            
        elif opc == 4: 
            flg_01 = False
            flg_02 = True

        # EXIT
        elif opc == 5:
            flg_01 = False
            salir = True
    
    # REPORTS
    while flg_02:
        texto = ("Most used answer", "Player with more games played", "Games played by user", "Go Back")
        opc = getOpt(texto, "Option: ", [1,2,3,4])
        
        # Most used answer
        if opc == 1:
            query_answer = "SELECT o.texto, COUNT(p.id_opcion) as total "
            query_answer += "FROM paso p JOIN opcion o ON p.id_opcion = o.id_opcion "
            query_answer += "GROUP BY p.id_opcion ORDER BY total DESC LIMIT 1"
            
            datos = get_table(query_answer)
            tabla = getFormatedTable(datos, "Player with more games played")
            
            print("\n" + tabla)
            input("\nEnter to Continue...")
        
        # Player with more games played
        elif opc == 2:
            query_player = "SELECT u.username AS 'USERNAME', "
            query_player += "COUNT(j.id_juego) AS 'GAME PLAYED'"
            query_player += "FROM usuario u"
            query_player += "JOIN juego j ON u.id_usuario = j.id_usuario "
            query_player += "GROUP BY u.id_usuario "
            query_player += "ORDER BY COUNT(j.id_juego) DESC "
            query_player += "LIMIT 1"

            datos = get_table(query_player)
            tabla = getFormatedTable(datos, "Player with more games played")
            
            print("\n" + tabla)
            input("\nEnter to Continue...")

        # Games played by user
        elif opc == 3:
            user_select =input("What user do you want to see?\n")

            user_existe = userExits(user_select)

            if userExits == True:
                id_user_select = getUserIdBySession(user_select)

                query_games = "SELECT j.id_aventura AS 'ID Adventure', "
                query_games += "a.nombre AS 'Name', "
                query_games += "j.fecha_hora AS 'Date' "
                query_games += "FROM juego j "
                query_games += "JOIN aventura a ON j.id_aventura = a.id_aventura "
                query_games += "WHERE j.id_usuario = " + str(id_user_select)

                datos = get_table(query_games)
                titulo = "Games played by " + user_select
                tabla = getFormatedTable(datos, titulo)
                
                print("\n" + tabla)
                input("\nEnter to Continue...")

        # Go Back
        elif opc == 4:
            flg_02 = False
            flg_01 = True
    
    # PLAY
    while flg_03:
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
            
            character = get_characters()
                
            opc_pj = getOpt("", "Select Characters ID (or 0 to go back): ", list(character.keys()), {}, ["0"])

            if opc_pj != 0:
                personaje_elegido = opc_pj

                id_juego_actual = setIdGame()
                
                get_first_step_adventure()
    

        flg_03 = False
        flg_01 = True