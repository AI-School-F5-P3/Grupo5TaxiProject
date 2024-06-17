
import time
from datetime import datetime

#Proceso de Bienvenida:

def bienvenida_usuario():
    print("¡Bienvenido al Sistema Taxi Driver! Este programa le proporcionará el detalle de gasto y facturación de su recorrido")
    
bienvenida_usuario()


#Declaramos la clase Taximetro:
class Taximetro:
    def __init__(self, tarifa_base=2.50, tarifa_por_minuto_movimiento=0.50, tarifa_por_minuto_parado=0.20):
        self.tarifa_base = tarifa_base
        self.tarifa_por_minuto_movimiento = tarifa_por_minuto_movimiento
        self.tarifa_por_minuto_parado = tarifa_por_minuto_parado

    def ahora(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def iniciar(self):
        print("La carrera ha comenzado")
        self.inicio_carrera = self.ahora()
        print(f"El horario de inicio es: {self.inicio_carrera}")
        print(f"La tarifa base es: {self.tarifa_base}")

    def mover(self, tiempo_movimiento):
        pass
        costo_movimiento = tiempo_movimiento * self.tarifa_por_minuto_movimiento
        print(f"Tiempo en movimiento: {tiempo_movimiento} minutos")
        print(f"Tarifa por movimiento: {costo_movimiento}")
         

    def parar(self,tiempo_parado):
        pass
        costo_parado = tiempo_parado * self.tarifa_por_minuto_movimiento
        print(f"Tiempo parado: {tiempo_parado} minutos")
        print(f"Tarifa parado: {costo_parado}")

    def detener(self):
        pass

    def actualizar_tarifa(self):
        pass



# Crear una instancia de la clase Taxímetro
carrera1 = Taximetro()
carrera1.iniciar()


    
