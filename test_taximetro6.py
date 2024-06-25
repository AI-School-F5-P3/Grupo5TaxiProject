import unittest
from unittest.mock import patch
from taxi_meter2 import Taximetro

class TestTaximetro(unittest.TestCase):

    def setUp(self):
        self.taximetro = Taximetro()

    def test_actualizar_tarifa_movimiento(self):
        with patch('time.time') as mock_time:
            mock_time.side_effect = [1000, 1005, 1010]
            
            self.taximetro.iniciar()
            self.taximetro.mover()
            self.taximetro.actualizar_tarifa()
            
            # Calcular tarifa esperada (tarifa base + tarifa por movimiento)
            tarifa_esperada = self.taximetro.tarifa_base + ((5 - 0) * self.taximetro.tarifa_por_minuto_movimiento / 60)
            
            self.assertAlmostEqual(self.taximetro.tarifa_total, tarifa_esperada, places=2)

    def test_actualizar_tarifa_parado(self):
        with patch('time.time') as mock_time:
            mock_time.side_effect = [1000, 1005, 1010, 1020]
            
            self.taximetro.iniciar()
            self.taximetro.mover()
            self.taximetro.actualizar_tarifa()
            
            # Simular tiempo parado
            self.taximetro.parar()
            self.taximetro.actualizar_tarifa()
            
            # Calcular tarifa esperada (tarifa base + tarifa por movimiento + tarifa por parado)
            tiempo_movimiento = (5 - 0)
            tiempo_parado = (10 - 5)
            tarifa_esperada = self.taximetro.tarifa_base + (tiempo_movimiento * self.taximetro.tarifa_por_minuto_movimiento / 60) + (tiempo_parado * self.taximetro.tarifa_por_minuto_parado / 60)
            
            self.assertAlmostEqual(self.taximetro.tarifa_total, tarifa_esperada, places=2)

if __name__ == '__main__':
    unittest.main()
