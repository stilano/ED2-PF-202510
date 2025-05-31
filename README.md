# Proyecto Final ED2: Extracción y Ordenamiento de Ventas

> **Responsable de esta sección**: [Samuel Tilano]  
> Encargado de la conexión a la base de datos MySQL, extracción de datos de la tabla `UN.VENTAS`.

---

## 📋 Contenido

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración de Credenciales](#configuraci%C3%B3n-de-credenciales)

---

## 1. Requisitos Previos

Antes de ejecutar cualquier script de conexión o de exportación, asegúrate de tener lo siguiente instalado y configurado en tu máquina local:

1. **Python 3.10+**  
   - Recomendada la versión 3.10 para compatibilidad con dependencias del proyecto.  
   - Verifica la versión con:
     ```bash
     python --version
     ```

2. **MySQL Server (v8.0+ o compatible)**  
   - Debe existir una base de datos llamada `UN` en tu servidor MySQL.

3. **Credenciales válidas de MySQL**  
   - Necesitarás un usuario y contraseña con permisos de lectura para la base `UN`.  
   - Estas credenciales no deben compartirse públicamente. Se almacenarán en un archivo `.env` (ver sección 2).

4. **Git (recomendado)**  
   - Para clonar el repositorio y administrar ramas.  
   - Verifica la instalación con:
     ```bash
     git --version
     ```

5. **Editor de código / IDE**  
   - VS Code (o tu editor favorito) con extensiones de Python y soporte para `.env`.  
   - Asegúrate de instalar la extensión “Python” en VS Code para autocompletado y linters.

6. **Miniconda (opcional, pero recomendado si necesitas aislar entornos)**  
   - Descarga e instala Miniconda desde: https://docs.conda.io/en/latest/miniconda.html  
   - Crea un entorno específico para el proyecto:
     ```bash
     conda create -n ed2 python=3.10 -y
     conda activate ed2
     pip install -r requirements.txt
     ```

7. **Dependencias del proyecto**  
   - En la raíz del repositorio debería existir un archivo `requirements.txt` con, al menos, las siguientes líneas:
     ```
     mysql-connector-python
     python-dotenv
     pytest
     scipy
     ```
   - Instálalas con:
     ```bash
     pip install --upgrade pip
     pip install -r requirements.txt
     ```

## 2. Configuración de Credenciales

Para no subir credenciales sensibles al repositorio, utilizaremos un archivo de entorno (`.env`) combinado con un módulo de configuración (`config/config.py`).  

### 2.1. Crear el archivo `.env`

1. En la raíz del proyecto, crea un archivo llamado `.env`. 

2. Dentro, define las siguientes variables (reemplaza los valores de ejemplo por tus credenciales reales):

   ```ini
   # .env
   DATABASE_USERNAME=user
   DATABASE_PASSWORD=password
   DATABASE_HOST=host
   DATABASE_NAME=name
   ```
3. Abre (o crea) el archivo .gitignore en la raíz del proyecto y agrega la línea:

    ```ini
    # .gitignore
    .env
    ```
### 2.2 ¿Que hacer si .env ya fue comprometido?

Si por error ya habías hecho commit y push de (`.env`) antes de añadirlo a (`.gitignore`), es necesario quitarlo del índice de Git para que deje de aparecer en GitHub, pero conservarlo localmente.

1. Verifica que .env esté en .gitignore
    
    Asegúrate de que tu .gitignore contenga:

    ```bash
    #.gitignore
    .env
    ```

2. Quitar .env del control de versiones (índice)
    
    En la terminal, estando en la carpeta raíz del proyecto, ejecuta:

    ```bash
    git rm --cached .env
    ```
    "--cached" indica que Git debe dejar de rastrear el archivo, pero sin borrarlo de tu disco local.

3. Hacer commit de la eliminación de .env

    ```bash
    git add .gitignore
    git commit -m "Dejar de rastrear .env y agregarlo a .gitignore"
    ```

4. Hacerle push de los cambios a GitHub

    ```bash
    git push origin <nombre-de-tu-rama>
    ```

A partir de este momento, el archivo .env ya no se mostrará en el listado de archivos de GitHub. Sin embargo, aún existirá en el historial anterior de commits.

> **Responsable de esta sección**: [Pones el nombre]  
> Encargado de la exportacion y formato de formatos csv y json.

> **Responsable de esta sección**: [Pones el nombre]  
> Encargado de los algoritmos 'sort' e hilos.

> **Responsable de esta sección**: [Pones el nombre]  
> Encargado de los sockets (cliente - servidor) y analisis del tiempo.