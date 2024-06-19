import streamlit as st
from datetime import datetime
import logging

def ahora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Taximetro:
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.reset()

    def reset(self):
        self.tarifa_base = 1.5  # Tarifa base en euros
        self.tarifa_por_km = 1.0  # Tarifa por kilómetro en euros
        self.distancia_recorrida = 0.0
        self.tiempo_viaje = 0.0
        self.monto_total = 0.0
        if not self.test_mode:
            logging.info("Taxímetro restablecido.")
        self.iniciar_tarifas_base()

    def iniciar_tarifas_base(self):
        if not self.test_mode:
            logging.info("Taxímetro inicializando con tarifas base.")
        self.tarifa_base = 1.5  # Tarifa base en euros
        self.tarifa_por_km = 1.0  # Tarifa por kilómetro en euros

    def iniciar(self):
        if 'messages' not in st.session_state:
            st.session_state['messages'] = []
        st.session_state.messages.append(f"{ahora()} - Inicia la carrera del taxi.")
        if not self.test_mode:
            logging.info("Carrera iniciada.")

    def mover(self, distancia_km):
        self.distancia_recorrida += distancia_km
        self.monto_total += self.tarifa_por_km * distancia_km
        st.session_state.messages.append(f"{ahora()} - El taxi se movió {distancia_km} km. Monto total: {self.monto_total:.2f} euros.")
        if not self.test_mode:
            logging.info(f"El taxi se ha movido {distancia_km} km.")

