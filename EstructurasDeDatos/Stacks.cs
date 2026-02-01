using System;
using System.Collections.Generic;

class Program
{
    static void Main_Ejercicio1(string[] args)
    {
        // Definir la expresion de prueba
        string expresion = "{7+(8*5)- [(9-7)+(4+1)]}";
        Console.WriteLine($"Analizando: {expresion}");

        // LLamar a la funcion de verificacion
        bool balanceada = VerificarBalanceo(expresion);
        if (balanceada)
            Console.WriteLine("Resultado: Formula balanceada");
        else
            Console.WriteLine("Resultado: Formula NO balanceada");
    }

    static bool VerificarBalanceo(string expresion)
    {
        // Crear una pila para almacenar los simbolos de apertura
        Stack<char> pila = new Stack<char>();
        foreach (char c in expresion)
        {
            // Si es un simbolo de apertura, agregar a la pila
            if (c == '(' || c == '{' || c == '[')
            {
                pila.Push(c);
            }
            // Si es un simbolo de cierre, verificar con la pila
            else if (c == ')' || c == '}' || c == ']')
            {
                // Si la pila esta vacia, no hay apertura correspondiente
                if (pila.Count == 0) return false;
                char ultimoAbierto = pila.Pop();

                // Verificar que el simbolo de cierre corresponda
                if (!SonPareja(ultimoAbierto, c))
                {
                    return false;
                }
            }
        }
        // Si la pila quedó vacía, todo se cerró correctamente
        return pila.Count == 0;
    }

    // Función auxiliar para comparar parejas
    static bool SonPareja(char apertura, char cierre)
    {
        if (apertura == '(' && cierre == ')') return true;
        if (apertura == '{' && cierre == '}') return true;
        if (apertura == '[' && cierre == ']') return true;
        return false;
    }
}
        
                

        