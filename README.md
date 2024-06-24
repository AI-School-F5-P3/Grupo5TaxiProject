# Taxi Driver

## Descripción

Taxi Driver es una aplicación que simula el funcionamiento de un taxímetro. Calcula el coste total de una carrera, con tarifas diferentes si el taxi está en movimiento o parado. Además, permite guardar el historial de carreras en una base de datos SQLite y visualizar logs y el historial de carreras en una interfaz gráfica desarrollada con Streamlit.

## Características

- Iniciar, parar y finalizar carreras.
- Calcular tarifas basadas en el tiempo en movimiento y el tiempo parado.
- Guardar el historial de carreras en una base de datos SQLite.
- Visualizar el historial de carreras y logs de actividades.
- Actualizar tarifas dinámicamente.

## Tecnologías Utilizadas

- Python
- Streamlit
- SQLAlchemy
- SQLite
- Logging
- Docker

## Instalación

1. Crea un directorio en tu PC donde clonar el repositorio localmente:
   ```sh
    mk taxi-driver
   ```
2. Navegar al directorio del proyecto:
    ```sh
    cd taxi-driver
    ```
3. Clonar el repositorio:
    ```sh
    git clone https://github.com/AI-School-F5-P3/Grupo5TaxiProject.git
    ```
4. Crear un entorno virtual e instalar las dependencias:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows, usa `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Uso

1. Ejecutar la aplicación:
    ```sh
    streamlit run Taximetro.py
    ```
2. Navegar a la interfaz de Streamlit que se abrirá en el navegador.

## Funcionalidades

### Taxímetro

- **Iniciar Carrera**: Comienza la carrera en estado parado.
- **Taxi en movimiento**: Indica que el taxi se ha puesto en marcha.
- **Taxi parado**: Indica que el taxi se ha detenido.
- **Finalizar Carrera**: Finaliza la carrera y calcula el importe total.

### Cambiar Precios

Permite actualizar las tarifas por minuto en movimiento, por minuto parado y la tarifa base.

### Ver Log

Muestra el registro de todas las actividades realizadas.

### Ver Historial

Muestra el historial de todas las carreras registradas en la base de datos.

### Ayuda

Proporciona detalles sobre el funcionamiento de la aplicación.

## Estructura del Código

### `Taximetro.py`

Contiene la clase `Taximetro` que simula el funcionamiento del taxímetro, incluyendo métodos para iniciar, mover, parar y finalizar carreras, así como para actualizar tarifas y guardar carreras en la base de datos.

Define el modelo de la base de datos usando SQLAlchemy. Incluye la clase `Carrera` que representa una carrera en la base de datos.

Incluye funciones auxiliares como `get_logger` para configurar el logging, `leer_log` para leer el archivo de log, y `hash_string` para el hashing de contraseñas.

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para mejorar el proyecto.
