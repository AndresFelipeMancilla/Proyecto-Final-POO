import os
from app.models.video import Video
from app.models.descargador import Descargador
from app.views.menu_view import MenuView
class DownloaderController:
    """
    Controlador que conecta el Modelo (Video, Descargador) con la Vista (MenuView).
    Maneja el flujo de la aplicación y captura los eventos del usuario de forma segura.
    """
    def __init__(self):
        self.vista = MenuView()
        self.modelo_descargador = Descargador()
        self.video_actual = None  # Guardará la instancia del video analizado en memoria
    def iniciar_aplicacion(self) -> None:
        """Ciclo principal de la aplicación."""
        while True:
            try:
                opcion = self.vista.mostrar_menu_principal()
                if opcion == "1":
                    self._procesar_analisis()
                elif opcion == "2":
                    self._procesar_descarga_video()
                elif opcion == "3":
                    self._procesar_descarga_audio()
                elif opcion == "4":
                    self.vista.mostrar_mensaje_estado("\n[bold red]Saliendo del programa. ¡Hasta luego![/bold red]")
                    break
            except KeyboardInterrupt:
                # Captura el Ctrl+C para que el programa no tire un error feo en consola
                self.vista.mostrar_mensaje_estado("\n[bold red]Programa interrumpido por el usuario.[/bold red]")
                break
            except Exception as e:
                self.vista.mostrar_error(f"Ocurrió un error inesperado: {str(e)}")
    def _procesar_analisis(self) -> None:
        """Maneja la lógica para solicitar una URL y cargar los metadatos del video."""
        url = self.vista.solicitar_url()
        # Validar previamente usando el método de clase del Modelo
        if not Video.validar_url(url):
            self.vista.mostrar_error("La URL no es un enlace válido de YouTube.")
            return
        self.vista.mostrar_mensaje_estado("🔍 Conectando con YouTube y analizando el video... (Esto puede tardar unos segundos)")
        try:
            # Crear instancia de la entidad de negocio (Modelo)
            self.video_actual = Video(url)
            # Extraer detalles
            detalles = self.video_actual.obtain_details() if hasattr(self.video_actual, "obtain_details") else self.video_actual.obtener_detalles()
            # Enviar metadatos a la vista para ser mostrados
            self.vista.mostrar_detalles_video(detalles)
        except Exception as e:
            self.video_actual = None
            self.vista.mostrar_error(f"No se pudo analizar el video. Detalle: {str(e)}")
    def _procesar_descarga_video(self) -> None:
        """Coordina la descarga del video en la resolución elegida por el usuario."""
        if not self.video_actual:
            self.vista.mostrar_error("Primero debe analizar un video (Opción 1) antes de descargarlo.")
            return
        try:
            # Solicitar al usuario elegir una de las resoluciones detectadas en el modelo
            resolucion = self.vista.solicitar_resolucion(self.video_actual.resoluciones)
            self.vista.mostrar_mensaje_estado(f"📥 Preparando la descarga en {resolucion}...")
            # Creamos el gestor de progreso de Rich para pasarlo al callback
            with self.vista.crear_barra_progreso() as progress:
                tarea_id = progress.add_task(description="Descargando Video", total=100)
                # Callback de progreso que yt-dlp llamará repetidamente
                def hook_progreso(d):
                    if d['status'] == 'downloading':
                        # Extraer porcentaje desde la info de yt-dlp
                        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                        descargado = d.get('downloaded_bytes', 0)
                        if total > 0:
                            porcentaje = (descargado / total) * 100
                            progress.update(tarea_id, completed=porcentaje)
                    elif d['status'] == 'finished':
                        progress.update(tarea_id, completed=100)
                # Ejecutar la descarga física delegando al modelo Descargador
                self.modelo_descargador.descargar_video(
                    video=self.video_actual,
                    resolucion=resolucion,
                    hook_progreso=hook_progreso
                )
            self.vista.mostrar_mensaje_exito(f"Video guardado correctamente en: {self.modelo_descargador.ruta_videos}")
        except Exception as e:
            self.vista.mostrar_error(f"Error en el proceso de descarga de video: {str(e)}")
    def _procesar_descarga_audio(self) -> None:
        """Coordina la extracción y descarga del audio en formato MP3."""
        if not self.video_actual:
            self.vista.mostrar_error("Primero debe analizar un video (Opción 1) antes de extraer su audio.")
            return
        try:
            self.vista.mostrar_mensaje_estado("📥 Descargando y convirtiendo audio a MP3...")
            with self.vista.crear_barra_progreso() as progress:
                tarea_id = progress.add_task(description="Descargando Audio", total=100)
                def hook_progreso(d):
                    if d['status'] == 'downloading':
                        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                        descargado = d.get('downloaded_bytes', 0)
                        if total > 0:
                            porcentaje = (descargado / total) * 100
                            progress.update(tarea_id, completed=porcentaje)
                    elif d['status'] == 'finished':
                        progress.update(tarea_id, completed=100)
                self.modelo_descargador.descargar_audio(
                    video=self.video_actual,
                    hook_progreso=hook_progreso
                )
            self.vista.mostrar_mensaje_exito(f"Audio extraído y guardado correctamente en: {self.modelo_descargador.ruta_audios}")
        except Exception as e:
            self.vista.mostrar_error(f"Error en el proceso de descarga de audio: {str(e)}")