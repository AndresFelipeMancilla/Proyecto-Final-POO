import re
import yt_dlp
class Video:
    """
    Representa un video de YouTube y se encarga de validar la URL
    y extraer los metadatos necesarios utilizando la librería yt-dlp.
    """
    # Expresión regular robusta para validar URLs de YouTube (cortas, largas, shorts y compartidas)
    YOUTUBE_REGEX = r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)[a-zA-Z0-9_-]{11}"
    def __init__(self, url: str):
        """
        Inicializa un objeto de tipo Video.
        :param url: URL del video de YouTube a procesar.
        """
        if not self.validar_url(url):
            raise ValueError("La URL proporcionada no es un enlace válido de YouTube.")
        self.url: str = url
        self.titulo: str = ""
        self.autor: str = ""
        self.duracion: int = 0  # Duración en segundos
        self.resoluciones: list[str] = []
        self._detalles_cargados: bool = False
    @classmethod
    def validar_url(cls, url: str) -> bool:
        """
        Valida si una URL pertenece a un formato soportado de YouTube.
        :param url: URL a evaluar.
        :return: True si es válida, False en caso contrario.
        """
        if not url:
            return False
        return bool(re.match(cls.YOUTUBE_REGEX, url.strip()))
    def obtener_detalles(self) -> dict:
        """
        Extrae los metadatos del video usando yt-dlp sin descargar el archivo.
        :return: Diccionario con los detalles del video (titulo, autor, duracion, resoluciones).
        :raises: ValueError si el video no está disponible, es privado o hay problemas de conexión.
        """
        # Si ya fueron extraídos previamente, los retornamos para evitar múltiples llamadas de red
        if self._detalles_cargados:
            return self._retornar_info_dict()
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'skip_download': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                if not info_dict:
                    raise ValueError("No se pudo obtener la información del video.")
                self.titulo = info_dict.get('title', 'Título desconocido')
                self.autor = info_dict.get('uploader', 'Autor desconocido')
                self.duracion = info_dict.get('duration', 0)
                # Filtrar resoluciones de video disponibles que tengan pista de video y audio combinados,
                # o resoluciones progresivas estándar (360p, 720p, 1080p, etc.)
                formats = info_dict.get('formats', [])
                resoluciones_set = set()
                for f in formats:
                    height = f.get('height')
                    # Buscamos formatos que tengan resolución vertical establecida
                    if height and height in [360, 480, 720, 1080]:
                        resoluciones_set.add(f"{height}p")
                # Ordenar resoluciones de menor a mayor calidad de forma visual
                self.resoluciones = sorted(list(resoluciones_set), key=lambda x: int(x.replace('p', '')))
                # Por si no se detectan formatos específicos, agregamos opciones por defecto
                if not self.resoluciones:
                    self.resoluciones = ["360p", "720p"]     
                self._detalles_cargados = True
                return self._retornar_info_dict()
        except Exception as e:
            # Enmascaramos excepciones complejas de red en un ValueError descriptivo para la UI y los Tests
            raise ValueError(f"Error al conectar con YouTube para extraer metadatos: {str(e)}")
    def _retornar_info_dict(self) -> dict:
        """Helper privado para estructurar la respuesta de metadatos."""
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "duracion": self.duracion,
            "resoluciones": self.resoluciones,
            "url": self.url
        }