import serial
import threading
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import time

# Configuración de la conexión serial
PORT = "/dev/ttyACM0"
BAUDRATE = 9600

arduino = serial.Serial(port = PORT, baudrate = BAUDRATE, timeout= 2.)

class SensorReversaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensor de Reversa")
        
       # Crear un canvas para dibujar el auto y el indicador
        self.canvas = Canvas(root, width=400, height=400)
        self.canvas.pack()

        # Cargar la imagen de fondo y escalarla al tamaño del canvas
        self.bg_image = Image.open("bg.png")
        self.bg_image = self.bg_image.resize((400, 400), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        
        # Dibujar la imagen de fondo
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        
        # Cargar la imagen y escalarla a las dimensiones deseadas
        self.car_image = Image.open("car.png")
        self.car_image = self.car_image.resize((50, 100), Image.ANTIALIAS)  # Escalar la imagen
        self.car_image = ImageTk.PhotoImage(self.car_image)  # Convertir la imagen a un formato compatible con tkinter
        
        # Dibujar la imagen del auto
        self.auto = self.canvas.create_image(
            175, 150, anchor=tk.NW, image=self.car_image
        )
        
        # Dibujar el indicador (media luna) justo debajo del auto
        self.indicador = self.canvas.create_arc(
            150, 200, 245, 300, start=0, extent=-180, fill="green"
        )
        
        # Etiqueta para mostrar la distancia
        self.distancia_label = tk.Label(root, text="Distancia: --- cm")
        self.distancia_label.pack()
        
        # Variable para rastrear la última vez que se recibieron datos
        self.last_data_time = time.time()
        
        # Iniciar la lectura de datos seriales
        self.iniciar_lectura_serial()
        
        # Comprobar periódicamente si se han recibido datos
        self.check_for_data()
        
    def actualizar_indicador(self, distancia):
        # Actualizar el color del indicador basado en la distancia
        if distancia < 10:
            color = "red"  # Rojo
        elif distancia < 30:
            color = "yellow"  # Amarillo
        else:
            color = "green"  # Verde
        self.canvas.itemconfig(self.indicador, fill=color)
        self.distancia_label.config(text=f"Distancia: {distancia} cm")
        print(f"Distancia actualizada: {distancia} cm")  # Mensaje de depuración

    def iniciar_lectura_serial(self):
        thread = threading.Thread(target=self.leer_datos_serial)
        thread.daemon = True
        thread.start()
        
    def leer_datos_serial(self):
        while True:
            if arduino.in_waiting > 0:
                try:
                    data = arduino.readline().decode('utf-8').strip()
                    print(f"Datos recibidos: {data}")  # Mensaje de depuración
                    if data.startswith("Distancia: "):
                        try:
                            distancia = int(data.split()[1])
                            self.last_data_time = time.time()  # Actualizar la última vez que se recibieron datos
                            self.root.after(0, self.actualizar_indicador, distancia)
                        except (IndexError, ValueError) as e:
                            print(f"Error al procesar los datos: {e}")  # Mensaje de depuración
                except serial.SerialException as e:
                    print(f"Error de lectura serial: {e}")  # Mensaje de depuración
            time.sleep(0.1)
    
    def check_for_data(self):
        current_time = time.time()
        # Si no se han recibido datos en los últimos 2 segundos, mostrar "Auto parado"
        if current_time - self.last_data_time > 2:
            self.distancia_label.config(text="Auto parado")
            self.canvas.itemconfig(self.indicador, fill="grey")
        
        # Comprobar de nuevo en 500 ms
        self.root.after(500, self.check_for_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = SensorReversaApp(root)
    root.mainloop()