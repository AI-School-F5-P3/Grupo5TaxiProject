import unittest
from unittest.mock import patch, MagicMock
import time
from datetime import datetime
import streamlit as st
from Taximetro import Taximetro

class TestTaximetro(unittest.TestCase):

    def setUp(self):
        # Inicializar Streamlit session_state para simulación
        st.session_state = MagicMock()
        st.session_state.messages = []

        # Crear una instancia de Taximetro para cada prueba
        self.taximetro = Taximetro()

    def test_mover(self):
        # Simular que el taxímetro está en marcha pero no en movimiento
        self.taximetro.en_marcha = True
        self.taximetro.en_movimiento = False
        self.taximetro.hora_inicio = time.time()

        # Simular tiempo falso para el patch
        fake_time = self.taximetro.hora_inicio + 60  # 60 segundos después
        with patch('time.time', return_value=fake_time):
            # Llamar a mover
            self.taximetro.mover()

            # Verificar el estado después de llamar a mover
            self.assertTrue(self.taximetro.en_movimiento)
            self.assertEqual(self.taximetro.ultima_hora, fake_time)

            # Verificar los mensajes en session_state
            self.assertIn("El taxi se ha puesto en marcha.", st.session_state.messages)

    def test_parar(self):
        # Implementar si es necesario
        pass

    def test_finalizar_carrera(self):
        # Implementar si es necesario
        pass

if __name__ == '__main__':
    unittest.main()