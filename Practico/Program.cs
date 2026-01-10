using System;
using System.Collections.Generic;
using System.Linq;

namespace EjerciciosProgramacionC
{
    class Program
    {
        static void Main(string[] args)
        {
            
            Ejercicios profesor = new Ejercicios();

            // Llamar a los ejercicios
            profesor.Ejercicio8();
            // profesor.Ejercicio5();
            // profesor.Ejercicio6();
            // profesor.Ejercicio7();
            // profesor.Ejercicio8();
        }
    }

    class Ejercicios
    {
        // Ejercicio 4: Numero de loteria ordenados
        public void Ejercicio4()
        {
            Console.WriteLine("- Ejercicio 4: Loteria -");
            List<int> numeros = new List<int>();
            for (int i = 0; i < 6; i++)
            {
                Console.Write($"Ingrese el numero {i + 1}: ");
                numeros.Add(int.Parse(Console.ReadLine()));
            }
            numeros.Sort();
            Console.WriteLine("Numeros ganadores: " + string.Join(", ", numeros));
        }

        // Ejercicio 5: Numeros del 1 al 10 en orden inverso
        public void Ejercicio5()
        {
            Console.WriteLine("\n-- Ejercicio 5: Inverso del 1 al 10 --");
            List<int> Lista = Enumerable.Range(1, 10).ToList();
            Lista.Reverse();
            Console.WriteLine(string.Join(", ", Lista));
        }

        // Ejercicio 6: Asignaturas a repetir
        public void Ejercicio6()
        {
            Console.WriteLine("\n--- Ejercicio 6: Materias ---");
            List<string> materias = new List<string> { "Matematicas", "Fisica", "Quimica", "Historia", "Lengua" };
            List<string> repetir = new List<string>();

            foreach (string materia in materias)
            {
                Console.Write($"Que nota sacaste en {materia}?: ");
                double nota = double.Parse(Console.ReadLine());
                if (nota < 7)
                {
                    repetir.Add(materia);
                }
            }
            Console.WriteLine("Materias a repetir: " + string.Join(", ", repetir));
        }

        // Ejercicio 7: Abecedario eliminar multiplos de 3
        public void Ejercicio7()
        {
            Console.WriteLine("\n- Ejercicio 7: Abecedario -");
            List<char> abecedario = "abcdefghijklmnopqrstuvwxyz".ToCharArray().ToList();
            for (int i = abecedario.Count; i >= 1; i--)
            {
                if (i % 3 == 0)
                {
                    abecedario.RemoveAt(i - 1);
                }
            }
            Console.WriteLine("Lista resultante: " + string.Join("", abecedario));
        }

        // Ejercicio 8: palindromo
        public void Ejercicio8()
        {
            Console.WriteLine("\n- Ejercicio 8: Palindromo -");
            Console.Write("Introduce una palabra: ");
            string palabra = Console.ReadLine().ToLower();

            string invertida = new string(palabra.ToCharArray().Reverse().ToArray());

            if (palabra == invertida)
            {
                Console.WriteLine("Es un palindromo");
            }
            else
            {
                Console.WriteLine("No es un palindromo");
            }
        }
    }
}
