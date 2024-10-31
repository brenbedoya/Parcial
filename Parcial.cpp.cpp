#include <iostream>
#include <fstream>
#include <string>
#include <stack>
#include <queue>
#include <limits>

using namespace std;

struct Libro {
	string titulo;
	string autor;
	int anio;
	string editorial;
	string ISBN;
	int paginas;
	Libro* siguiente;
};

struct Lector {
	string nombre;
	int dni;
	string libroSolicitado;
};

Libro* inicioLibros = nullptr;
queue<Lector> colaSolicitudes;
stack<string> pilaOperaciones;

void cargarLibrosDesdeArchivo() {
	ifstream archivo("biblioteca.txt");
	if (!archivo.is_open()) {
		cerr << "Error al abrir el archivo de biblioteca." << endl;
		return;
	}
	
	string titulo, autor, editorial, ISBN;
	int anio, paginas;
	
	while (archivo >> ws && getline(archivo, titulo)) {
		getline(archivo, autor);
		archivo >> anio >> ws;
		getline(archivo, editorial);
		getline(archivo, ISBN);
		archivo >> paginas;
		
		if (archivo.fail()) {
			cerr << "Error de formato en archivo de biblioteca." << endl;
			break;
		}
		
		Libro* nuevoLibro = new Libro{titulo, autor, anio, editorial, ISBN, paginas, inicioLibros};
		inicioLibros = nuevoLibro;
	}
	archivo.close();
}

void guardarLibrosEnArchivo() {
	ofstream archivo("biblioteca.txt");
	if (!archivo.is_open()) {
		cerr << "Error al guardar el archivo de biblioteca." << endl;
		return;
	}
	Libro* actual = inicioLibros;
	while (actual) {
		archivo << actual->titulo << endl
			<< actual->autor << endl
			<< actual->anio << endl
			<< actual->editorial << endl
			<< actual->ISBN << endl
			<< actual->paginas << endl;
		actual = actual->siguiente;
	}
	archivo.close();
}

void cargarSolicitudesDesdeArchivo() {
	ifstream archivo("solicitudes.txt");
	if (!archivo.is_open()) {
		cerr << "Error al abrir el archivo de solicitudes." << endl;
		return;
	}
	
	string nombre, libroSolicitado;
	int dni;
	
	while (archivo >> ws && getline(archivo, nombre)) {
		archivo >> dni >> ws;
		getline(archivo, libroSolicitado);
		
		if (archivo.fail()) {
			cerr << "Error de formato en archivo de solicitudes." << endl;
			break;
		}
		
		Lector lector{nombre, dni, libroSolicitado};
		colaSolicitudes.push(lector);
	}
	archivo.close();
}

void guardarSolicitudesEnArchivo() {
	ofstream archivo("solicitudes.txt");
	if (!archivo.is_open()) {
		cerr << "Error al guardar el archivo de solicitudes." << endl;
		return;
	}
	
	queue<Lector> copiaCola = colaSolicitudes;
	while (!copiaCola.empty()) {
		Lector lector = copiaCola.front();
		archivo << lector.nombre << endl
			<< lector.dni << endl
			<< lector.libroSolicitado << endl;
		copiaCola.pop();
	}
	archivo.close();
}

Libro* buscarLibro(const string& criterio, const string& valor) {
	Libro* actual = inicioLibros;
	while (actual) {
		if ((criterio == "titulo" && actual->titulo == valor) ||
			(criterio == "autor" && actual->autor == valor) ||
			(criterio == "ISBN" && actual->ISBN == valor)) {
			return actual;
		}
			actual = actual->siguiente;
	}
	return nullptr;
}

void ordenarLibros(Libro* inicio) {
	if (!inicio || !inicio->siguiente) return;
	
	Libro* menor = inicio;
	Libro* actual = inicio->siguiente;
	while (actual) {
		if (actual->titulo < menor->titulo)
			menor = actual;
		actual = actual->siguiente;
	}
	if (menor != inicio) swap(*inicio, *menor);
	
	ordenarLibros(inicio->siguiente);
}

void agregarLibro() {
	Libro* nuevoLibro = new Libro();
	cout << "Ingrese el titulo: "; getline(cin >> ws, nuevoLibro->titulo);
	cout << "Ingrese el autor: "; getline(cin >> ws, nuevoLibro->autor);
	
	cout << "Ingrese el anio: ";
	while (!(cin >> nuevoLibro->anio)) {
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << "Año inválido. Inténtelo de nuevo: ";
	}
	
	cout << "Ingrese la editorial: "; getline(cin >> ws, nuevoLibro->editorial);
	cout << "Ingrese el ISBN: "; cin >> nuevoLibro->ISBN;
	
	cout << "Ingrese el numero de paginas: ";
	while (!(cin >> nuevoLibro->paginas)) {
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << "Número de páginas inválido. Inténtelo de nuevo: ";
	}
	
	nuevoLibro->siguiente = inicioLibros;
	inicioLibros = nuevoLibro;
	pilaOperaciones.push("Agregar libro: " + nuevoLibro->titulo);
	
	guardarLibrosEnArchivo();
}

void solicitarLibro() {
	Lector lector;
	cout << "Ingrese el nombre del lector: "; getline(cin >> ws, lector.nombre);
	
	cout << "Ingrese el DNI del lector: ";
	while (!(cin >> lector.dni)) {
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << "DNI inválido. Inténtelo de nuevo: ";
	}
	
	cout << "Ingrese el titulo del libro solicitado: "; getline(cin >> ws, lector.libroSolicitado);
	
	Libro* libro = buscarLibro("titulo", lector.libroSolicitado);
	if (libro) {
		colaSolicitudes.push(lector);
		pilaOperaciones.push("Solicitar libro: " + lector.libroSolicitado);
		cout << "Solicitud agregada a la cola." << endl;
		guardarSolicitudesEnArchivo();
	} else {
		cerr << "El libro no existe en la biblioteca." << endl;
	}
}

void devolverLibro() {
	if (colaSolicitudes.empty()) {
		cerr << "No hay solicitudes en la cola." << endl;
		return;
	}
	
	Lector lector = colaSolicitudes.front();
	colaSolicitudes.pop();
	pilaOperaciones.push("Devolver libro: " + lector.libroSolicitado);
	
	cout << "Libro devuelto por " << lector.nombre << "." << endl;
	guardarSolicitudesEnArchivo();
}

void deshacerOperacion() {
	if (pilaOperaciones.empty()) {
		cerr << "No hay operaciones para deshacer." << endl;
		return;
	}
	
	cout << "Deshaciendo operacion: " << pilaOperaciones.top() << endl;
	pilaOperaciones.pop();
}

int main() {
	cargarLibrosDesdeArchivo();
	cargarSolicitudesDesdeArchivo();
	
	int opcion;
	do {
		cout << "\n--- Menu Biblioteca ---\n";
		cout << "1. Agregar libro\n";
		cout << "2. Ordenar libros\n";
		cout << "3. Buscar libro\n";
		cout << "4. Solicitar libro\n";
		cout << "5. Devolver libro\n";
		cout << "6. Deshacer ultima operacion\n";
		cout << "7. Salir\n";
		cout << "Seleccione una opcion: ";
		
		if (!(cin >> opcion)) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cerr << "Opción no válida. Inténtelo de nuevo.\n";
			continue;
		}
		
		switch (opcion) {
		case 1: agregarLibro(); break;
		case 2: ordenarLibros(inicioLibros); break;
		case 3: {
			string criterio, valor;
			cout << "Buscar por (titulo, autor, ISBN): "; cin >> criterio;
			cout << "Ingrese el valor de " << criterio << ": "; cin >> ws;
			getline(cin, valor);
			Libro* libroEncontrado = buscarLibro(criterio, valor);
			if (libroEncontrado) {
				cout << "Libro encontrado: " << libroEncontrado->titulo << endl;
			} else {
				cerr << "Libro no encontrado." << endl;
			}
			break;
		}
		case 4: solicitarLibro(); break;
		case 5: devolverLibro(); break;
		case 6: deshacerOperacion(); break;
		case 7: cout << "Saliendo...\n"; break;
		default: cerr << "Opción no válida.\n"; break;
		}
	} while (opcion != 7);
	
	guardarLibrosEnArchivo();
	guardarSolicitudesEnArchivo();
	return 0;
}


