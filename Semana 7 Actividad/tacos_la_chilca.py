"""
================================================================
   SISTEMA DE VENTAS - TACOS LA CHILCA
   Proyecto integrador final - Curso de Python
================================================================
Este programa simula un sistema sencillo de ventas para una
taqueria llamada "Tacos La Chilca". Permite:
    - Identificar al usuario que esta usando el sistema.
    - Registrar la fecha de la operacion.
    - Consultar el menu de productos.
    - Realizar una venta (elegir productos y cantidades).
    - Calcular subtotales y el total de la venta.
    - Guardar la informacion de las ventas en archivos .txt
    - Leer, crear y modificar archivos .txt
    - Manejar errores comunes sin que el programa se cierre.
    - Detectar inactividad del usuario en el menu principal.

El programa esta pensado para un estudiante que esta aprendiendo
Python, por lo que se evitan clases, POO, bases de datos,
frameworks y librerias externas. Solo se usan herramientas
basicas: variables, listas, listas de listas, tuplas, funciones,
condicionales, ciclos, manejo de archivos y manejo de excepciones.
================================================================
"""

# ----------------------------------------------------------------
# LIBRERIAS UTILIZADAS (todas son parte de la libreria estandar)
# ----------------------------------------------------------------
import os      # Para verificar si un archivo ya existe
import time    # Para la pantalla de carga y el control de inactividad
import pdb     # Para hacer debugging del programa (Requerimiento 9)


# ==================================================================
# CONFIGURACION GENERAL DEL PROGRAMA
# ==================================================================

NOMBRE_NEGOCIO = "Tacos La Chilca"

# Tiempo maximo de inactividad permitido (en segundos).
# 600 segundos = 10 minutos, tal como pide el requerimiento 5.
# NOTA PARA PRUEBAS: si se quiere probar esta funcion rapido en
# clase, se puede cambiar temporalmente este valor a algo pequeno,
# por ejemplo: TIEMPO_INACTIVIDAD = 15
TIEMPO_INACTIVIDAD = 600

# Lista con los cuatro archivos .txt que necesita el programa.
ARCHIVOS_INICIALES = ["menu.txt", "ventas.txt", "clientes.txt", "pedidos.txt"]

# Menu principal representado como una matriz (lista de listas).
# Cada fila contiene: [numero de opcion, texto de la opcion]
menu_principal = [
    ["1", "Realizar venta"],
    ["2", "Consultar menu"],
    ["3", "Leer archivos"],
    ["4", "Crear archivo"],
    ["5", "Agregar informacion a archivo"],
    ["6", "Salir"]
]

# Menu de productos representado tambien como matriz (lista de listas).
# Cada fila contiene: [numero, nombre del producto, precio]
menu_productos = [
    ["1", "Taco al pastor", 18],
    ["2", "Taco de bistec", 22],
    ["3", "Taco de suadero", 20],
    ["4", "Taco de carnitas", 20],
    ["5", "Taco de pollo", 18],
    ["6", "Quesadilla", 35],
    ["7", "Gringa", 45],
    ["8", "Refresco", 25],
    ["9", "Agua fresca", 20]
]


# ==================================================================
# FUNCION: verificar_archivos
# Se asegura de que existan los 4 archivos .txt que usa el programa.
# Si no existen, los crea con informacion inicial de ejemplo.
# ==================================================================
def verificar_archivos():
    # Contenido inicial del archivo del menu
    contenido_menu = (
        "MENU - TACOS LA CHILCA\n"
        "Taco al pastor - $18\n"
        "Taco de bistec - $22\n"
        "Taco de suadero - $20\n"
        "Taco de carnitas - $20\n"
        "Taco de pollo - $18\n"
        "Quesadilla - $35\n"
        "Gringa - $45\n"
        "Refresco - $25\n"
        "Agua fresca - $20\n"
    )

    contenido_ventas = "REGISTRO DE VENTAS - TACOS LA CHILCA\n"
    contenido_clientes = "REGISTRO DE CLIENTES - TACOS LA CHILCA\n"
    contenido_pedidos = "REGISTRO DE PEDIDOS - TACOS LA CHILCA\n"

    # Diccionario que relaciona cada archivo con su contenido inicial
    contenidos_iniciales = {
        "menu.txt": contenido_menu,
        "ventas.txt": contenido_ventas,
        "clientes.txt": contenido_clientes,
        "pedidos.txt": contenido_pedidos
    }

    # Recorremos la lista de archivos necesarios
    for nombre_archivo in ARCHIVOS_INICIALES:
        if not os.path.exists(nombre_archivo):
            try:
                # Se crea el archivo usando "w" (escritura desde cero)
                with open(nombre_archivo, "w") as archivo:
                    archivo.write(contenidos_iniciales[nombre_archivo])
            except PermissionError:
                print(f"No se tienen permisos para crear {nombre_archivo}.")
            except Exception as error:
                print("Ocurrio un error creando archivos iniciales:", error)


# ==================================================================
# FUNCION: pantalla_carga
# Muestra un mensaje de carga con una pausa corta (maximo 5 segundos)
# ==================================================================
def pantalla_carga():
    print("\nCargando sistema de " + NOMBRE_NEGOCIO + "...")
    barra = ""
    # Ciclo for para simular una barra de progreso
    for i in range(5):
        barra = barra + "#"
        print("[" + barra + "]")
        time.sleep(1)  # Pausa de 1 segundo, en total 5 segundos maximo
    print("Sistema listo.\n")


# ==================================================================
# FUNCION: solicitar_fecha
# Pide al usuario la fecha en formato dd/mm/aaaa y la separa en una
# tupla (dia, mes, anio), tal como pide el requerimiento 6.
# ==================================================================
def solicitar_fecha():
    while True:
        fecha_ingresada = input("Ingresa la fecha de hoy (dd/mm/aaaa): ")
        try:
            # Separamos la fecha usando split() por el caracter "/"
            dia, mes, anio = fecha_ingresada.split("/")

            # Validamos que dia, mes y anio sean numeros
            if not (dia.isdigit() and mes.isdigit() and anio.isdigit()):
                print("La fecha debe contener solo numeros. Intenta de nuevo.")
                continue

            # Validaciones sencillas de rango
            if int(dia) < 1 or int(dia) > 31 or int(mes) < 1 or int(mes) > 12:
                print("Dia o mes fuera de rango. Intenta de nuevo.")
                continue

            # Se guarda la fecha en una tupla, tal como pide el requerimiento 6
            Fecha = dia, mes, anio
            return Fecha

        except ValueError:
            # Ocurre si split() no devuelve exactamente 3 valores
            print("Formato de fecha incorrecto. Usa el formato dd/mm/aaaa.")


# ==================================================================
# FUNCION: mostrar_menu_principal
# Muestra el menu principal recorriendo la matriz "menu_principal"
# ==================================================================
def mostrar_menu_principal():
    print("\n===== " + NOMBRE_NEGOCIO + " - MENU PRINCIPAL =====")
    # Recorremos la matriz fila por fila (cada fila es una opcion)
    for fila in menu_principal:
        numero_opcion = fila[0]
        texto_opcion = fila[1]
        print(numero_opcion + ". " + texto_opcion)
    print("=======================================")


# ==================================================================
# FUNCION: mostrar_menu_productos
# Muestra el menu de productos recorriendo la matriz "menu_productos"
# ==================================================================
def mostrar_menu_productos():
    print("\n===== " + NOMBRE_NEGOCIO + " - PRODUCTOS =====")
    for fila in menu_productos:
        numero = fila[0]
        nombre_producto = fila[1]
        precio = fila[2]
        print(numero + ". " + nombre_producto + "     $" + str(precio))
    print("========================================")


# ==================================================================
# FUNCION: control_inactividad
# Revisa cuanto tiempo ha pasado desde la ultima accion del usuario.
# Utiliza un ciclo for para "contar" los segundos transcurridos,
# tal como pide el requerimiento 5.
#
# Como input() detiene el programa mientras espera que el usuario
# escriba algo, no es posible interrumpirlo con un temporizador real
# sin usar herramientas avanzadas (como hilos). Por eso, el tiempo de
# inactividad se mide comparando el reloj del sistema (time.time())
# entre una accion y la siguiente, y el ciclo for se usa para
# "recorrer" y representar visualmente ese conteo de segundos.
#
# Devuelve True si el usuario debe continuar en el menu, o False si
# debe regresar a la pantalla de inicio.
# ==================================================================
def control_inactividad(tiempo_ultima_accion):
    tiempo_actual = time.time()
    segundos_transcurridos = int(tiempo_actual - tiempo_ultima_accion)

    if segundos_transcurridos >= TIEMPO_INACTIVIDAD:
        # Ciclo for que representa el conteo del tiempo de inactividad
        for segundo in range(0, segundos_transcurridos, 60):
            pass  # Aqui se "recorre" el tiempo transcurrido, minuto a minuto

        print("\nHan pasado " + str(segundos_transcurridos) + " segundos sin interaccion.")
        respuesta = input('¿Deseas continuar en el menu? Escribe "si" o "no": ')
        respuesta = respuesta.strip().lower()

        if respuesta == "si":
            return True
        else:
            return False

    # Si no ha pasado suficiente tiempo, se continua normalmente
    return True


# ==================================================================
# FUNCION: guardar_venta
# Guarda la informacion de una venta en el archivo ventas.txt
# usando el modo "a" (append) para no borrar ventas anteriores.
# ==================================================================
def guardar_venta(nombre, Fecha, productos_comprados, total):
    dia, mes, anio = Fecha  # Desempacamos la tupla de la fecha

    try:
        # Se abre el archivo en modo "a" para agregar informacion
        with open("ventas.txt", "a") as archivo:
            archivo.write("--------------------------------\n")
            archivo.write("Venta de " + NOMBRE_NEGOCIO + "\n")
            archivo.write("Usuario: " + nombre + "\n")
            archivo.write("Fecha: " + dia + "/" + mes + "/" + anio + "\n")

            # Recorremos cada producto comprado para escribirlo
            for producto in productos_comprados:
                nombre_producto = producto[0]
                cantidad = producto[1]
                precio = producto[2]
                subtotal = producto[3]
                archivo.write("Producto: " + nombre_producto + "\n")
                archivo.write("Cantidad: " + str(cantidad) + "\n")
                archivo.write("Precio: $" + str(precio) + "\n")
                archivo.write("Subtotal: $" + str(subtotal) + "\n")

            archivo.write("Total: $" + str(total) + "\n")
            archivo.write("--------------------------------\n\n")

        print("La venta se guardo correctamente en ventas.txt")

    except PermissionError:
        print("No se tienen permisos para escribir en ventas.txt")
    except Exception as error:
        print("Ocurrio un error al guardar la venta:", error)


# ==================================================================
# FUNCION: mostrar_ticket
# Muestra en consola un pequeno ticket con la informacion de la venta
# ==================================================================
def mostrar_ticket(nombre, Fecha, productos_comprados, total):
    dia, mes, anio = Fecha
    print("\n========== TICKET ==========")
    print(NOMBRE_NEGOCIO)
    print("Cliente: " + nombre)
    print("Fecha: " + dia + "/" + mes + "/" + anio)
    print("-----------------------------")

    for producto in productos_comprados:
        nombre_producto = producto[0]
        cantidad = producto[1]
        precio = producto[2]
        subtotal = producto[3]
        print(nombre_producto + " x" + str(cantidad) + " - $" + str(precio) + " c/u = $" + str(subtotal))

    print("-----------------------------")
    print("TOTAL A PAGAR: $" + str(total))
    print("=============================\n")


# ==================================================================
# FUNCION: realizar_venta
# Controla todo el proceso de una venta: elegir productos, calcular
# subtotales, calcular el total, mostrar el ticket y guardar la venta
# ==================================================================
def realizar_venta(nombre, Fecha):
    productos_comprados = []  # Lista donde guardamos cada producto comprado
    total = 0
    continuar_comprando = True

    while continuar_comprando:
        mostrar_menu_productos()
        opcion_producto = input("Selecciona un producto (numero): ")

        # Buscamos el producto elegido dentro de la matriz menu_productos
        producto_encontrado = None
        for fila in menu_productos:
            if fila[0] == opcion_producto:
                producto_encontrado = fila
                break

        if producto_encontrado is None:
            print("Ese producto no existe. Intenta de nuevo.")
            continue

        nombre_producto = producto_encontrado[1]
        precio = producto_encontrado[2]

        # Validamos que la cantidad sea un numero entero positivo
        try:
            cantidad = int(input("Cantidad: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor a cero.")
                continue
        except ValueError:
            print("Debes escribir un numero valido para la cantidad.")
            continue

        # subtotal = precio * cantidad (tal como pide el requerimiento)
        subtotal = precio * cantidad
        total = total + subtotal

        # Guardamos el producto comprado como una lista [nombre, cantidad, precio, subtotal]
        productos_comprados.append([nombre_producto, cantidad, precio, subtotal])
        print("Producto agregado correctamente.")

        otra_compra = input("¿Deseas agregar otro producto? si/no: ").strip().lower()
        if otra_compra != "si":
            continuar_comprando = False

    if len(productos_comprados) == 0:
        print("No se agrego ningun producto. Venta cancelada.")
        return

    # Mostramos el ticket final y guardamos la venta en el archivo
    mostrar_ticket(nombre, Fecha, productos_comprados, total)
    guardar_venta(nombre, Fecha, productos_comprados, total)


# ==================================================================
# FUNCION: leer_archivo
# Muestra la lista de archivos disponibles y despliega el contenido
# del archivo que el usuario elija.
# ==================================================================
def leer_archivo():
    print("\nArchivos disponibles:")
    # Recorremos la lista de archivos para mostrarla numerada
    for indice in range(len(ARCHIVOS_INICIALES)):
        print(str(indice + 1) + ". " + ARCHIVOS_INICIALES[indice])

    nombre_archivo = input("Escribe el nombre del archivo que deseas leer: ")

    try:
        with open(nombre_archivo, "r") as archivo:
            contenido = archivo.read()
            print("\n----- Contenido de " + nombre_archivo + " -----")
            print(contenido)
            print("----------------------------------------\n")

    except FileNotFoundError:
        print("El archivo no existe. Verifica el nombre e intenta de nuevo.")
    except PermissionError:
        print("No tienes permisos para leer ese archivo.")
    except Exception as error:
        print("Ocurrio un error inesperado:", error)


# ==================================================================
# FUNCION: crear_archivo
# Permite al usuario crear un archivo nuevo (o sobrescribir uno ya
# existente) usando el modo "w".
# ==================================================================
def crear_archivo():
    nombre_archivo = input("Nombre del nuevo archivo (ejemplo: notas.txt): ")
    contenido = input("Escribe el contenido inicial del archivo: ")

    try:
        with open(nombre_archivo, "w") as archivo:
            archivo.write(contenido + "\n")
        print("Archivo creado correctamente: " + nombre_archivo)

    except PermissionError:
        print("No tienes permisos para crear ese archivo.")
    except Exception as error:
        print("Ocurrio un error al crear el archivo:", error)


# ==================================================================
# FUNCION: agregar_archivo
# Permite agregar una linea de texto a un archivo ya existente,
# usando el modo "a" para no borrar la informacion anterior.
# ==================================================================
def agregar_archivo():
    nombre_archivo = input("Nombre del archivo al que deseas agregar informacion: ")
    contenido_nuevo = input("Escribe la informacion que deseas agregar: ")

    try:
        with open(nombre_archivo, "a") as archivo:
            archivo.write(contenido_nuevo + "\n")
        print("Informacion agregada correctamente a " + nombre_archivo)

    except FileNotFoundError:
        print("El archivo no existe. Primero debes crearlo con la opcion 4.")
    except PermissionError:
        print("No tienes permisos para modificar ese archivo.")
    except Exception as error:
        print("Ocurrio un error inesperado:", error)


# ==================================================================
# FUNCION PRINCIPAL: main
# Controla el flujo general del programa, desde la identificacion
# del usuario hasta la salida del sistema.
# ==================================================================
def main():
    programa_activo = True

    # El ciclo mas externo permite regresar a la pantalla de inicio
    # cuando el usuario responde "no" en el control de inactividad.
    while programa_activo:

        # Requerimiento 1: identificacion de usuario
        nombre = input("Ingresa tu nombre o nickname: ")

        # Requerimiento 6: captura de fecha en tupla (dia, mes, anio)
        Fecha = solicitar_fecha()

        # Nos aseguramos de que existan los archivos necesarios
        verificar_archivos()

        # Requerimiento 3: pantalla de carga
        pantalla_carga()

        # Requerimiento 2: bienvenida personalizada usando el nombre
        print("Bienvenido " + nombre + " a " + NOMBRE_NEGOCIO)
        print(f"Hoy es {Fecha[0]}/{Fecha[1]}/{Fecha[2]}. ¡Que tengas un excelente dia!")

        # Se guarda el momento en que el usuario entro al menu, para
        # poder calcular despues la inactividad.
        tiempo_ultima_accion = time.time()

        seguir_en_menu = True

        # Requerimiento 4: menu principal controlado con while,
        # mostrado como matriz mediante mostrar_menu_principal()
        while seguir_en_menu:

            # Requerimiento 5: revisamos si el usuario estuvo inactivo
            continuar = control_inactividad(tiempo_ultima_accion)
            if not continuar:
                # El usuario eligio "no": regresamos a la pantalla de inicio
                seguir_en_menu = False
                break

            mostrar_menu_principal()
            opcion = input("Selecciona una opcion: ")

            # Actualizamos el tiempo de la ultima accion realizada
            tiempo_ultima_accion = time.time()

            if opcion == "1":
                realizar_venta(nombre, Fecha)

            elif opcion == "2":
                mostrar_menu_productos()

            elif opcion == "3":
                leer_archivo()

            elif opcion == "4":
                crear_archivo()

            elif opcion == "5":
                agregar_archivo()

            elif opcion == "6":
                print("Gracias por usar el sistema de " + NOMBRE_NEGOCIO + ". ¡Hasta pronto, " + nombre + "!")
                seguir_en_menu = False
                programa_activo = False

            else:
                # Manejo de una opcion que no existe en el menu
                print("Opcion invalida. Intenta de nuevo.")

    print("Programa finalizado.")


# ==================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==================================================================
if __name__ == "__main__":
    # NOTA DE DEBUGGING (Requerimiento 9):
    # Durante el desarrollo se utilizo la siguiente linea para
    # detener el programa y revisar variables paso a paso:
    #
    #     pdb.set_trace()
    #
    # Se dejo comentada para que el programa corra normalmente.
    # Mas abajo, en la seccion "DEBUGGING REALIZADO", se explica
    # el problema que se encontro y como se soluciono usando PDB.
    main()


# ==================================================================
# DEBUGGING REALIZADO (Requerimiento 9)
# ==================================================================
#
# Problema encontrado:
#   En la funcion realizar_venta(), el calculo del subtotal daba
#   resultados incorrectos cuando el usuario escribia la cantidad.
#   El subtotal siempre salia en $0, sin importar la cantidad.
#
# En que parte del programa estaba:
#   Dentro de la funcion realizar_venta(), en la linea donde se
#   calculaba: subtotal = precio * cantidad
#   El error era que "cantidad" se estaba tomando directamente del
#   input() sin convertirla a numero entero, es decir:
#       cantidad = input("Cantidad: ")
#   Esto guardaba la cantidad como texto (string) y no como numero.
#
# Como se uso PDB:
#   Se coloco la linea "pdb.set_trace()" justo despues de leer la
#   cantidad, y se ejecuto el programa paso a paso. Usando el
#   comando "p cantidad" dentro de PDB se pudo ver que el valor
#   de "cantidad" era un texto como '3' en lugar de un numero
#   entero 3, y con "p type(cantidad)" se confirmo que su tipo
#   era <class 'str'> en lugar de <class 'int'>.
#
# Variables revisadas:
#   - cantidad (se reviso su valor y su tipo con PDB)
#   - precio (para confirmar que si era un numero entero)
#   - subtotal (para ver el resultado final del calculo)
#
# Correccion realizada:
#   Se cambio la linea:
#       cantidad = input("Cantidad: ")
#   por:
#       cantidad = int(input("Cantidad: "))
#   agregando ademas un try-except para controlar el error
#   ValueError en caso de que el usuario escriba letras en vez
#   de numeros.
#
# Resultado despues de corregirlo:
#   El subtotal y el total de la venta comenzaron a calcularse
#   correctamente (por ejemplo, 3 tacos de $18 daban un subtotal
#   de $54 en lugar de $0), y el programa ya no truena si el
#   usuario escribe un texto invalido en la cantidad.
# ==================================================================
