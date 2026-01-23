# FLAGS
salir = False            # EXIT
flg_00 = True            # MENU DE INICIO (NO LOGUEADO)
flg_01 = False           # MENU DE USUARIO (LOGUEADO)
flg_02 = False           # MENU DE REPORTS
user_session = ""        # EL USUARIO ACTUAL
personaje_elegido = 0    # PERSONAJE ELEGIDO
id_juego_actual = 0      # ID JUEGO ACTUAL



while not salir:

    # MENU 00: ACCESO Y REGISTRO
    while flg_00:
        import game_logic.engine as engine

        engine.mostrar_logo()

        diccionario_opciones = {"l": 1, "e": 4}
        excepciones = ["l", "e", "-1"]

        # Opcion del menu principal
        opc = engine.getOpt(engine.menu00, "Option: ", [1,2,3,4], diccionario_opciones, excepciones)
            
            
        # LOGIN
        if opc == 1:
            login = False
            while not login:
                print("\n" * 6 + ">> SISTEMA NADIR [Modulo: Seguridad/Acceso]".center(engine.ancho))
                print("-" * engine.ancho)
                print("(Escribe 'exit' para cancelar)".center(engine.ancho))
                print("\n    Iniciando secuencia de identificacion...")

                username = input("    Username: ")
                if username.lower() == "exit":
                    break

                password = input("    Password: ")
                if password.lower() == "exit":
                    break

                resultado = engine.checkUserbdd(username, password)

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

                print("-" * engine.ancho)

        # CREATE USER
        elif opc == 2:
            registro = False

            while not registro:
                print("\n" * 6 + ">> SISTEMA NADIR [Modulo: Gestion/Registro]".center(engine.ancho))
                print("-" * engine.ancho)
                print("(Escribe 'exit' para cancelar)".center(engine.ancho))
                print("\n    Registrando nueva cuenta de usuario...")

                username = input("    Username: ")
                if username.lower() == "exit":
                    break

                if engine.checkUser(username):
                    if engine.userExits(username):
                        print("    [!] There is already a user named {}".format(username))
                        input("    Enter to continue")
                    else:
                        password_valida = False
                        while not password_valida:
                            password = input("    Password: ")

                            if password.lower() == "exit":
                                registro = True
                                break

                            if engine.checkPassword(password):
                                if engine.createUserBD(username, password):
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
        import game_logic.engine as engine

        engine.mostrar_logo()  
        print((">> SESION INICIADA: {}".format(user_session)).center(engine.ancho))
        print("-" * engine.ancho)

        diccionario_opciones = {"l": 1, "p": 2, "e": 5}
        excepciones = ["l", "p", "e", "-1"]

        opc = engine.getOpt(engine.menu01, "Option: ", [1,2,3,4,5], diccionario_opciones, excepciones)

        # LOGOUT
        if opc == 1: 
            flg_01 = False
            flg_00 = True
            user_session = ""

        # PLAY
        elif opc == 2:
            import game_logic.engine_game as engine_game, game_logic.engine as engine

            adventures = engine_game.get_adventures_with_chars()
            print(engine_game.getFormatedAdventures(adventures))

            opc_adv = engine.getOpt("", "Select Adventure ID (or 0 to go back): ", list(adventures.keys()), {}, ["0"])

            if opc_adv != 0:
                
                nombre_aventura = adventures[opc_adv]["Name"]

                todos_personajes = engine_game.get_characters()

                ids_filtrados = adventures[opc_adv]["characters"]
                personajes_tabla = {}
                    
                for id_character in ids_filtrados:
                    personajes_tabla[id_character] = todos_personajes[id_character]

                print(engine_game.getFormatedCharacters(personajes_tabla, nombre_aventura))
                    
                opc_pj = engine.getOpt("", "Select Characters ID (or 0 to go back): ", ids_filtrados, {}, ["0"])

                if opc_pj != 0:
                    import game_logic.narrative as narrative

                    personaje_elegido = opc_pj

                    id_juego_actual = engine_game.setIdGame(opc_adv,personaje_elegido, user_session)
                
                    print("\n" * 3)
                    aventura = narrative.get_first_step_adventure(opc_adv, id_juego_actual, personaje_elegido, user_session)
        
        # REPLAY ADVENTURE
        elif opc == 3:
            import game_logic.narrative as narrative

            query_replay = "SELECT j.id_juego as 'ID GAME', u.username as 'USERNAME', "
            query_replay += "a.nombre as 'ADVENTURE', p.nombre as 'CHARACTER', "
            query_replay += "ps.fecha_hora as 'DATE' "
            query_replay += "FROM juego j "
            query_replay += "JOIN usuario u ON j.id_usuario = u.id_usuario "
            query_replay += "JOIN aventura a ON j.id_aventura = a.id_aventura "
            query_replay += "JOIN personaje p ON j.id_personaje = p.id_personaje "
            query_replay += "JOIN paso ps ON j.id_juego = ps.id_juego "
            query_replay += "WHERE ps.es_final = 0 "

            datos = engine.get_table(query_replay)

            tabla = engine.getFormatedTable(datos, "")
            print("\n" * 3 + tabla)

            id_seleccionada = int(input("\nSelect ID Game to play: "))

            choices = narrative.getChoices(id_seleccionada)
            narrative.replay(choices) 

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
        import game_logic.engine as engine

        texto = "\n1)Most used answer\n2)Player with more games played\n3)Games played by use\n4)Go Back"
        opc = engine.getOpt(texto, "Option: ", [1,2,3,4])
        
        # Most used answer
        if opc == 1:
            query_answer = "SELECT o.texto, COUNT(p.id_opcion) as total "
            query_answer += "FROM paso p JOIN opcion o ON p.id_opcion = o.id_opcion "
            query_answer += "GROUP BY p.id_opcion ORDER BY total DESC LIMIT 1"
            
            datos = engine.get_table(query_answer)
            tabla = engine.getFormatedTable(datos, "Player with more games played")
            
            print("\n" + tabla)
            input("\nEnter to Continue...")
        
        # Player with more games played
        elif opc == 2:
            query_player = "SELECT u.username AS 'PLAYER', "
            query_player += "COUNT(j.id_juego) AS 'TOTAL GAMES' "
            query_player += "FROM usuario u "
            query_player += "JOIN juego j ON u.id_usuario = j.id_usuario "
            query_player += "GROUP BY u.id_usuario "
            query_player += "ORDER BY COUNT(j.id_juego) DESC LIMIT 1 "

            datos = engine.get_table(query_player)
            tabla = engine.getFormatedTable(datos, "TOP PLAYER")
            
            print("\n" + tabla)
            input("\nEnter to Continue...")

        # Games played by user
        elif opc == 3:
            user_select = input("What user do you want to see?\n")

            user_existe = engine.userExits(user_select)

            if user_existe == True:
                id_user_select = engine.getUserIdBySession(user_select)

                query_games = "SELECT j.id_aventura AS 'ID Adventure', "
                query_games += "a.nombre AS 'Name', "
                query_games += "j.fecha_hora AS 'Date' "
                query_games += "FROM juego j "
                query_games += "JOIN aventura a ON j.id_aventura = a.id_aventura "
                query_games += "WHERE j.id_usuario = {}".format(id_user_select)

                datos = engine.get_table(query_games)
                titulo = "Games played by {}".format(user_select)
                tabla = engine.getFormatedTable(datos, titulo)
                
                print("\n" + tabla)
                input("\nEnter to Continue...")

            else:
                print("[!] User not found.")

        # Go Back
        elif opc == 4:
            if user_session == "":
                flg_02 = False
                flg_00 = True
            else:
                flg_02 = False
                flg_01 = True