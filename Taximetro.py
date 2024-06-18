
import time

class Taximetro:
  """Clase que simula el funcionamiento de un taxímetro."""

  def __init__(self):
    """Inicializa las variables de la clase."""
    self.tiempo_parado = 0
    self.tiempo_movimiento = 0
    self.tarifa_parado = 0
    self.tarifa_movimiento = 0
    self.tarifa_total = 0
    self.tarifa_base = 2.5
  
  def iniciar_carrera(self):
    print ("Inicia la carrera del taxi.")
    input("Presiona Enter para iniciar la carrera: ")
    self.tiempo_inicio = time.time()

  def actualizar_estado(self, estado_taxi):
    """Actualiza el estado del taxi (en movimiento o parado)."""
    estado_taxi = estado_taxi.lower()
    if estado_taxi == "m":
      self.actualizar_movimiento()
    elif estado_taxi == "p":
      self.actualizar_parado()
    else:
      print("Fin de la carrera.")

  def actualizar_movimiento(self):
    """Actualiza el tiempo y la tarifa en movimiento."""
    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
    self.tiempo_movimiento += tiempo_transcurrido
    self.tarifa_movimiento += tiempo_transcurrido * 0.05
    self.tiempo_inicio = tiempo_actual

  def actualizar_parado(self):
    """Actualiza el tiempo y la tarifa parado."""
    tiempo_actual = time.time()
    self.tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
    self.tiempo_parado += self.tiempo_transcurrido
    self.tarifa_parado += self.tiempo_transcurrido * 0.02
    self.tiempo_inicio = tiempo_actual

  def finalizar_carrera(self):
    """Calcula y muestra la tarifa total de la carrera."""
    self.tarifa_total = self.tarifa_parado + self.tarifa_movimiento + self.tarifa_base
    print(f"El tiempo transcurrido fue de: {round(self.tiempo_transcurrido,2)} y la tarifa total de la carrera es de: {self.tarifa_total:.2f} €")

def main():
  """Función principal que crea y utiliza la clase Taximetro."""
  taximetro = Taximetro()
  taximetro.iniciar_carrera()

  while True:
    estado_taxi = input("¿El taxi está en movimiento (m), parado (p) o finalizar (f)? ")
    taximetro.actualizar_estado(estado_taxi)

    if estado_taxi not in ("m", "p"):
      break

  taximetro.finalizar_carrera()

if __name__ == "__main__":
  main()