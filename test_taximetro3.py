import unittest
from unittest.mock import MagicMock, patch
from taxi_meter import Taximetro  


class TestTaximetro(unittest.TestCase):
    def setUp(self):
        self.taximetro = Taximetro()
        self.taximetro.logger = MagicMock()
        

    def test_iniciar(self):
        self.taximetro.iniciar()
        self.assertTrue(self.taximetro.en_marcha)
        self.assertFalse(self.taximetro.en_movimiento)
        self.assertIsNotNone(self.taximetro.hora_inicio)
        self.assertEqual(len(self.taximetro.messages), 1)
        self.assertIn("Inicia la carrera del taxi", self.taximetro.messages[0])

    def test_mover(self):
        self.taximetro.iniciar()
        self.taximetro.mover()
        self.assertTrue(self.taximetro.en_marcha)
        self.assertTrue(self.taximetro.en_movimiento)
        self.taximetro.logger.info.assert_called_with("El taxi se ha puesto en marcha.")
        self.assertEqual(len(self.taximetro.messages), 2)
        self.assertIn("El taxi se ha puesto en marcha", self.taximetro.messages[1])

    def test_parar(self):
        self.taximetro.iniciar()
        self.taximetro.mover()
        self.taximetro.parar()
        self.assertTrue(self.taximetro.en_marcha)
        self.assertFalse(self.taximetro.en_movimiento)
        self.taximetro.logger.info.assert_called_with("El taxi se ha parado.")
        self.assertEqual(len(self.taximetro.messages), 2)  

    def test_finalizar_carrera(self):
        self.taximetro.iniciar()
        self.taximetro.finalizar_carrera()
        self.assertFalse(self.taximetro.en_marcha)
        self.assertFalse(self.taximetro.en_movimiento)
        self.taximetro.logger.info.assert_any_call(f"Carrera finalizada. Importe total: {self.taximetro.tarifa_total:.2f} €")
        self.taximetro.logger.info.assert_any_call("Taxímetro restablecido.")
        self.assertEqual(len(self.taximetro.messages), 1)  

    def test_cambiar_precios(self):
        nueva_tarifa_movimiento = 4.0
        nueva_tarifa_parado = 1.5
        nueva_tarifa_base = 3.0
        self.taximetro.cambiar_precios(nueva_tarifa_movimiento, nueva_tarifa_parado, nueva_tarifa_base)
        self.assertEqual(self.taximetro.tarifa_por_minuto_movimiento, nueva_tarifa_movimiento)
        self.assertEqual(self.taximetro.tarifa_por_minuto_parado, nueva_tarifa_parado)
        self.assertEqual(self.taximetro.tarifa_base, nueva_tarifa_base)
        self.taximetro.logger.info.assert_any_call("Actualización de tarifas realizada.")
        self.taximetro.logger.info.assert_any_call("Taxímetro restablecido.")

if __name__ == '__main__':
    unittest.main()
