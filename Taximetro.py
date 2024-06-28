'''
Importación de libreria streamlit para interface grafica, hashlib para encriptar password, 
logging para funcionalidad de log, datetime y time para fechas y horas legibles.
'''
import time
from datetime import datetime
import streamlit as st
import logging
import hashlib

# Biblioteca para bbdd
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Función para bbdd.
class Carrera(Base):
    __tablename__ = 'carreras'
    id = Column(Integer, primary_key=True)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    tiempo_movimiento = Column(Float)
    tiempo_parado = Column(Float)
    tarifa_final = Column(Float)

    def __repr__(self):
        return f"<Carrera(id={self.id}, fecha_inicio={self.fecha_inicio}, tarifa_final={self.tarifa_final})>"

# Crear la conexión con la bbdd.
engine = create_engine('sqlite:///taximetro.db', echo=True)
Base.metadata.create_all(engine)

# Crear una sesión con la bbdd.
Session = sessionmaker(bind=engine)
session = Session()

class Taximetro:
    # Clase que simula el funcionamiento de un taxímetro.
    def __init__(self):
        # Metodo que inicializa la clase y establece valores por defecto.
        self.tarifa_por_minuto_movimiento = 3.0
        self.tarifa_por_minuto_parado = 1.2
        self.tarifa_base = 2.5
        self.reset()
        logger.info ("Taxímetro inicializando con tarifas base.") # Genera un nuevo registro en el log.
   
    def reset(self):
        # Metodo para restablecer el valor inicial de todas las variables despues de una carrera.
        self.en_marcha = False # Esta variable indica que se ha iniciado una carrera.
        self.en_movimiento = False # Esta variable indica que el taxi esta en movimiento.
        self.tarifa_total = 0
        self.hora_inicio = None # Almacena el momento en que se inicia la carrera a traves de función time() de la biblioteca time.
        self.ultima_hora = None # Almacena el momento en que se produce la transición a ultimo estado.
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
        
    def mover(self):
        # Metodo que calcula la tarifa del ultimo estado (parado) e indica que a partir de ahora estamos en movimiento.
        if self.en_marcha and not self.en_movimiento:
            self.actualizar_tarifa()
            self.en_movimiento = True
            self.ultima_hora = time.time()
            st.session_state.messages.append(f"{ahora()} - El taxi se ha puesto en marcha.") # Mensaje en interface grafica Streamlit.
            logger.info ("El taxi se ha puesto en marcha.") 
            
    def parar(self):
        # Metodo que calcula la tarifa del ultimo estado (movimiento) e indica que a partir de ahora estamos parados.
        if self.en_marcha and self.en_movimiento:
            self.actualizar_tarifa()
            self.en_movimiento = False
            self.ultima_hora = time.time()
            st.session_state.messages.append(f"{ahora()} - El taxi se ha parado.")
            logger.info ("El taxi se ha parado.")
           
    def finalizar_carrera(self):
        ''' Metodo que calcula la tarifa final de la carrera en curso en base a la suma total del tiempo parado y en movimiento,
        multiplicada por el precio correspondiente y añadiendo la tarifa base.'''
        if self.en_marcha:
            self.actualizar_tarifa()
            st.session_state.tarifa_final = self.tarifa_total + self.tarifa_base
            # st.session_state.tarifa_final es una variable de Streamlit que muestra el precio final de la carrera. 
            self.guardar_carrera()
            # Guarda la carrera dentro de la bbdd SQL.
            st.session_state.messages.append(f"{ahora()} - Carrera finalizada. Tiempo de marcha y paro : {self.tiempo_movimiento + self.tiempo_parado :.2f} segundos, Importe total: {st.session_state.tarifa_final:.2f} €")
            # st.session_state.messages.append agrega a la lista de mensajes generados en Streamlit los datos de la carrera finalizada.
            logger.info(f"Carrera finalizada. Importe total:{self.tarifa_total:.2f} €") 
            self.reset()
        else:
            st.session_state.messages.append(f"{ahora()} - No hay carrera en curso para finalizar.") 
            logger.warning("Intento de finalizar una carrera que no está en curso") 

    def actualizar_tarifa(self):
        ''' Este metodo acumula los importes parciales ante cambios de estado (parado o movimiento).
        A esta funcion se la llama antes de producirse un nuevo estado y registra el importe del estado anterior'''
        hora_actual = time.time()
        if self.en_marcha:
            tiempo_transcurrido = hora_actual - self.ultima_hora
            if self.en_movimiento:
                self.tiempo_movimiento += tiempo_transcurrido
                self.tarifa_total += tiempo_transcurrido * (self.tarifa_por_minuto_movimiento / 60)
                # Se convierte self.tarifa_por_minuto_movimiento a segundos porque los tiempos transcurridos estan en segundos.
            else:
                self.tiempo_parado += tiempo_transcurrido
                self.tarifa_total += tiempo_transcurrido * (self.tarifa_por_minuto_parado / 60)
            self.ultima_hora = hora_actual
            logger.info ("Tarifa actualizada.")

    def cambiar_precios(self, nueva_tarifa_por_minuto_movimiento, nueva_tarifa_por_minuto_parado, nueva_tarifa_base):
            # Metodo que actualiza los valores de las variables de las tarifas (nueva_tarifa_por_minuto_movimiento, nueva_tarifa_por_minuto_parado, nueva_tarifa_base)
            self.tarifa_por_minuto_movimiento = nueva_tarifa_por_minuto_movimiento
            self.tarifa_por_minuto_parado = nueva_tarifa_por_minuto_parado
            self.tarifa_base = nueva_tarifa_base
            logger.info ("Actualización de tarifas realizada.")
            self.reset()  # Reinicia a valores por defecto con el objetivo de dejar los parametros limpios, listos para el inicio de una nueva carrera.
            st.session_state.messages.append(f"{ahora()} - Precios actualizados: Movimiento €{self.tarifa_por_minuto_movimiento}/min, Parado €{self.tarifa_por_minuto_parado}/min, Base €{self.tarifa_base}.")
    
    def guardar_carrera(self):
        # Guarda en la base de datos toda la informacion relativa a cada una de las carreras realizadas.
        nueva_carrera = Carrera(
            fecha_inicio=datetime.fromtimestamp(self.hora_inicio), # Construye formato de fecha/hora para los valores de time().
            fecha_fin=datetime.now(), # Recoge la fecha/hora actual
            tiempo_movimiento=self.tiempo_movimiento,
            tiempo_parado=self.tiempo_parado,
            tarifa_final=self.tarifa_total + self.tarifa_base
        )
        session.add(nueva_carrera)
        session.commit()
        logger.info(f"Carrera guardada en la base de datos: {nueva_carrera}")

def obtener_carreras():
    # Extrae informacion de todas las carreras de la base de datos.
    return session.query(Carrera).all()


def get_logger():
    # Funcion para el log.
    # Crear un logger
    logger = logging.getLogger() 
    logger.setLevel(logging.INFO)

    # Crear una vista del log para la terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # Crea un archivo .log
    file_handler = logging.FileHandler('taximetro.log')
    file_handler.setLevel(logging.INFO)

    # Formato del log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Añade los gestores de log si no existen.
    if not logger.handlers:
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
    return logger

logger = get_logger()

def leer_log():
    # Funcion para leer fichero log.
    try:
        with open('taximetro.log', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "No se encontró el archivo de log."

def ahora():
    # Función que devuelve hora actual en un formato hora/minuto/segundo.
    ahora = datetime.now()
    hora_actual = ahora.strftime("%H:%M:%S")
    return hora_actual

def hash_string(input_string):
    # Función que devuelve el hash de una cadena de texto.
    return hashlib.md5(input_string.encode()).hexdigest()

usuarios = {
    # Las contraseñas aparecen encriptadas mediante metodo de hash.
    "user1": "7c6a180b36896a0a8c02787eeafb0e4c",
    "user2": "6cb75f652a9b52798eb6cf2201057c73",
    "user3": "819b0643d6b89dc9b579fdfc9094f28e",
    "user4": "34cc93ece0ba9e3f6f235d4af979b16c",
    "user5": "db0edd04aaac4506f7edab03ac855d56",
}

def main():
    # Estilos personalizados con CSS, para el color de fondo y el nombre de la aplicación.
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #FEE338;  /* Fondo amarillo mate */ 
            }
            .css-1d391kg {  /* Sidebar */
                 background-color: #FEE338;  /* Fondo amarillo mate */
            }
            .stTextInput, .stButton, .stNumberInput {
                margin-bottom: 10px;  /* Espacio entre los elementos del formulario */
            }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #FEE338;  /* Fondo amarillo mate */ 
            }
            .css-1d391kg {  /* Sidebar */
                 background-color: #FEE338;  /* Fondo amarillo mate */
            }
            .stTextInput, .stButton, .stNumberInput {
                margin-bottom: 10px;  /* Espacio entre los elementos del formulario */
            }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <h1 style='text-align: center;'>Taxi Driver</h1>
        """, 
        unsafe_allow_html=True
    )

    try:
    # Proporcionamos robustez a la aplicacion mediante try y except.
        menu_options = ["Taxímetro", "Login", "Cambiar Precios", "Ver Log", "Ver Historial", "Ayuda"]
        menu_selection = st.sidebar.selectbox("Menú", menu_options)
        logger.info(f"Menu seleccionado: {menu_selection}")

        if 'taximetro' not in st.session_state:
            # Inicializamos variables de Streamlit.
            st.session_state.taximetro = Taximetro()
            st.session_state.messages = []
            st.session_state.tarifa_final = 0.0
            st.session_state.logged_in = False
        if not st.session_state.logged_in:
            # Comprobamos si el usuario ha realizado login, se presenta formulario de login.
            if menu_selection == "Login":
                with st.form("form_login"):
                    usuario = st.text_input("Usuario")
                    password = st.text_input("Password", type="password")
                    submit_button = st.form_submit_button(label="Login")
                    if submit_button:
                        if usuario in usuarios and usuarios[usuario] == hash_string(password):                      
                            st.session_state.logged_in = True
                            st.success("Login realizado con éxito")
                        else:
                            st.session_state.logged_in = False
                            st.error("Usuario o password incorrectos")
            else:
                # Se añade texto de bienvenida.
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
            # Comprobamos si el usuario ha accedido a alguno de los menus disponibles.
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
                        <li>Esta aplicación calcula el coste total de una carrera, con un precio distinto si el taxi se mueve o está parado</li>
                        <li>Tarifas iniciales: 3€/min en marcha, 1.2 €/min parado y 2.5€ por bajada de bandera (tarifa base)</li>
                        <li>La simulación se realiza mediante los botones situados en la parte superior de la pantalla Taxímetro</li>
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
            # Menu para ver el log del taximetro en Streamlit.
                st.markdown("### Visualización del Log")
                st.text_area("", value=leer_log(), height=200)   
            elif menu_selection == "Ver Historial":
            # Menu para ver historial de carreras (bbdd) en Streamlit. 
                st.markdown("### Historial de Carreras")
                carreras = obtener_carreras()
                if carreras:
                    historial_text = ""
                    for carrera in carreras:
                    # Muestra todas las carreras realizadas en Stremlit en siguiente formato:
                        historial_text += f"Carrera {carrera.id}:\n"
                        historial_text += f"  Inicio: {carrera.fecha_inicio}\n"
                        historial_text += f"  Fin: {carrera.fecha_fin}\n"
                        historial_text += f"  Tiempo en movimiento: {carrera.tiempo_movimiento:.2f} segundos\n"
                        historial_text += f"  Tiempo parado: {carrera.tiempo_parado:.2f} segundos\n"
                        historial_text += f"  Tarifa final: {carrera.tarifa_final:.2f}€\n\n"
                    st.text_area("", value=historial_text, height=400)
                else:
                    st.write("No hay carreras registradas en la base de datos.")
            else:
                # Disponemos los botones del taximetro en horizontal.
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    if st.button("Iniciar Carrera"):
                        st.session_state.taximetro.iniciar()
                        st.session_state.tarifa_final = 0.0  # Reset de tarifa total al iniciar carrera.
                        logger.info("Botón 'Iniciar Carrera' presionado.")

                with col2:
                    if st.button("Taxi en movimiento"):
                        st.session_state.taximetro.mover() 
                        logger.info("Botón 'Taxi en movimiento' presionado.")

                with col3:
                    if st.button("Taxi parado"):
                        st.session_state.taximetro.parar()
                        logger.info("Botón 'Taxi parado' presionado.")

                with col4:
                    if st.button("Finalizar Carrera"):
                        st.session_state.taximetro.finalizar_carrera()
                        logger.info("Botón 'Finalizar carrera' presionado.")

                st.text_area("Mensajes", value="\n".join(st.session_state.messages), height=200)
                st.markdown(f"**Tarifa Total: €{st.session_state.tarifa_final:.2f}**")

    # Detectamos los tipos de error mas comunes como valor, tipo y el resto se clasifica como generico o (inesperado).
    except ValueError as ve:
        st.error(f"Error de valor: {ve}")
        logger.error(f"Error de valor: {ve}")
    except TypeError as te:
        st.error(f"Error de tipo: {te}")
        logger.error(f"Error de tipo: {te}")
    except Exception as e:
        st.error(f"Se ha producido un error inesperado: {e}")
        logger.error(f"Error inesperado: {e}")

# __name__ es una variable especial en Python que toma el valor "__main__" cuando el script se ejecuta directamente. 
if __name__ == "__main__":
    main()
