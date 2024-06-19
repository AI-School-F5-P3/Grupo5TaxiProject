import time
from datetime import datetime
import streamlit as st
import logging

class Taximetro:
    """Clase que simula el funcionamiento de un taxímetro."""

  
    def __init__(self):
        self.tarifa_por_minuto_movimiento = 3.0
        self.tarifa_por_minuto_parado = 1.2
        self.tarifa_base = 2.5
        self.reset()
        logger.info ("Taxímetro inicializando con tarifas base.")
        logger.info ("Taxímetro inicializando con tarifas base.")

    def reset(self):
        self.en_marcha = False
        self.en_movimiento = False
        self.tarifa_total = 0
        self.tarifa_total = 0
        self.hora_inicio = None
        self.ultima_hora = None
        self.tiempo_movimiento = 0
        self.tiempo_parado = 0
        logger.info ("Taxímetro restablecido.")


    def iniciar(self):
        # Comienza la carrera en estado parado, ya tarifica 
        self.en_marcha = True
        self.en_movimiento = False
        self.hora_inicio = time.time()
        self.ultima_hora = self.hora_inicio
        st.session_state.messages.append(f"{ahora()} - Inicia la carrera del taxi.")
        logger.info ("Carrera iniciada.")
        logger.info ("Carrera iniciada.")
        
    def mover(self):
        if self.en_marcha and not self.en_movimiento:
            self.actualizar_tarifa()
            self.en_movimiento = True
            self.ultima_hora = time.time()
            st.session_state.messages.append(f"{ahora()} - El taxi se ha puesto en marcha.")
            logger.info ("El taxi se ha puesto en marcha.")
            logger.info ("El taxi se ha puesto en marcha.")

    def parar(self):
        if self.en_marcha and self.en_movimiento:
            self.actualizar_tarifa()
            self.en_movimiento = False
            self.ultima_hora = time.time()
            st.session_state.messages.append(f"{ahora()} - El taxi se ha parado.")
            logger.info ("El taxi se ha parado.")
           

    def finalizar_carrera(self):
        if self.en_marcha:
            self.actualizar_tarifa()
            st.session_state.tarifa_final = self.tarifa_total + self.tarifa_base # cambio al actualizar precios
            st.session_state.messages.append(f"{ahora()} - Carrera finalizada. Tiempo de marcha y paro : {self.tiempo_movimiento + self.tiempo_parado :.2f} segundos, Importe total: {st.session_state.tarifa_final:.2f} €")
            logger.info(f"Carrera finalizada. Importe total:{self.tarifa_total:.2f} €") 
            self.reset()
        else:
            st.session_state.messages.append(f"{ahora()} - No hay carrera en curso para finalizar.")
            logger.warning("Intento de finalizar una carrera que no está en curso")


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
            logger.info ("Tarifa actualizada.")

    def cambiar_precios(self, nueva_tarifa_por_minuto_movimiento, nueva_tarifa_por_minuto_parado, nueva_tarifa_base):
            self.tarifa_por_minuto_movimiento = nueva_tarifa_por_minuto_movimiento
            self.tarifa_por_minuto_parado = nueva_tarifa_por_minuto_parado
            self.tarifa_base = nueva_tarifa_base
            logger.info ("Actualización de tarifas realizada.")
            self.reset()  # Llamar a reset después de cambiar las tarifas
            st.session_state.messages.append(f"{ahora()} - Precios actualizados: Movimiento €{self.tarifa_por_minuto_movimiento}/min, Parado €{self.tarifa_por_minuto_parado}/min, Base €{self.tarifa_base}.")
            

# Funcion para el log.
def get_logger():
    # Crear un logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Crear un manejador para la terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # Crear un manejador para el archivo de log
    file_handler = logging.FileHandler('taximetro.log')
    file_handler.setLevel(logging.INFO)

    # Formato del logging
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Añadir los manejadores al logger
    if not logger.handlers:
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger

logger = get_logger()



def leer_log():
    try:
        with open('taximetro.log', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "No se encontró el archivo de log."


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
    menu_options = ["Taxímetro", "Login", "Cambiar Precios", "Ver Log", "Ayuda"]
    menu_selection = st.sidebar.selectbox("Menú", menu_options)
    logger.info(f"Menu seleccionado: {menu_selection}")

    if 'taximetro' not in st.session_state:
        st.session_state.taximetro = Taximetro()
        st.session_state.messages = []
        st.session_state.tarifa_final = 0.0  # Inicializar la variable para la tarifa final
        st.session_state.logged_in = False  # Estado de login

    if not st.session_state.logged_in:
        if menu_selection == "Login":
            with st.form("form_login"):
                usuario = st.text_input("Usuario")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button(label="Login")
                if submit_button:
                    if usuario == "user" and password == "password":
                        st.session_state.logged_in = True
                        st.success("Login realizado con éxito")
                    else:
                        st.session_state.logged_in = False
                        st.error("Usuario o password incorrectos")
        else:
            html_warning = """
            <div style='display: flex; justify-content: center; align-items: center; height: 50vh;'>
                <div style='font-size:  xx-large; color: black; text-align: center;'>
                    <p>Bienvenido al Taxímetro de Precisión.</p>
                    <p>Debe realizar login para utilizar el Taxímetro.</p>
                    <p>Para detalles del funcionamiento elija la opción Ayuda.</p>
                </div>
            </div>
            """
            st.markdown(html_warning, unsafe_allow_html=True)


    else:
        if menu_selection == "Cambiar Precios":
            with st.form("form_cambiar_precios"):
                nueva_tarifa_movimiento = st.number_input("Nueva Tarifa por Minuto en Movimiento (€)", min_value=0.0, value=float(st.session_state.taximetro.tarifa_por_minuto_movimiento))
                nueva_tarifa_parado = st.number_input("Nueva Tarifa por Minuto Parado (€)", min_value=0.0, value=float(st.session_state.taximetro.tarifa_por_minuto_parado))
                nueva_tarifa_base = st.number_input("Nueva Tarifa Base (€)", min_value=0.0, value=float(st.session_state.taximetro.tarifa_base))
                submit_button = st.form_submit_button(label="Actualizar Tarifas")
                if submit_button:
                    st.session_state.taximetro.cambiar_precios(nueva_tarifa_movimiento, nueva_tarifa_parado, nueva_tarifa_base)
                    st.success("Tarifas actualizadas correctamente.")
        

        elif menu_selection == "Ayuda":
            html_ayuda = """
                <div style='font-size:xx-large; color:black;'>
                    <h2>Ayuda</h2>
                    <ul>
                    <li><b>Iniciar Carrera:</b> Comienza la carrera en estado parado.</li>
                    <li><b>Taxi en Movimiento:</b> Indica que el taxi se ha puesto en marcha.</li>
                    <li><b>Taxi Parado:</b> Indica que el taxi se ha detenido.</li>
                    <li><b>Finalizar Carrera:</b> Finaliza la carrera y calcula el total.</li>
                    <li><b>Cambiar Precios:</b> Permite actualizar las tarifas base, por minuto en movimiento y por minuto parado.</li>
                    <li><b>Ver Log:</b> Muestra el registro de todas las actividades realizadas</li>
                    </ul>             
                </div>
            """
            st.markdown(html_ayuda, unsafe_allow_html=True)
            
        elif menu_selection == "Ver Log":
            # Mostrar el contenido del log en una sección separada
            st.markdown("### Log del Sistema")
            st.text_area("Log del sistema", value=leer_log(), height=200)

        else:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("Iniciar Carrera"):
                    st.session_state.taximetro.iniciar()
                    logger.info ("Botón 'Iniciar Carrera' presionado.")

            with col2:
                if st.button("Taxi en movimiento"):
                    st.session_state.taximetro.mover()
                    logger.info ("Botón 'Taxi en movimiento' presionado.")

            with col3:
                if st.button("Taxi parado"):
                    st.session_state.taximetro.parar()
                    logger.info ("Botón 'Taxi parado' presionado.")

            with col4:
                if st.button("Finalizar Carrera"):
                    st.session_state.taximetro.finalizar_carrera()
                    logger.info ("Botón 'Finalizar carrera' presionado.")

            # Mostrar mensajes
            st.text_area("Mensajes", value="\n".join(st.session_state.messages), height=200)

            # Mostrar tarifa total dinámicamente
            st.text(f"Tarifa Total: €{st.session_state.tarifa_final:.2f}")

if __name__ == "__main__":
    main()
