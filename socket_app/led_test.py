import RPi.GPIO as GPIO
import time

# Definir el número del pin que estás utilizando
pin_led_rojo = 18

# Configurar los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_led_rojo, GPIO.OUT)

try:
    while True:
        # Encender el LED rojo
        GPIO.output(pin_led_rojo, GPIO.HIGH)
        print("LED rojo encendido")
        time.sleep(1)  # Esperar 1 segundo
        
        # Apagar el LED rojo
        GPIO.output(pin_led_rojo, GPIO.LOW)
        print("LED rojo apagado")
        time.sleep(1)  # Esperar 1 segundo

except KeyboardInterrupt:
    # Limpiar los pines GPIO antes de salir
    GPIO.cleanup()
