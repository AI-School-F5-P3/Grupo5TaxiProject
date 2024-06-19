import unittest
import Taximetro

class TestTaximetro(unittest.TestCase):
    def setUp(self):
        self.taximetro = Taximetro(test_mode=True)  # Inicializar una nueva instancia de Taximetro antes de cada test, con test_mode=True

    def test_mover(self):
        self.taximetro.iniciar()
        self.taximetro.mover(5)
        self.assertEqual(self.taximetro.distancia_recorrida, 5)
        self.assertEqual(self.taximetro.monto_total, 5.0)  # Assuming tarifa_por_km = 1.0

    def test_mover_logger(self):
        with unittest.mock.patch('logging.info') as logger_mock:
            self.taximetro.mover(3)
            logger_mock.info.assert_called_once_with("El taxi se ha movido 3 km.")

if __name__ == '__main__':
    unittest.main()



