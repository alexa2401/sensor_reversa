import socket
import serial
import time
import RPi.GPIO as GPIO

# Configuración del LED en la Raspberry Pi
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Configuración de la conexión serial
PORT_ARDUINO = "/dev/ttyACM0"
BAUDRATE_ARDUINO = 9600

arduino = serial.Serial(port=PORT_ARDUINO, baudrate=BAUDRATE_ARDUINO, timeout=2.)

ADDRESS = '0.0.0.0'
PORT = 3333

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ADDRESS, PORT))
sock.listen()

print(f"[*] Listening on {ADDRESS}:{PORT}")

try:
    while True:
        connection, address = sock.accept()
        print(f"Accepted connection from {address}")
        
        try:
            while True:
                # Leer datos del Arduino
                if arduino.in_waiting > 0:
                    data = arduino.readline().decode('utf-8').strip()
                    if data.startswith("Distancia: "):
                        distancia = int(data.split()[1])
                        message = f"{distancia}"
                        connection.send(message.encode('utf-8'))
                        print(f"Sent to client: {message}")
                        time.sleep(1)  # Espera opcional para no saturar la conexión

                # Recibir respuesta del cliente
                received = connection.recv(1024).decode('utf-8')
                if received:
                    print(f"Received from client: {received}")
                    if received == "Frenado Automático Activado":
                        GPIO.output(LED_PIN, GPIO.HIGH)
                    else:
                        GPIO.output(LED_PIN, GPIO.LOW)
        finally:
            connection.close()

except KeyboardInterrupt:
    print("Exiting app...")
except Exception as e:
    print(f"Something has happened {e}")
finally:
    sock.close()
    GPIO.cleanup()
