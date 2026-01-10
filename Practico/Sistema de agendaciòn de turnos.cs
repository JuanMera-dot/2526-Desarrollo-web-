using System;

namespace SistemaClinica
{
    // Estructura para representar a un Paciente (Uso de Estructuras/Registros)
    public struct Paciente
    {
        public string Nombre;
        public string Cedula;
        public string Especialidad;
        public string Hora;

        public Paciente(string nombre, string cedula, string especialidad, string hora)
        {
            Nombre = nombre;
            Cedula = cedula;
            Especialidad = especialidad;
            Hora = hora;
        }

        public override string ToString()
        {
            return $"Hora: {Hora} | Paciente: {Nombre} | Cédula: {Cedula} | Especialidad: {Especialidad}";
        }
    }

    // Clase Principal que gestiona la lógica (Uso de POO)
    class GestionTurnos
    {
        private Paciente[] listaTurnos; // Uso de Vectores (Arreglos)
        private int contador;

        public GestionTurnos(int capacidad)
        {
            listaTurnos = new Paciente[capacidad];
            contador = 0;
        }

        public void AgregarTurno(string nombre, string cedula, string especialidad, string hora)
        {
            if (contador < listaTurnos.Length)
            {
                listaTurnos[contador] = new Paciente(nombre, cedula, especialidad, hora);
                contador++;
                Console.WriteLine("Turno registrado exitosamente.");
            }
            else
            {
                Console.WriteLine("Error: La agenda está llena.");
            }
        }

        // Reportería: Visualizar todos los elementos
        public void MostrarTodosLosTurnos()
        {
            Console.WriteLine("\n--- LISTA GENERAL DE TURNOS ---");
            if (contador == 0) Console.WriteLine("No hay turnos registrados.");
            for (int i = 0; i < contador; i++)
            {
                Console.WriteLine($"{i + 1}. {listaTurnos[i].ToString()}");
            }
        }

        // Reportería: Consultar por Cédula
        public void ConsultarPorCedula(string cedula)
        {
            Console.WriteLine($"\n--- RESULTADO DE BÚSQUEDA (Cédula: {cedula}) ---");
            bool encontrado = false;
            for (int i = 0; i < contador; i++)
            {
                if (listaTurnos[i].Cedula == cedula)
                {
                    Console.WriteLine(listaTurnos[i].ToString());
                    encontrado = true;
                    break;
                }
            }
            if (!encontrado) Console.WriteLine("Paciente no encontrado.");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            GestionTurnos clinica = new GestionTurnos(10); // Capacidad para 10 turnos
            int opcion;

            do
            {
                Console.WriteLine("\n--- SISTEMA DE TURNOS MÉDICOS ---");
                Console.WriteLine("1. Registrar Turno");
                Console.WriteLine("2. Ver Todos los Turnos (Reportería)");
                Console.WriteLine("3. Buscar Paciente por Cédula (Consulta)");
                Console.WriteLine("4. Salir");
                Console.Write("Seleccione una opción: ");
                opcion = int.Parse(Console.ReadLine());

                switch (opcion)
                {
                    case 1:
                        Console.Write("Nombre: "); string n = Console.ReadLine();
                        Console.Write("Cédula: "); string c = Console.ReadLine();
                        Console.Write("Especialidad: "); string e = Console.ReadLine();
                        Console.Write("Hora (HH:MM): "); string h = Console.ReadLine();
                        clinica.AgregarTurno(n, c, e, h);
                        break;
                    case 2:
                        clinica.MostrarTodosLosTurnos();
                        break;
                    case 3:
                        Console.Write("Ingrese Cédula a buscar: ");
                        string busqueda = Console.ReadLine();
                        clinica.ConsultarPorCedula(busqueda);
                        break;
                }
            } while (opcion != 4);
        }
    }
}