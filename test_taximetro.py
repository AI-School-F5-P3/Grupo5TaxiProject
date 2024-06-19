import unittest
from Taximetro import Taximetro  # Asumiendo que tu clase Taximetro está en un archivo llamado Taximetro.py

class TestTaximetro(unittest.TestCase):

    def setUp(self):
        self.taximetro = Taximetro()  # Inicializar una nueva instancia de Taximetro antes de cada test

    def test_mover(self):
        print("Test: Verificando que en_marcha sea False al inicio")
        self.assertFalse(self.taximetro.en_marcha)

        print("Test: Llamar al método iniciar")
        self.taximetro.iniciar()

        print("Test: Verificando que en_marcha sea True después de iniciar")
        self.assertTrue(self.taximetro.en_marcha)

        print("Test: Verificando que en_movimiento sea False al inicio")
        self.assertFalse(self.taximetro.en_movimiento)

        print("Test: Llamar al método mover")
        self.taximetro.mover()

        print("Test: Verificando que en_movimiento sea True después de mover")
        self.assertTrue(self.taximetro.en_movimiento)

if __name__ == "__main__":
    unittest.main()
