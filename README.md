Descargador de Videos de YouTube (MVC + POO)

Descripción
Este proyecto es una aplicación de consola interactiva y moderna escrita en Python que permite a los usuarios descargar videos completos o extraer únicamente el audio de YouTube de forma organizada.

Diseñada bajo estrictos principios de la Programación Orientada a Objetos (POO) y estructurada bajo el patrón de arquitectura Modelo-Vista-Controlador (MVC), esta herramienta garantiza un desacoplamiento completo entre la lógica de negocio, la interacción con el usuario y el control del flujo.

Objetivo
El propósito de este desarrollo es demostrar la aplicación consciente y profesional de la ingeniería de software en utilidades del día a día, asegurando un código limpio, legible, extensible y verificado a través de pruebas unitarias automatizadas.

Características principales
- Mapeo detallado de metadatos: Obtiene de forma segura el título, autor, duración y resoluciones disponibles antes de proceder con cualquier descarga.
- Descargas personalizadas:
    - Video completo en múltiples resoluciones (baja, media, alta).
    - Audio independiente en alta fidelidad (formato MP3/M4A).
- Validación robusta: Verificación integrada en los modelos para validar enlaces de YouTube y asegurar que las rutas de destino en el disco sean correctas.
- Consola elegante (UI Premium): Interfaz interactiva construida con la librería Rich, que incluye menús coloridos, paneles informativos y barras de progreso en tiempo real durante la descarga.
- Clasificación automática: Organización autónoma de las descargas en carpetas locales (Descargas/Videos/ y Descargas/Audio/).

Tecnologías Utilizadas
- Python 3.10+ (Lenguaje de programación principal)
- yt-dlp (Librería externa para interactuar de forma estable con los servidores de YouTube)
- rich (Librería externa para dar estilos, tablas y animaciones en la terminal)
- pytest (Framework para la automatización y ejecución de pruebas unitarias)
- Git & GitHub (Control de versiones y publicación de código)

Arquitectura del Proyecto (MVC)
La aplicación divide estrictamente sus responsabilidades en tres capas fundamentales:

1. Modelo (app/models/)
- video.py: Modela la entidad de un video de YouTube, se encarga de extraer la información de los metadatos y realizar validaciones de la URL.
- descargador.py: Controla la descarga física del archivo, gestionando las configuraciones técnicas de yt-dlp. Ninguno de estos archivos realiza impresiones (print) ni pide capturas de pantalla o inputs por consola.

2. Vista (app/views/)
- menu_view.py: Diseña toda la experiencia visual del usuario utilizando Rich. Imprime menús interactivos, tablas con metadatos y captura las entradas de teclado del usuario de forma amigable.

3. Controlador (app/controllers/)
- downloader_controller.py: Funciona como el cerebro de la aplicación. Captura los eventos e instrucciones de la vista, invoca los métodos lógicos del modelo y retorna los resultados (o maneja excepciones) para presentárselos ordenadamente al usuario.

Diagrama de Clases
A continuación se detalla la estructura lógica y relaciones de asociación entre nuestras clases del sistema:

classDiagram
    class Video {
        -str url
        -str titulo
        -int duracion
        -str autor
        +obtener_detalles() dict
        +validar_url(url) bool
    }
    class Descargador {
        -str ruta_destino
        +descargar_video(video, resolucion) bool
        +descargar_audio(video) bool
    }
    class DownloaderController {
        -Video modelo_video
        -Descargador modelo_descargador
        -MenuView vista
        +iniciar_aplicacion() void
        +procesar_descarga(opcion) void
    }
    class MenuView {
        +mostrar_menu_principal() str
        +mostrar_detalles_video(detalles) void
        +mostrar_mensaje_exito(mensaje) void
        +mostrar_error(error) void
    }
    DownloaderController --> Video : Usa
    DownloaderController --> Descargador : Usa
    DownloaderController --> MenuView : Controla

Instalación y uso

Requisitos previos
Asegúrate de tener instalado Python 3.10 o superior y el gestor de paquetes pip.

Paso 1: Clonar el repositorio
git clone https://github.com/AndrésFelipeMancilla/Proyecto-Final-POO.git
cd Proyecto-Final-POO

Paso 2: Instalar las dependencias externas
pip install -r requirements.txt

Paso 3: Configuración automática de FFmpeg
Este proyecto requiere FFmpeg para procesar audio. Para descargarlo automáticamente en la raíz del proyecto, ejecuta una sola vez:
python -m ffmpeg_downloader download

Paso 4: Ejecutar la aplicación
Para iniciar el descargador interactivo, corre:
python app/main.py

Pruebas unitarias
Hemos implementado una robusta suite de pruebas utilizando pytest para asegurar el correcto funcionamiento de las validaciones y procesos lógicos de la aplicación.
Para ejecutar las pruebas y verificar la integridad del código, usa:
pytest

Capturas de pantalla
(Las capturas del funcionamiento serán cargadas en la carpeta docs/capturas/ una vez se termine la fase de desarrollo)
1. Menú Principal: docs/capturas/captura_menu.png
2. Descarga en Progreso: docs/capturas/captura_descarga.png
3. Archivos Guardados: docs/capturas/captura_archivos.png
4. Pruebas unitarias (Pytest): docs/capturas/captura_pruebas.png
5. Repositorio en GitHub: docs/capturas/captura_github.png

Autor
Andrés Felipe Mancilla Santiago - Desarrollo de Software en Solitario

Licencia
Este proyecto se encuentra bajo la Licencia MIT. Para más información, ver el archivo LICENSE.