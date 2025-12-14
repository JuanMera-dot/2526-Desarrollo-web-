using System;

// Tarea: Clases para figuras geométricas
// Nombre: [Pon tu nombre aquí]
// Fecha: [Pon la fecha aquí]

public class Circulo
{
    // Datos primitivos encapsulados (privados)
    private double radio;

    // Constructor
    public Circulo(double r)
    {
        radio = r;
    }

    // CalcularArea es una función que devuelve un valor double, se utiliza para calcular el área de un circulo, 
    // requiere como argumento el radio del circulo que ya tenemos guardado.
    public double CalcularArea()
    {
        return Math.PI * radio * radio;
    }

    // CalcularPerimetro es una función que devuelve un valor double, calcula la longitud de la circunferencia.
    public double CalcularPerimetro()
    {
        return 2 * Math.PI * radio;
    }
}

public class Rectangulo
{
    // Variables privadas para encapsulamiento
    private double baseRect;
    private double alturaRect;

    // Constructor para dar valores iniciales
    public Rectangulo(double b, double h)
    {
        baseRect = b;
        alturaRect = h;
    }

    // CalcularArea es una función que devuelve un valor double, multiplica la base por la altura para sacar el área.
    public double CalcularArea()
    {
        return baseRect * alturaRect;
    }

    // CalcularPerimetro es una función que devuelve un valor double, suma todos los lados de la figura.
    public double CalcularPerimetro()
    {
        return (baseRect + alturaRect) * 2;
    }
}

class Program
{
    static void Main(string[] args)
    {
        // Prueba del Circulo
        Console.WriteLine("--- Resultados del Circulo ---");
        Circulo miCirculo = new Circulo(5.5); 
        
        double areaC = miCirculo.CalcularArea();
        double perimetroC = miCirculo.CalcularPerimetro();

        Console.WriteLine("Radio: 5.5");
        Console.WriteLine("El Area es: " + areaC);
        Console.WriteLine("El Perimetro es: " + perimetroC);

        Console.WriteLine(); // Espacio en blanco

        // Prueba del Rectangulo
        Console.WriteLine("--- Resultados del Rectangulo ---");
        Rectangulo miRectangulo = new Rectangulo(10, 4);

        double areaR = miRectangulo.CalcularArea();
        double perimetroR = miRectangulo.CalcularPerimetro();

        Console.WriteLine("Base: 10, Altura: 4");
        Console.WriteLine("El Area es: " + areaR);
        Console.WriteLine("El Perimetro es: " + perimetroR);

        // Para que no se cierre la consola inmediatamente
        Console.ReadKey();
    }
}