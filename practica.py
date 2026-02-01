import threading
import time
import os

def tarea_cpu(nombre, duracion):
    """Simula una tarea intensiva de CPU."""
    pid = os.getpid()
    print(f"[{nombre}] Iniciando en proceso PID: {pid}")
    start_time = time.time()
    
    # Simulación de carga de trabajo
    while time.time() - start_time < duracion:
        pass  # Bucle vacío para consumir CPU
        
    print(f"[{nombre}] Finalizada después de {duracion} segundos.")

def tarea_io(nombre, duracion):
    """Simula una tarea de entrada/salida (espera)."""
    pid = os.getpid()
    print(f"[{nombre}] Iniciando en proceso PID: {pid}")
    time.sleep(duracion) # Simula espera (descarga, lectura de disco)
    print(f"[{nombre}] Finalizada.")

if __name__ == "__main__":
    print(f"--- Proceso Principal (Main) PID: {os.getpid()} ---")
    print("Presiona ENTER para iniciar los hilos...")
    input()

    # Creación de los hilos
    hilo1 = threading.Thread(target=tarea_cpu, args=("Hilo-CPU", 15)) # 15 segundos de carga
    hilo2 = threading.Thread(target=tarea_io, args=("Hilo-IO", 15))  # 15 segundos de espera

    print("Iniciando hilos...")
    hilo1.start()
    hilo2.start()

    print("Hilos en ejecución.")
    
    # Esperar a que terminen
    hilo1.join()
    hilo2.join()
    
    print("--- Todos los hilos han terminado ---")
    input("Presiona ENTER para salir.")