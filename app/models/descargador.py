import os
import yt_dlp
from app.models.video import Video
class Descargador:
    """
    Se encarga de gestionar la descarga física de videos y audios desde YouTube
    utilizando la librería yt-dlp y organizando los archivos en subcarpetas.
    """
    def __init__(self, ruta_destino_base: str = "Descargas"):
        """
        Inicializa el descargador con una ruta base en el almacenamiento.
        
        :param ruta_destino_base: Nombre de la carpeta principal para guardar descargas.
        """
        self.ruta_destino_base = ruta_destino_base
        self._crear_directorios()
    def _crear_directorios(self) -> None:
        """Crea de forma segura las subcarpetas necesarias para video y audio."""
        self.ruta_videos = os.path.join(self.ruta_destino_base, "Videos")
        self.ruta_audios = os.path.join(self.ruta_destino_base, "Audio")
        os.makedirs(self.ruta_videos, exist_ok=True)
        os.makedirs(self.ruta_audios, exist_ok=True)
    def descargar_video(self, video: Video, resolucion: str, hook_progreso=None) -> bool:
        """
        Descarga un video en la resolución seleccionada.

        :param video: Instancia de la clase Video a descargar.
        :param resolucion: Resolución deseada (ej: '720p').
        :param hook_progreso: Función de callback opcional para reportar el progreso de la descarga.
        :return: True si la descarga fue exitosa, de lo contrario lanza una excepción.
        """
        # Extraer el número de la resolución (ej: '720p' -> '720')
        res_num = resolucion.replace('p', '')
        # Opciones para yt-dlp: intentamos emparejar la resolución elegida con el mejor audio disponible
        ydl_opts = {
            'format': f'bestvideo[height<={res_num}]+bestaudio/best[height<={res_num}]/best',
            'outtmpl': os.path.join(self.ruta_videos, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        if hook_progreso:
            ydl_opts['progress_hooks'] = [hook_progreso]
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video.url])
            return True
        except Exception as e:
            raise RuntimeError(f"Error al descargar el video: {str(e)}")
    def descargar_audio(self, video: Video, hook_progreso=None) -> bool:
        """
        Descarga únicamente el audio de un video y lo convierte a formato MP3 de alta calidad.

        :param video: Instancia de la clase Video de la cual extraer el audio.
        :param hook_progreso: Función de callback opcional para reportar el progreso.
        :return: True si la descarga fue exitosa, de lo contrario lanza una excepción.
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.ruta_audios, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            # Configuración de post-procesamiento para extraer y convertir el audio a mp3
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        if hook_progreso:
            ydl_opts['progress_hooks'] = [hook_progreso]
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video.url])
            return True
        except Exception as e:
            raise RuntimeError(f"Error al descargar y procesar el audio: {str(e)}")