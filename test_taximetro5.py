import unittest
from datetime import datetime, timedelta
from taxi_meter2 import Taximetro

class TestTaximetro(unittest.TestCase):

    def setUp(self):
        self.taximetro = Taximetro()
    
    def avanzar_tiempo(self, segundos):
        # Avanza el tiempo interno del taxímetro
        self.taximetro.ultima_hora -= segundos

    def test_actualizar_tarifa_movimiento(self):
        # Iniciar carrera y poner en movimiento
        self.taximetro.iniciar()
        self.taximetro.mover()

        # Avanzar tiempo manualmente
        self.avanzar_tiempo(60)  # Simular 1 minuto de movimiento

        # Actualizar tarifa
        self.taximetro.actualizar_tarifa()

        # Calcular tarifa esperada (sin incluir tarifa base)
        tarifa_movimiento = 60 * (self.taximetro.tarifa_por_minuto_movimiento / 60)
        tarifa_esperada = tarifa_movimiento
        
        # Verificar tarifa actualizada
        self.assertAlmostEqual(self.taximetro.tarifa_total, tarifa_esperada, places=2)

    def test_actualizar_tarifa_parado(self):
        # Iniciar carrera y poner en movimiento
        self.taximetro.iniciar()
        self.taximetro.mover()

        # Avanzar tiempo manualmente
        self.avanzar_tiempo(60)  # Simular 1 minuto de movimiento
        self.taximetro.actualizar_tarifa()

        self.taximetro.parar()

        # Avanzar tiempo manualmente
        self.avanzar_tiempo(60)  # Simular 1 minuto parado

        # Actualizar tarifa
        self.taximetro.actualizar_tarifa()

        # Calcular tarifa esperada (sin incluir tarifa base)
        tarifa_movimiento = 60 * (self.taximetro.tarifa_por_minuto_movimiento / 60)
        tarifa_parado = 60 * (self.taximetro.tarifa_por_minuto_parado / 60)
        tarifa_esperada = tarifa_movimiento + tarifa_parado

        # Verificar tarifa actualizada
        self.assertAlmostEqual(self.taximetro.tarifa_total, tarifa_esperada, places=2)

if __name__ == '__main__':
    unittest.main()
