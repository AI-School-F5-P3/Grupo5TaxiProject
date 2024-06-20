import unittest
from unittest.mock import patch, MagicMock
import time
from Taximetro import Taximetro, ahora

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

    def test_mover(self):
        self.taximetro.iniciar()
        self.taximetro.mover()
        self.assertTrue(self.taximetro.en_marcha)
        self.assertTrue(self.taximetro.en_movimiento)
        self.taximetro.logger.info.assert_called_with("El taxi se ha puesto en marcha.")
        self.assertEqual(len(self.taximetro.messages), 2)

if __name__ == '__main__':
    unittest.main()
