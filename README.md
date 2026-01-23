# Nadir

**Nadir** es un juego de rol narrativo para terminal desarrollado en **Pyhton**. El proyecto combina una narrativa ramificada con una infraestructura que incluye una **base de datos MySQL** remota y una **interfaz web** para la gestión ded datos.

---

## 📝 Descripción del Proyecto

En Nadir, las decisiones del jugador dan forma a la historia. El juego utiliza un sistema de **probabilidades**, aunque todos los personajes pueden intentar las mismas acciones, sus especiales determinarán si es segura o mortal.

El proyecto se divide en dos experiencias narrativas:

### 🎭 Historia 1: Curtain Call: Zero
Una aventura de terro surrealista ambientada en un teatro infinito. Un viaje psicológico basado en la identidad, la percepción de la realidad y la gestión de la cordura.
* **El Actor**: Especialista en interacción social, interpretación y engaño.
* **La Violinista**: Especialista en sigilo y resolución de puzzles sonoros.
* **El Escenógrafo**: Especialista en manipulación el entorno y mecanismos físicos.

### 🚀 Historia 2: Protocolo Epsilon
Una aventura de ciencia ficción ambientada en una nave espacial. La trama gira en torno a la supervivencia técnica y la creciente desconfianza hacia la inteligencia artificial de a bordo.
* **Ingeniero**: Especialista técnico con alto éxito en reparaciones y sistemas.
* **Médico**: Especialista biológico experto en análisis y curación.
* **Soldado**: Especialista en combate, seguridad y situaciones de fuerza.

---

## 🛠️ Instalación y Configuración

Todos los archivos necesarios para la configuración se encuentran en la carpeta **`M1`** de este repositorio.

### Paso 0: Preparación deel Entorno
Antes de empezar con los puntos principales, debes preparar tu sistema:

1. **Si usas Windows**: Descarga e instala **"Ubuntu"** desde la Microsoft Store.
   * Abre la terminal de Ubuntu y asegúrate de estar en el directorio home del usuario.
2. **Si usuas Linux/macOS**: Abre tu terminal y sitúate en tu carpeta personal.
3. **Mover archivos**: Copia el contenido de la carpeta **`M1`** del repositorio en el **home (`$HOME`)** de tu usuario.

### Paso 1: Configuración de Seguridad RSA
El accesso al servidor se realiza mediante claves públicas.
1. **Generar la clave localmente**:

   ```bash
   ssh-keygen -t rsa
   ```

2. **Configurar permisos**:

   ```bash
   chmod 600 $HOME/.ssh/id_rsa
   ```

3. **Vincular con el serivdor**: Entra en https://kamehouse.ieti.site con tu cuenta de **"@iesesteveterradas.cat"**  y añade la clave pública que  obtenrás con este comando:

   ```bash
   cat $HOME/.ssh/id_rsa.pub
   ```
    **Recuerda el nombre que le pongas a la clave, ya que será tu usuario de conexión.**

### Paso 2: Configuración del Archivo de Entorno
Localiza ek archivo **`proxmox/config.env`** y editalo con tus credenciales:

   ```bash
   # El DEFUALT_USER es el nombre de la clave en Kamehouse
   DEFAULT_USER="nombre_de_tu_clave"
   DEFAULT_RSA_PATH="$HOME/.ssh/id_rsa"
   DEFAULT_SERVER_PORT="3000"
   ```

### PASO 3: Conexión e Instalación de la Base de Datos
**Importante**: Si estás en Windows, dentro de la terminal de Linux debes ejecutar estos comandos para dar permisos y corregir el formato de los archivos antes de conectar:
   ```bash
   cd ~/nodejs_server/proxmox/
   chmod +x *.sh
   dos2unix *.sh
   dos2unix *.env
   ```

   Para configurar el servidor:
   ```bash
   # Opción A: Coonexión manual
   ssh -p 20127 nombre_de_tu_clave@ieticloudpro.ieti.cat

   # Opción B: Uso del script
   cd ~/nodejs_server/proxmox/
    ./proxmoxConnect.sh
   ```

Una vez dentro del servidor remoto, instala y configura MySQL:
   
   ```bash
   sudo apt update
   sudo apt install mysql-server

   # Configuración del usuario:
   sudo mysql
   CREATE USER 'nombre_usuario'@'localhost' INDETIFIED WITH caching_sha2_password BY 'tu_contraseña';
   GRANT ALL PRIVILEGES ON *.* TO 'nombre_usuario'@'localhost' WITH GRANT OPTION;
   FLUSH PRIVILEGES
   quit
   ```

---

## 🎮 Utilización del proyecto

### Gestión del Túnel de Datos
Para comunicar el juego con la base de datos remota, abre el túnel.
Primero accede a la carpeta y luego ejecuta los comandos seguún necesites:

   ```bash
   cd ~/nodejs_server/proxmox/

   # Iniciar el túnel
   ./proxmoxTunelStart.sh

   # Comprobar el estado del túnel
   ./proxmoxTunelStatus.sh

   # Detener el túnel
   ./proxmoxTunelStop.sh
   ```

### Conexión a la Base de Datos Remota
Con el túnel **funcionando**, puedes conectar con la base de datosde dos maneras:
1. **Via Terminal**:

   ```bash
   mysql -h 127.0.0.1 -P 3307 -u nombre_usuario -p
   # Se solicitará la contraseña del usuario. Escribe 'quit' para salir.
   ```

2. **Via Herramienta Grñafica (MySQL Workbench, etc.)**:
* **Host**: `127.0.0.1`
* **Puerto**: `3307`
* **Usuario**: `nombre_usuario`
* **Contraseña**: `tu_contraseña`

### Ejecución del Juego
El código principal del juego se ecnuentra en la carpeta `M3` del repositorio. Para iniciarlo, ejecuta el archivo `app.py`:

   ```bash
   python3 ~/ruta_al_archivo/M3/app.py
   ```

---

## 📧 Contacto de los autores
* [drioscruz.25cf@iesesteveterradas.cat](mailto:drioscruz.25cf@iesesteveterradas.cat)
* [frodriguezgaleas01.cf@iesesteveterradas.cat](mailto:frodriguezgaleas01.cf@iesesteveterradas.cat)
* [promeroramos.25cf@iesesteveterradas.cat](mailto:promeroramos.25cf@iesesteveterradas.cat)
