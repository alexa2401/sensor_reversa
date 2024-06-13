from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import serial
import threading
import time

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configuración de la conexión serial
PORT = "/dev/ttyACM0"
BAUDRATE = 9600

arduino = serial.Serial(port = PORT, baudrate = BAUDRATE, timeout= 2.)

def leer_datos_serial():
    global distancia_actual
    while True:
        if arduino.in_waiting > 0:
            try:
                data = arduino.readline().decode('utf-8').strip()
                if data.startswith("Distancia: "):
                    distancia = int(data.split()[1])
                    distancia_actual = distancia
            except Exception as e:
                print(f"Error de lectura serial: {e}")
        time.sleep(0.1)

@app.on_event("startup")
async def startup_event():
    threading.Thread(target=leer_datos_serial, daemon=True).start()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/distancia")
async def obtener_distancia():
    return {"distancia": distancia_actual}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
