import socket

ADDRESS = 'localhost'
PORT = 3333

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ADDRESS, PORT))

try:
    while True:
        # Recibir datos de distancia del servidor
        received = sock.recv(1024).decode('utf-8')
        if received:
            distancia = int(received)
            print(f"Distancia recibida: {distancia} cm")
            
            # Enviar mensaje de frenado automático si la distancia es menor a 5
            if distancia < 7:
                to_send = "Frenado Automático Activado"
            else:
                to_send = "Distancia segura"
            
            sock.send(to_send.encode('utf-8'))
            print(f"Sent to server: {to_send}")

except KeyboardInterrupt:
    print("Exiting app...")
except Exception as e:
    print(f"Something has happened {e}")
finally:
    sock.close()
