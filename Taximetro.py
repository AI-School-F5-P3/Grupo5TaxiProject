
import time
from datetime import datetime


#Proceso de Bienvenida:

def bienvenida_usuario():
    print("¡Bienvenido al Sistema Taxi Driver! Este programa le proporcionará el detalle de gasto y facturación de su recorrido")
    
bienvenida_usuario()


#Declaramos la clase Taximetro:
class Taximetro:
    def init(self, tarifa_base=2.50, tarifa_por_minuto_movimiento=0.50, tarifa_por_minuto_parado=0.20):
        self.tarifa_base = tarifa_base
        self.tarifa_por_minuto_movimiento = tarifa_por_minuto_movimiento
        self.tarifa_por_minuto_parado = tarifa_por_minuto_parado
        self.tiempo_transcurrido = tiempo_transcurrido

        
    def carrera(self):
        estado = int(input("Ingresar '1' para comenzar:"))
        Total = 0
        while estado == 1:
            taxi = "en movimiento"
            if taxi == "en movimiento":
                Total == self.tiempo_transcurrido * self.tarifa_por_minuto_movimiento
                print(f"El total de su carrera son: {Total} euros")
            else :
                Total == self.tiempo_transcurrido * self.tarifa_por_minuto_parado
                print(f"El total de su carrera son: {Total} euros")

  
    '''
    local_time=0
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    epoch_time = time.time()
    local_time = time.localtime(epoch_time)

    def ahora(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def iniciar(self):
        print("La carrera ha comenzado")
        self.inicio_carrera = self.ahora()
        print(f"El horario de inicio es: {self.inicio_carrera}")'''
    
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


    
