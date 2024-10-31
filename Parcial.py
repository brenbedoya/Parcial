from collections import deque
from typing import Optional

class Libro:
    def __init__(self, titulo: str, autor: str, anio: int, editorial: str, ISBN: str, paginas: int):
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.editorial = editorial
        self.ISBN = ISBN
        self.paginas = paginas
        self.siguiente = None

class Lector:
    def __init__(self, nombre: str, dni: int, libro_solicitado: str):
        self.nombre = nombre
        self.dni = dni
        self.libro_solicitado = libro_solicitado

inicio_libros = None
cola_solicitudes = deque()
pila_operaciones = []

def cargar_libros_desde_archivo():
    global inicio_libros
    try:
        with open("biblioteca.txt", "r") as archivo:
            while True:
                titulo = archivo.readline().strip()
                if not titulo:
                    break
                autor = archivo.readline().strip()
                anio = int(archivo.readline().strip())
                editorial = archivo.readline().strip()
                ISBN = archivo.readline().strip()
                paginas = int(archivo.readline().strip())

                nuevo_libro = Libro(titulo, autor, anio, editorial, ISBN, paginas)
                nuevo_libro.siguiente = inicio_libros
                inicio_libros = nuevo_libro
    except FileNotFoundError:
        print("Error al abrir el archivo de biblioteca.")
    except Exception as e:
        print(f"Error de formato en archivo de biblioteca: {e}")

def guardar_libros_en_archivo():
    global inicio_libros
    try:
        with open("biblioteca.txt", "w") as archivo:
            actual = inicio_libros
            while actual:
                archivo.write(f"{actual.titulo}\n{actual.autor}\n{actual.anio}\n{actual.editorial}\n{actual.ISBN}\n{actual.paginas}\n")
                actual = actual.siguiente
    except Exception as e:
        print(f"Error al guardar el archivo de biblioteca: {e}")

def cargar_solicitudes_desde_archivo():
    global cola_solicitudes
    try:
        with open("solicitudes.txt", "r") as archivo:
            while True:
                nombre = archivo.readline().strip()
                if not nombre:
                    break
                dni = int(archivo.readline().strip())
                libro_solicitado = archivo.readline().strip()

                lector = Lector(nombre, dni, libro_solicitado)
                cola_solicitudes.append(lector)
    except FileNotFoundError:
        print("Error al abrir el archivo de solicitudes.")
    except Exception as e:
        print(f"Error de formato en archivo de solicitudes: {e}")

def guardar_solicitudes_en_archivo():
    global cola_solicitudes
    try:
        with open("solicitudes.txt", "w") as archivo:
            for lector in cola_solicitudes:
                archivo.write(f"{lector.nombre}\n{lector.dni}\n{lector.libro_solicitado}\n")
    except Exception as e:
        print(f"Error al guardar el archivo de solicitudes: {e}")

def buscar_libro(criterio: str, valor: str) -> Optional[Libro]:
    global inicio_libros
    actual = inicio_libros
    while actual:
        if (criterio == "titulo" and actual.titulo == valor) or \
           (criterio == "autor" and actual.autor == valor) or \
           (criterio == "ISBN" and actual.ISBN == valor):
            return actual
        actual = actual.siguiente
    return None

def ordenar_libros(inicio: Libro) -> None:
    if not inicio or not inicio.siguiente:
        return
    menor = inicio
    actual = inicio.siguiente
    while actual:
        if actual.titulo < menor.titulo:
            menor = actual
        actual = actual.siguiente
    if menor!= inicio:
        inicio.titulo, menor.titulo = menor.titulo, inicio.titulo
        inicio.autor, menor.autor = menor.autor, inicio.autor
        inicio.anio, menor.anio = menor.anio, inicio.anio
        inicio.editorial, menor.editorial = menor.editorial, inicio.editorial
        inicio.ISBN, menor.ISBN = menor.ISBN, inicio.ISBN
        inicio.paginas, menor.paginas = menor.paginas, inicio.paginas
    ordenar_libros(inicio.siguiente)

def agregar_libro() -> None:
    global inicio_libros
    nuevo_libro = Libro("", "", 0, "", "", 0)
    nuevo_libro.titulo = input("Ingrese el titulo: ")
    nuevo_libro.autor = input("Ingrese el autor: ")
    
    while True:
        try:
            nuevo_libro.anio = int(input("Ingrese el anio: "))
            break
        except ValueError:
            print("Año inválido. Inténtelo de nuevo: ")
    
    nuevo_libro.editorial = input("Ingrese la editorial: ")
    nuevo_libro.ISBN = input("Ingrese el ISBN: ")
    
    while True:
        try:
            nuevo_libro.paginas = int(input("Ingrese el numero de paginas: "))
            break
        except ValueError:
            print("Número de páginas inválido. Inténtelo de nuevo: ")
    
    nuevo_libro.siguiente = inicio_libros
    inicio_libros = nuevo_libro
    pila_operaciones.append(f"Agregar libro: {nuevo_libro.titulo}")
    
    guardar_libros_en_archivo()

def solicitar_libro() -> None:
    lector = Lector("", 0, "")
    lector.nombre = input("Ingrese el nombre del lector: ")
    
    while True:
        try:
            lector.dni = int(input("Ingrese el DNI del lector: "))
            break
        except ValueError:
            print("DNI inválido. Inténtelo de nuevo: ")
    
    lector.libro_solicitado = input("Ingrese el titulo del libro solicitado: ")
    
    libro = buscar_libro("titulo", lector.libro_solicitado)
    if libro:
        cola_solicitudes.append(lector)
        pila_operaciones.append(f"Solicitar libro: {lector.libro_solicitado}")
        print("Solicitud agregada a la cola.")
        guardar_solicitudes_en_archivo()
    else:
        print("El libro no existe en la biblioteca.")

def devolver_libro() -> None:
    global cola_solicitudes
    if not cola_solicitudes:
        print("No hay solicitudes en la cola.")
        return
    
    lector = cola_solicitudes.popleft()
    pila_operaciones.append(f"Devolver libro: {lector.libro_solicitado}")
    
    print(f"Libro devuelto por {lector.nombre}.")
    guardar_solicitudes_en_archivo()

def deshacer_operacion() -> None:
    global pila_operaciones
    if not pila_operaciones:
        print("No hay operaciones para deshacer.")
        return
    
    print(f"Deshaciendo operacion: {pila_operaciones.pop()}")

def mostrar_libros() -> None:
    try:
        with open("biblioteca.txt", "r") as archivo:
            print("Contenido del archivo de biblioteca:")
            for linea in archivo:
                print(linea.strip())
    except FileNotFoundError:
        print("Error al abrir el archivo de biblioteca.")
    except Exception as e:
        print(f"Error al leer el archivo de biblioteca: {e}")

def mostrar_solicitudes() -> None:
    try:
        with open("solicitudes.txt", "r") as archivo:
            print("Contenido del archivo de solicitudes:")
            solicitud = []
            for linea in archivo:
                solicitud.append(linea.strip())
                if len(solicitud) == 3:
                    print(f"Nombre: {solicitud[0]}")
                    print(f"DNI: {solicitud[1]}")
                    print(f"Libro solicitado: {solicitud[2]}\n")
                    solicitud = []
    except FileNotFoundError:
        print("Error al abrir el archivo de solicitudes.")
    except Exception as e:
        print(f"Error al leer el archivo de solicitudes: {e}")

def main() -> None:
    global inicio_libros, cola_solicitudes, pila_operaciones
    
    cargar_libros_desde_archivo()
    cargar_solicitudes_desde_archivo()
    
    while True:
        print("\n--- Menu Biblioteca ---\n")
        print("1. Agregar libro\n")
        print("2. Ordenar libros\n")
        print("3. Buscar libro\n")
        print("4. Solicitar libro\n")
        print("5. Devolver libro\n")
        print("6. Deshacer ultima operacion\n")
        print("7. Mostrar libros\n")
        print("8. Mostrar solicitudes\n")
        print("9. Salir\n")
        
        while True:
            try:
                opcion = int(input("Seleccione una opcion: "))
                break
            except ValueError:
                print("Opción no válida. Inténtelo de nuevo.\n")
        
        if opcion == 1:
            agregar_libro()
        elif opcion == 2:
            ordenar_libros(inicio_libros)
        elif opcion == 3:
            criterio = input("Buscar por (titulo, autor, ISBN): ")
            valor = input(f"Ingrese el valor de {criterio}: ")
            libro_encontrado = buscar_libro(criterio, valor)
            if libro_encontrado:
                print(f"Libro encontrado: {libro_encontrado.titulo}")
            else:
                print("Libro no encontrado.")
        elif opcion == 4:
            solicitar_libro()
        elif opcion == 5:
            devolver_libro()
        elif opcion == 6:
            deshacer_operacion()
        elif opcion == 7:
            mostrar_libros()
        elif opcion == 8:
            mostrar_solicitudes()
        elif opcion == 9:
            print("Saliendo...\n")
            break
        else:
            print("Opción no válida.\n")

    guardar_libros_en_archivo()
    guardar_solicitudes_en_archivo()

if __name__ == "__main__":
    main()
    