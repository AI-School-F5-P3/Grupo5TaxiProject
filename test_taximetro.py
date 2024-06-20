import unittest
from unittest.mock import patch
import sys

# Añadir la ruta del directorio donde se encuentra el archivo Taximetro.py
sys.path.append(r'C:\Users\Administrator\Documents\TrabajoTaximetroGrupo5\Grupo5TaxiProject')

class TestTaximetro(unittest.TestCase):

    def setUp(self):
        from Taximetro import Taximetro  # Importar aquí para evitar problemas de importación circular
        self.taximetro = Taximetro()

    @patch('Taximetro.logging')
    def test_iniciar(self, logger_mock):
        # Prueba que el método iniciar cambia el estado a 'en marcha' y registra el mensaje correcto
        self.taximetro.iniciar()
        self.assertTrue(self.taximetro.en_marcha)
        self.assertFalse(self.taximetro.en_movimiento)
        logger_mock.info.assert_any_call("Carrera iniciada.")

    @patch('Taximetro.logging')
    def test_mover(self, logger_mock):
        # Prueba que el método mover cambia el estado a 'en movimiento' y registra el mensaje correcto
        self.taximetro.iniciar()  # Necesario para activar el taxímetro antes de moverlo
        self.taximetro.mover()
        self.assertTrue(self.taximetro.en_movimiento)
        logger_mock.info.assert_any_call("El taxi se ha puesto en marcha.")

    @patch('Taximetro.logging')
    def test_parar(self, logger_mock):
        # Prueba que el método parar cambia el estado a 'no en movimiento' y registra el mensaje correcto
        self.taximetro.iniciar()
        self.taximetro.mover()
        self.taximetro.parar()
        self.assertFalse(self.taximetro.en_movimiento)
        logger_mock.info.assert_any_call("El taxi se ha parado.")

    @patch('Taximetro.logging')
    def test_finalizar_carrera(self, logger_mock):
        # Prueba que el método finalizar_carrera resetea el taxímetro y registra el mensaje correcto
        self.taximetro.iniciar()
        self.taximetro.mover()
        self.taximetro.parar()
        self.taximetro.finalizar_carrera()
        self.assertFalse(self.taximetro.en_marcha)
        self.assertEqual(self.taximetro.tarifa_total, 0)
        logger_mock.info.assert_any_call("Carrera finalizada. Importe total:0.00 €")

    @patch('Taximetro.logging')
    def test_cambiar_precios(self, logger_mock):
        # Prueba que el método cambiar_precios actualiza las tarifas y registra el mensaje correcto
        nueva_tarifa_por_minuto_movimiento = 4.0
        nueva_tarifa_por_minuto_parado = 1.5
        nueva_tarifa_base = 3.0
        self.taximetro.cambiar_precios(nueva_tarifa_por_minuto_movimiento, nueva_tarifa_por_minuto_parado, nueva_tarifa_base)
        self.assertEqual(self.taximetro.tarifa_por_minuto_movimiento, nueva_tarifa_por_minuto_movimiento)
        self.assertEqual(self.taximetro.tarifa_por_minuto_parado, nueva_tarifa_por_minuto_parado)
        self.assertEqual(self.taximetro.tarifa_base, nueva_tarifa_base)
        logger_mock.info.assert_any_call("Actualización de tarifas realizada.")

if __name__ == '__main__':
    unittest.main()





