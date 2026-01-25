using System;

namespace EstructurasDeListasEnlazadas
{
    // Definición de un nodo en la lista enlazada
    public class Nodo
    {
        public int dato;
        public Nodo siguiente;

        public Nodo(int dato)
        {
            this.dato = dato; 
            this.siguiente = null;
        }
    }

    // Definición de la lista enlazada
    public class ListaEnlazada
    {
        private Nodo cabeza;

        public ListaEnlazada()
        {
            cabeza = null;
        }

        // Método para agregar un nodo al final de la lista
        public void Agregar(int dato)
        {
            Nodo nuevoNodo = new Nodo(dato);
            if (cabeza == null)
            {
                cabeza = nuevoNodo;
            }
            else
            {
                Nodo actual = cabeza;
                while (actual.siguiente != null)
                {
                    actual = actual.siguiente;
                }
                actual.siguiente = nuevoNodo;
            }
        }

        // Método para imprimir la lista
        public void Imprimir()
        {
            if (cabeza == null)
            {
                Console.WriteLine("La lista está vacía.");
                return;
            }
            Nodo actual = cabeza;
            while (actual != null)
            {
                Console.Write(actual.dato + " -> ");
                actual = actual.siguiente;
            }
            Console.WriteLine("null");
        }

        // EJERCICIO 3: Método de búsqueda que cuenta ocurrencias
        public int Buscar(int valor)
        {
            int contador = 0;
            Nodo actual = cabeza;
            while (actual != null)
            {
                if (actual.dato == valor)
                {
                    contador++;
                }
                actual = actual.siguiente;
            }
            
            if (contador == 0)
            {
                Console.WriteLine($"El dato {valor} no se encuentra en la lista.");
            }
            return contador;
        }

        // EJERCICIO 4: Eliminar nodos fuera de rango
        public void EliminarFueraDeRango(int min, int max)
        {
            Nodo actual = cabeza;
            Nodo anterior = null;

            while (actual != null)
            {
                // Verificar si el dato está fuera del rango (menor que min O mayor que max)
                if (actual.dato < min || actual.dato > max)
                {
                    if (anterior == null)
                    {
                        
                        cabeza = actual.siguiente;
                    }
                    else
                    {
                        // Saltar el nodo actual (el anterior apunta al siguiente del actual)
                        anterior.siguiente = actual.siguiente;
                    }
                  
                }
                else
                {
                    // Si no eliminamos, avanzamos el puntero 'anterior'
                    anterior = actual;
                }
                // Avanzamos al siguiente nodo para continuar el ciclo
                actual = actual.siguiente;
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            ListaEnlazada lista = new ListaEnlazada();
            Random rnd = new Random();

         
            // EJERCICIO 4 (Parte 1): Crear lista con 50 números aleatorios
         
            Console.WriteLine("--- Generando lista con 50 números aleatorios (1-999) ---");
            for (int i = 0; i < 50; i++)
            {
                lista.Agregar(rnd.Next(1, 1000));
            }
            lista.Imprimir();
            Console.WriteLine();

            
            // PRUEBA EJERCICIO 3: Buscar un número
    
            Console.WriteLine("--- EJERCICIO 3: Buscar un número ---");
            Console.Write("Ingrese un número a buscar en la lista: ");
            
            // Usamos una variable temporal string para leer, para evitar errores si el input es vacío
            string input = Console.ReadLine();
            if (int.TryParse(input, out int numeroABuscar))
            {
                int veces = lista.Buscar(numeroABuscar);
                if (veces > 0)
                {
                    Console.WriteLine($"El número {numeroABuscar} se encuentra {veces} veces en la lista.");
                }
            }
            else 
            {
                Console.WriteLine("Entrada no válida, saltando búsqueda...");
            }
            Console.WriteLine();

      
            // PRUEBA EJERCICIO 4 (Parte 2): Filtrar por rango
      
            Console.WriteLine("--- EJERCICIO 4: Eliminar nodos fuera de rango ---");
            try 
            {
                Console.Write("Ingrese el valor MÍNIMO del rango: ");
                int min = int.Parse(Console.ReadLine());

                Console.Write("Ingrese el valor MÁXIMO del rango: ");
                int max = int.Parse(Console.ReadLine());

                Console.WriteLine($"\nEliminando nodos menores a {min} y mayores a {max}...");
                
             
                lista.EliminarFueraDeRango(min, max);

                Console.WriteLine("Lista resultante filtrada:");
                lista.Imprimir();
            }
            catch (Exception)
            {
                Console.WriteLine("Error en el ingreso de datos del rango.");
            }

            Console.WriteLine("Presione cualquier tecla para salir...");
            Console.ReadKey();
        }
    }
}