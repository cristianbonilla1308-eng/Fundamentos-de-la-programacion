"""
================================================================
   SISTEMA DE VENTAS Y INVENTARIO - TACOS LA CHILCA
   Proyecto final 
================================================================
"""

import os      # Para verificar si un archivo ya existe
import time    # Para la pantalla de carga y el control de inactividad
import pdb     # Para hacer debugging del programa 

NOMBRE_NEGOCIO = "Tacos La Chilca"


TIEMPO_INACTIVIDAD = 600


ARCHIVOS_INICIALES = ["menu.txt", "ventas.txt", "clientes.txt", "pedidos.txt", "inventario.txt"]

ARCHIVO_INVENTARIO = "inventario.txt"

menu_principal = [
    ["1", "Realizar venta"],
    ["2", "Consultar menu"],
    ["3", "Leer archivos"],
    ["4", "Crear archivo"],
    ["5", "Agregar informacion a archivo"],
    ["6", "Ver inventario"],
    ["7", "Salir"]
]

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

def verificar_archivos():
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

    contenido_inventario = (
        "Taco al pastor|50\n"
        "Taco de bistec|40\n"
        "Taco de suadero|45\n"
        "Taco de carnitas|40\n"
        "Taco de pollo|35\n"
        "Quesadilla|20\n"
        "Gringa|15\n"
        "Refresco|30\n"
        "Agua fresca|25\n"
    )

    contenidos_iniciales = {
        "menu.txt": contenido_menu,
        "ventas.txt": contenido_ventas,
        "clientes.txt": contenido_clientes,
        "pedidos.txt": contenido_pedidos,
        "inventario.txt": contenido_inventario
    }

    for nombre_archivo in ARCHIVOS_INICIALES:
        if not os.path.exists(nombre_archivo):
            try:
                with open(nombre_archivo, "w") as archivo:
                    archivo.write(contenidos_iniciales[nombre_archivo])
            except PermissionError:
                print(f"No se tienen permisos para crear {nombre_archivo}.")
            except Exception as error:
                print("Ocurrio un error creando archivos iniciales:", error)

def pantalla_carga():
    print("\nCargando sistema de " + NOMBRE_NEGOCIO + "...")
    barra = ""
    for i in range(5):
        barra = barra + "#"
        print("[" + barra + "]")
        time.sleep(1)  
    print("Sistema listo.\n")

def solicitar_fecha():
    while True:
        fecha_ingresada = input("Ingresa la fecha de hoy (dd/mm/aaaa): ")
        try:
            dia, mes, anio = fecha_ingresada.split("/")

            if not (dia.isdigit() and mes.isdigit() and anio.isdigit()):
                print("La fecha debe contener solo numeros. Intenta de nuevo.")
                continue

            if int(dia) < 1 or int(dia) > 31 or int(mes) < 1 or int(mes) > 12:
                print("Dia o mes fuera de rango. Intenta de nuevo.")
                continue

            Fecha = dia, mes, anio
            return Fecha

        except ValueError:
            print("Formato de fecha incorrecto. Usa el formato dd/mm/aaaa.")

def mostrar_menu_principal():
    print("\n===== " + NOMBRE_NEGOCIO + " - MENU PRINCIPAL =====")
    for fila in menu_principal:
        numero_opcion = fila[0]
        texto_opcion = fila[1]
        print(numero_opcion + ". " + texto_opcion)
    print("=======================================")

def mostrar_menu_productos():
    print("\n===== " + NOMBRE_NEGOCIO + " - PRODUCTOS =====")
    for fila in menu_productos:
        numero = fila[0]
        nombre_producto = fila[1]
        precio = fila[2]
        print(numero + ". " + nombre_producto + "     $" + str(precio))
    print("========================================")

def cargar_inventario():
    inventario = []
    try:
        with open(ARCHIVO_INVENTARIO, "r") as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                linea = linea.strip()
                if linea == "":
                    continue
                partes = linea.split("|")
                if len(partes) == 2:
                    nombre_producto = partes[0]
                    cantidad = int(partes[1])
                    inventario.append([nombre_producto, cantidad])

    except FileNotFoundError:
        print("No se encontro inventario.txt, se creara uno nuevo.")
        verificar_archivos()
        return cargar_inventario()
    except PermissionError:
        print("No tienes permisos para leer inventario.txt")
    except Exception as error:
        print("Ocurrio un error al leer el inventario:", error)

    return inventario

def guardar_inventario(inventario):
    try:
        with open(ARCHIVO_INVENTARIO, "w") as archivo:
            for fila in inventario:
                nombre_producto = fila[0]
                cantidad = fila[1]
                archivo.write(nombre_producto + "|" + str(cantidad) + "\n")

    except PermissionError:
        print("No tienes permisos para actualizar inventario.txt")
    except Exception as error:
        print("Ocurrio un error al guardar el inventario:", error)

def mostrar_inventario(inventario):
    print("\n===== INVENTARIO DE " + NOMBRE_NEGOCIO.upper() + " =====\n")
    print("Producto              Existencias")

    contador = 1
    for fila in inventario:
        nombre_producto = fila[0]
        cantidad = fila[1]

        if cantidad == 0:
            print(str(contador) + ". " + nombre_producto + "        AGOTADO")
        else:
            print(str(contador) + ". " + nombre_producto + "        " + str(cantidad))
        contador = contador + 1

    print("")

def control_inactividad(tiempo_ultima_accion):
    tiempo_actual = time.time()
    segundos_transcurridos = int(tiempo_actual - tiempo_ultima_accion)

    if segundos_transcurridos >= TIEMPO_INACTIVIDAD:
        for segundo in range(0, segundos_transcurridos, 60):
            pass  

        print("\nHan pasado " + str(segundos_transcurridos) + " segundos sin interaccion.")
        respuesta = input('¿Deseas continuar en el menu? Escribe "si" o "no": ')
        respuesta = respuesta.strip().lower()

        if respuesta == "si":
            return True
        else:
            return False

    return True

def guardar_venta(nombre, Fecha, productos_comprados, total):
    dia, mes, anio = Fecha  # Desempacamos la tupla de la fecha

    try:
        with open("ventas.txt", "a") as archivo:
            archivo.write("--------------------------------\n")
            archivo.write("Venta de " + NOMBRE_NEGOCIO + "\n")
            archivo.write("Usuario: " + nombre + "\n")
            archivo.write("Fecha: " + dia + "/" + mes + "/" + anio + "\n")

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

def buscar_en_inventario(inventario, nombre_producto):
    for indice in range(len(inventario)):
        if inventario[indice][0] == nombre_producto:
            return indice
    return -1

def realizar_venta(nombre, Fecha, inventario):
    productos_comprados = []  # Lista donde se guarda cada producto comprado
    total = 0
    continuar_comprando = True
    hubo_venta_exitosa = False  # Para saber si hay que guardar el inventario al final

    while continuar_comprando:
        mostrar_menu_productos()
        opcion_producto = input("Selecciona un producto (numero): ")

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

        indice_inventario = buscar_en_inventario(inventario, nombre_producto)

        if indice_inventario == -1:
            print("No se encontro este producto en el inventario.")
            continue

        existencia_actual = inventario[indice_inventario][1]

        if existencia_actual == 0:
            print("Este producto esta agotado y no puede venderse.")
            print("Por favor selecciona otro producto.")
            continue

        try:
            cantidad = int(input("Cantidad: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor a cero.")
                continue
        except ValueError:
            print("Debes escribir un numero valido para la cantidad.")
            continue

        if cantidad > existencia_actual:
            print("No hay suficientes existencias.")
            print("Actualmente solo quedan " + str(existencia_actual) +
                  " unidades de " + nombre_producto + ".")
            print("La venta de esta cantidad no puede realizarse.")
            continue  # Se le permite al usuario intentar de nuevo

        subtotal = precio * cantidad
        total = total + subtotal

        existencia_nueva = existencia_actual - cantidad
        inventario[indice_inventario][1] = existencia_nueva
        hubo_venta_exitosa = True

        print("Existencias anteriores: " + str(existencia_actual))
        print("Cantidad vendida: " + str(cantidad))
        print("Existencias restantes: " + str(existencia_nueva))

        productos_comprados.append([nombre_producto, cantidad, precio, subtotal])
        print("Producto agregado correctamente.")

        otra_compra = input("¿Deseas agregar otro producto? si/no: ").strip().lower()
        if otra_compra != "si":
            continuar_comprando = False

    if len(productos_comprados) == 0:
        print("No se agrego ningun producto. Venta cancelada.")
        return

    mostrar_ticket(nombre, Fecha, productos_comprados, total)
    guardar_venta(nombre, Fecha, productos_comprados, total)

    if hubo_venta_exitosa:
        guardar_inventario(inventario)

def leer_archivo():
    print("\nArchivos disponibles:")
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

def main():
    programa_activo = True

    while programa_activo:

        #  identificacion de usuario
        nombre = input("Ingresa tu nombre o nickname: ")

        #  captura de fecha en tupla (dia, mes, anio)
        Fecha = solicitar_fecha()

        verificar_archivos()

        #  pantalla de carga
        pantalla_carga()

        #  bienvenida personalizada usando el nombre
        print("Bienvenido " + nombre + " a " + NOMBRE_NEGOCIO)
        print(f"Hoy es {Fecha[0]}/{Fecha[1]}/{Fecha[2]}. ¡Que tengas un excelente dia!")

        # Cargamos el inventario desde inventario.txt 
        inventario = cargar_inventario()

        tiempo_ultima_accion = time.time()

        seguir_en_menu = True

        #  menu principal controlado con while,
        while seguir_en_menu:

            #  revisamos si el usuario estuvo inactivo
            continuar = control_inactividad(tiempo_ultima_accion)
            if not continuar:
                seguir_en_menu = False
                break

            mostrar_menu_principal()
            opcion = input("Selecciona una opcion: ")

            tiempo_ultima_accion = time.time()

            if opcion == "1":
                realizar_venta(nombre, Fecha, inventario)

            elif opcion == "2":
                mostrar_menu_productos()

            elif opcion == "3":
                leer_archivo()

            elif opcion == "4":
                crear_archivo()

            elif opcion == "5":
                agregar_archivo()

            elif opcion == "6":
                #  consultar inventario en cualquier momento
                mostrar_inventario(inventario)

            elif opcion == "7":
                print("Gracias por usar el sistema de " + NOMBRE_NEGOCIO + ". ¡Hasta pronto, " + nombre + "!")
                seguir_en_menu = False
                programa_activo = False

            else:
                print("Opcion invalida. Intenta de nuevo.")

    print("Programa finalizado.")

if __name__ == "__main__":
    # NOTA DE DEBUGGING 
# DEBUGGING REALIZADO: se uso PDB para revisar cantidad, precio y subtotal.
# Se detecto que cantidad era texto; se corrigio convirtiendola con int() y try-except.
    main()

# DEBUGGING REALIZADO: se uso PDB para revisar cantidad, precio y subtotal.
# Se detecto que cantidad era texto; se corrigio convirtiendola con int() y try-except.
