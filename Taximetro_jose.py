import time
from datetime import datetime

#Proceso de Bienvenida:

def bienvenida_usuario():
    print("¡Bienvenido al Sistema Taxi Driver! Este programa le proporcionará el detalle de gasto y facturación de su recorrido")
    
bienvenida_usuario()

def ahora():
    ahora = datetime.now()
    hora_actual = ahora.strftime("%H:%M:%S")
    return hora_actual

#Declaramos la clase Taximetro:
class Taximetro:
    def init(self, tarifa_base=2.50, tarifa_por_minuto_movimiento=0.50, tarifa_por_minuto_parado=0.20):
        self.tarifa_base = tarifa_base
        self.tarifa_por_minuto_movimiento = tarifa_por_minuto_movimiento
        self.tarifa_por_minuto_parado = tarifa_por_minuto_parado


    def iniciar(self):
        self.corre_tiempo = True
        self.en_movimiento = False
        print("La carrera ha comenzado")
        self.inicio_carrera = time.time()
        print(f"La hora de inicio de la carrera es: {ahora()}")

    
    def detener(self):
        pass

    def mover(self):
        pass

    def parar(self):
        pass

    def actualizar_tarifa(self):
        pass



# Crear una instancia de la clase Taxímetro
carrera1 = Taximetro()
carrera1.iniciar()
