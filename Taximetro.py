import time

from datetime import datetime
import streamlit as st

class Taximetro:
    """Clase que simula el funcionamiento de un taxímetro."""

  
    def __init__(self):
        self.tarifa_por_minuto_movimiento =  3
        self.tarifa_por_minuto_parado =  1.2
        self.tarifa_base =  2.5
        self.reset()

    def reset(self):
        self.en_marcha = False
        self.en_movimiento = False
        self.tarifa_total = 0
        self.hora_inicio = None
        self.ultima_hora = None
        self.tiempo_movimiento = 0
        self.tiempo_parado = 0

    def iniciar(self):
        # Comienza la carrera en estado parado, ya tarifica 
        self.en_marcha = True
        self.en_movimiento = False
        self.hora_inicio = time.time()
        self.ultima_hora = self.hora_inicio
        st.session_state.messages.append(f"{ahora()} - Inicia la carrera del taxi.")
        
    def mover(self):
        if self.en_marcha and not self.en_movimiento:
            self.actualizar_tarifa()
            self.en_movimiento = True
            self.ultima_hora = time.time()
            st.session_state.messages.append(f"{ahora()} - El taxi se ha puesto en marcha.")

    def parar(self):
        if self.en_marcha and self.en_movimiento:
            self.actualizar_tarifa()
            self.en_movimiento = False
            self.ultima_hora = time.time()
            st.session_state.messages.append(f"{ahora()} - El taxi se ha parado.")

    def finalizar_carrera(self):
        if self.en_marcha:
            self.actualizar_tarifa()
            st.session_state.tarifa_final = self.tarifa_total+ self.tarifa_base  # Guardar la tarifa final en session_state
            st.session_state.messages.append(
                f"{ahora()} - Carrera finalizada. Tiempo de marcha y paro : {self.tiempo_movimiento + self.tiempo_parado :.2f} segundos, Importe total: {st.session_state.tarifa_final:.2f} €")
            self.reset()
        else:
            st.session_state.messages.append(f"{ahora()} - No hay carrera en curso para finalizar.")

    def actualizar_tarifa(self):
        hora_actual = time.time()
        if self.en_marcha:
            tiempo_transcurrido = hora_actual - self.ultima_hora
            if self.en_movimiento:
                self.tiempo_movimiento += tiempo_transcurrido
                self.tarifa_total += tiempo_transcurrido * (self.tarifa_por_minuto_movimiento / 60)
            else:
                self.tiempo_parado += tiempo_transcurrido
                self.tarifa_total += tiempo_transcurrido * (self.tarifa_por_minuto_parado / 60)
            self.ultima_hora = hora_actual

    def actualizar_precios(self, nueva_tarifa_por_minuto_movimiento, nueva_tarifa_por_minuto_parado, nueva_tarifa_base):
        self.tarifa_por_minuto_movimiento = nueva_tarifa_por_minuto_movimiento
        self.tarifa_por_minuto_parado = nueva_tarifa_por_minuto_parado
        self.tarifa_base = nueva_tarifa_base
        self.reset()
       
        st.session_state.messages.append(f"{ahora()} - Precios actualizados: Movimiento €{self.tarifa_por_minuto_movimiento}/min, Parado €{self.tarifa_por_minuto_parado}/min, Base €{self.tarifa_base}.")


def ahora():
    ahora = datetime.now()
    hora_actual = ahora.strftime("%H:%M:%S")
    return hora_actual

def limpiar_mensajes():
    st.session_state.messages = []

def main():
     
    st.markdown(
        """
        <h1 style='text-align: center;'>Taxímetro - G5</h1>
        """, 
        unsafe_allow_html=True
    )
    
    # Menú desplegable en la barra lateral
    menu_options = [ "Seleccione Opción", "Cambiar Precios", "Ver Log", "Ayuda"]
    menu_selection = st.sidebar.selectbox("Menú", menu_options)

    if 'taximetro' not in st.session_state:
        st.session_state.taximetro = Taximetro()
        st.session_state.messages = []
        st.session_state.tarifa_final = 0.0  # Inicializar la variable para la tarifa final
    
    #Opción del menú para actualizar los Precios
    if menu_selection == "Cambiar Precios":
        nueva_tarifa_por_minuto_movimiento = st.number_input("Nueva Tarifa por Minuto en Movimiento (€)", value=st.session_state.taximetro.tarifa_por_minuto_movimiento)
        nueva_tarifa_por_minuto_parado = st.number_input("Nueva Tarifa por Minuto Parado (€)", value=st.session_state.taximetro.tarifa_por_minuto_parado)
        nueva_tarifa_base = st.number_input("Nueva Tarifa Base (€)", value=st.session_state.taximetro.tarifa_base)

        if st.button("Actualizar Precios"):
            st.session_state.taximetro.actualizar_precios(nueva_tarifa_por_minuto_movimiento, nueva_tarifa_por_minuto_parado, nueva_tarifa_base)


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Iniciar Carrera"):
            st.session_state.taximetro.iniciar()

    with col2:
        if st.button("Taxi en movimiento"):
            st.session_state.taximetro.mover()

    with col3:
        if st.button("Taxi parado"):
            st.session_state.taximetro.parar()

    with col4:
        if st.button("Finalizar Carrera"):
            st.session_state.taximetro.finalizar_carrera()

    # Mostrar mensajes
    st.text_area("Mensajes", value="\n".join(st.session_state.messages), height=200)

    # Mostrar tarifa total dinámicamente
    st.text(f"Tarifa Total: €{st.session_state.tarifa_final:.2f}")

if __name__ == "__main__":
    main()
