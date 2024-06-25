import time
from datetime import datetime
import logging

class Taximetro:
    """Clase que simula el funcionamiento de un taxímetro."""

    def __init__(self):
        self.tarifa_por_minuto_movimiento = 3.0
        self.tarifa_por_minuto_parado = 1.2
        self.tarifa_base = 2.5

        self.messages = []
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.info("Taxímetro inicializando con tarifas base.")
        self.reset()

    def reset(self):
        self.en_marcha = False
        self.en_movimiento = False
        self.tarifa_total = 0
        self.hora_inicio = None
        self.ultima_hora = None
        self.tiempo_movimiento = 0
        self.tiempo_parado = 0
        self.logger.info("Taxímetro restablecido.")

    def iniciar(self):
        self.en_marcha = True
        self.en_movimiento = False
        self.hora_inicio = time.time()
        self.ultima_hora = self.hora_inicio
        self.logger.info("Carrera iniciada.")
        self.add_message(f"{ahora()} - Inicia la carrera del taxi.")

    def mover(self):
        if self.en_marcha and not self.en_movimiento:
            self.actualizar_tarifa()
            self.en_movimiento = True
            self.ultima_hora = time.time()
            self.logger.info("El taxi se ha puesto en marcha.")
            self.add_message(f"{ahora()} - El taxi se ha puesto en marcha")

    def parar(self):
        if self.en_marcha and self.en_movimiento:
            self.actualizar_tarifa()
            self.en_movimiento = False
            self.ultima_hora = time.time()
            self.logger.info("El taxi se ha parado.")

    def finalizar_carrera(self):
        if self.en_marcha:
            self.actualizar_tarifa()
            self.logger.info(f"Carrera finalizada. Importe total: {self.tarifa_total:.2f} €")
            self.reset()
        else:
            self.logger.warning("Intento de finalizar una carrera que no está en curso")

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
            self.logger.info("Tarifa actualizada.")

    def cambiar_precios(self, nueva_tarifa_por_minuto_movimiento, nueva_tarifa_por_minuto_parado, nueva_tarifa_base):
        self.tarifa_por_minuto_movimiento = nueva_tarifa_por_minuto_movimiento
        self.tarifa_por_minuto_parado = nueva_tarifa_por_minuto_parado
        self.tarifa_base = nueva_tarifa_base
        self.logger.info("Actualización de tarifas realizada.")
        self.reset()

    def add_message(self, message):
        self.messages.append(message)


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler('taximetro.log')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

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


"""
def limpiar_mensajes():
    st.session_state.messages = []

def main():
    st.markdown(
         
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
            html_warning = 
            st.markdown(html_warning, unsafe_allow_html=True)


    else:
        if menu_selection == "Cambiar Precios":
            with st.form("form_cambiar_precios"):
                try:
                    nueva_tarifa_movimiento = st.number_input("Nueva Tarifa por Minuto en Movimiento (€)", min_value=0.0, value=float(st.session_state.taximetro.tarifa_por_minuto_movimiento))
                    nueva_tarifa_parado = st.number_input("Nueva Tarifa por Minuto Parado (€)", min_value=0.0, value=float(st.session_state.taximetro.tarifa_por_minuto_parado))
                    nueva_tarifa_base = st.number_input("Nueva Tarifa Base (€)", min_value=0.0, value=float(st.session_state.taximetro.tarifa_base))
                    submit_button = st.form_submit_button(label="Actualizar Tarifas")
                    if submit_button:
                        st.session_state.taximetro.cambiar_precios(nueva_tarifa_movimiento, nueva_tarifa_parado, nueva_tarifa_base)
                        st.success("Tarifas actualizadas correctamente.")
                except ValueError:
                    st.error("Error: Debes ingresar un número válido para las tarifas.")

        elif menu_selection == "Ayuda":
            html_ayuda = 
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
            
            """


