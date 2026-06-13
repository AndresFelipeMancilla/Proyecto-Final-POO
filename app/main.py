import sys
import os
# Añadir la raíz del proyecto al sys.path para asegurar que las importaciones relativas funcionen
# sin importar desde dónde se ejecute el archivo.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.controllers.downloader_controller import DownloaderController
def main():
    """
    Función de arranque de la aplicación.
    Instancia el controlador principal e inicia el ciclo de vida del software.
    """
    controlador = DownloaderController()
    controlador.iniciar_aplicacion()
if __name__ == "__main__":
    main()