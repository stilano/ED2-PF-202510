# Para leer variables de entorno desde un archivo .env
from dotenv import load_dotenv
# Para conectar a MySQL y capturar errores relacionados
from mysql.connector import connect, errorcode, Error
# Para acceder a las variables de entorno del sistema
from os import environ
# Para manejar datos en formato de tabla (DataFrame)
import pandas as pd


# 1. Cargamos variables del archivo .env
# load_dotenv() busca un archivo llamado ".env" en el directorio actual
# y carga las variables definidas allí en el entorno de Python.
load_dotenv()


# 2. Configuramos la conexión

# Aquí creamos un diccionario con las claves necesarias para conectarse
# a la base de datos MySQL. Las claves (DATABASE_USERNAME, etc.) deben
# estar definidas en el archivo .env.
config = {
    "user": environ['DATABASE_USERNAME'],       # Nombre de usuario de la BD
    "password": environ['DATABASE_PASSWORD'],   # Contraseña de la BD
    "host": environ['DATABASE_HOST'],           # Dirección del servidor MySQL (p.ej. 'localhost')
    "database": environ['DATABASE_NAME'],       # Nombre de la base de datos a usar
    "charset": 'utf8'                           # Codificación de caracteres
}


# 3. Obtenemnos la conexión
def get_connection():
    """
    Intenta establecer una conexión con la base de datos MySQL usando
    los parámetros definidos en 'config'. Si hay un error de autenticación
    o la base de datos no existe, lo informa por pantalla y retorna None.
    """
    try:
        # connect(**config) descompone el diccionario y lo pasa como argumentos.
        return connect(**config)
    except Error as err:
        # Si el error es por credenciales incorrectas
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: usuario o contraseña inválidos.")
        # Si la base de datos indicada no existe
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: la base de datos no existe.")
        else:
            # Otros errores genéricos de MySQL
            print(err)
        return None


# 4. Ejecutamos una consulta y devolver los resultados
def get_data(connection: connect, query: str):
    """
    Recibe una conexión activa a MySQL y una consulta SQL en forma de cadena.
    Ejecuta la consulta y devuelve todos los resultados como una lista de tuplas.
    """
    # Se crea un cursor a partir de la conexión para ejecutar la consulta
    my_cursor = connection.cursor()
    # Se ejecuta la consulta SQL
    my_cursor.execute(query)
    # Se realiza un fetchall() obtiene todos los registros resultantes de la consulta
    data = my_cursor.fetchall()
    # Cerramos el cursor para liberar recursos
    my_cursor.close()
    return data


# 5. Establecemos la conexión y verificar
cnx = get_connection()

# Si la conexión se estableció correctamente, imprimimos un mensaje.
# Si get_connection() devolvió None, no hay conexión válida.
if cnx:
    print("Conexión establecida exitosamente")
else:
    print("No se pudo conectar a la base de datos")


# 6. Obtenemos datos de la tabla UN.VENTAS
# En este ejemplo, limitamos la consulta a 1000 filas para no sobrecargar la memoria.
data = get_data(cnx, "SELECT * FROM UN.VENTAS LIMIT 1000")


# 7. Crear un DataFrame de pandas con los resultados
# Convertimos la lista de tuplas 'data' en un DataFrame y asignamos nombres
# de columna para cada campo de la tabla UN.VENTAS.
df = pd.DataFrame(
    data,
    columns=[
        'ID_VENTA',       # Identificador único de la venta
        'FECHA_VENTA',    # Fecha en que se realizó la venta
        'ID_CLIENTE',     # Identificador del cliente
        'ID_EMPLEADO',    # Identificador del empleado que registró la venta
        'ID_PRODUCTO',    # Identificador del producto vendido
        'CANTIDAD',       # Cantidad de unidades vendidas
        'PRECIO_UNITARIO',# Precio por unidad en el momento de la venta
        'DESCUENTO',      # Porcentaje o valor de descuento aplicado
        'FORMA_PAGO'      # Forma de pago utilizada (p.ej. 'Efectivo', 'Tarjeta')
    ]
)


# 8. Mostrar el DataFrame por pantalla
# Esto permite verificar que los datos se cargaron correctamente.
print(df)

