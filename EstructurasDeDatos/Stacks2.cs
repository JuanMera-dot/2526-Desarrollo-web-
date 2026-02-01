using System;
using System.Collections.Generic;

class TorresHanoi
{
    // Representamos las torres como pilas de enteros
    static Stack<int> torreOrigen = new Stack<int>();
    static Stack<int> torreAux = new Stack<int>();
    static Stack<int> torreDestino = new Stack<int>();

    static void Main(string[] args)
    {
        int nDiscos = 3; // Puedes cambiar este número
        double totalMovimientos = Math.Pow(2, nDiscos) - 1;

        // Llenamos la torre origen (el disco mayor entra primero)
        // Disco 3, luego 2, luego 1 (1 está en el tope)
        for (int i = nDiscos; i >= 1; i--)
        {
            torreOrigen.Push(i);
        }

        Console.WriteLine($"Resolviendo Torres de Hanoi con {nDiscos} discos usando Pilas:\n");
        ImprimirEstado(); // Estado inicial

        // Algoritmo iterativo
        for (int i = 1; i <= totalMovimientos; i++)
        {
            // Determinar movimiento según el turno (i)
            if (i % 3 == 1)
                MoverDiscoLegal(torreOrigen, torreDestino, "Origen", "Destino");
            else if (i % 3 == 2)
                MoverDiscoLegal(torreOrigen, torreAux, "Origen", "Auxiliar");
            else if (i % 3 == 0)
                MoverDiscoLegal(torreAux, torreDestino, "Auxiliar", "Destino");
            
            ImprimirEstado(); // Ver cómo quedaron las torres
        }
    }

    // Intenta mover un disco entre dos torres respetando las reglas
    static void MoverDiscoLegal(Stack<int> origen, Stack<int> destino, string nombreOr, string nombreDest)
    {
        // Caso 1: La torre destino está vacía -> movemos origen a destino
        if (destino.Count == 0 && origen.Count > 0)
        {
            int disco = origen.Pop();
            destino.Push(disco);
            Console.WriteLine($"Mover disco {disco} de {nombreOr} a {nombreDest}");
        }
        // Caso 2: La torre origen está vacía -> movemos destino a origen
        else if (origen.Count == 0 && destino.Count > 0)
        {
            int disco = destino.Pop();
            origen.Push(disco);
            Console.WriteLine($"Mover disco {disco} de {nombreDest} a {nombreOr}");
        }
        // Caso 3: Ambas tienen discos, comparamos tamaños
        else if (origen.Count > 0 && destino.Count > 0)
        {
            if (origen.Peek() < destino.Peek())
            {
                int disco = origen.Pop();
                destino.Push(disco);
                Console.WriteLine($"Mover disco {disco} de {nombreOr} a {nombreDest}");
            }
            else
            {
                int disco = destino.Pop();
                origen.Push(disco);
                Console.WriteLine($"Mover disco {disco} de {nombreDest} a {nombreOr}");
            }
        }
    }

    static void ImprimirEstado()
    {
        // Función para visualizar las pilas
        Console.WriteLine($"   [Origen]: {String.Join(",", torreOrigen)}");
        Console.WriteLine($"   [Aux   ]: {String.Join(",", torreAux)}");
        Console.WriteLine($"   [Dest  ]: {String.Join(",", torreDestino)}");
        Console.WriteLine("-----------------------------");
    }
}