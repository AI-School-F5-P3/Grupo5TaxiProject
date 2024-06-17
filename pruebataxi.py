import time

def iniciar_carrera():
    print("La carrera ha comenzado.")
    return time.time()

def parar_taxi(inicio):
    fin = time.time()
    duracion = fin - inicio
    print("El taxi se ha parado.")
    return duracion

def arrancar_taxi(inicio):
    fin = time.time()
    duracion = fin - inicio
    print("El taxi ha arrancado.")
    return duracion

def calcular_tarifa(duracion, en_movimiento):
    if en_movimiento:
        tarifa = duracion * 0.05
    else:
        tarifa = duracion * 0.02
    return tarifa

inicio = input("Presiona ENTER para iniciar la carrera.")
tiempo_inicio = iniciar_carrera()

tarifa_total = 0

while True:
    accion = input("Presiona ENTER para parar el taxi, escribe 'arrancar' y presiona ENTER para arrancar el taxi, o escribe 'terminar' y presiona ENTER para terminar la carrera.")
    if accion == "arrancar":
        tiempo_parado = parar_taxi(tiempo_inicio)
        tarifa_parado = calcular_tarifa(tiempo_parado, False)
        tarifa_total += tarifa_parado
        tiempo_inicio = time.time()
    elif accion == "terminar":
        tiempo_movimiento = arrancar_taxi(tiempo_inicio)
        tarifa_movimiento = calcular_tarifa(tiempo_movimiento, True)
        tarifa_total += tarifa_movimiento
        break
    else:
        tiempo_movimiento = arrancar_taxi(tiempo_inicio)
        tarifa_movimiento = calcular_tarifa(tiempo_movimiento, True)
        tarifa_total += tarifa_movimiento
        tiempo_inicio = time.time()

print("La tarifa total de la carrera es: ", tarifa_total, "Euros")