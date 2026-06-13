import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
class MenuView:
    """
    Se encarga de la interfaz de usuario en la consola.
    Utiliza la librería 'rich' para mostrar menús, tablas,
    mensajes de error y una barra de progreso estética durante las descargas.
    """
    def __init__(self):
        self.console = Console()
    def mostrar_banner(self) -> None:
        """Muestra el banner decorativo de inicio de la aplicación."""
        self.console.clear()
        banner_text = (
            "[bold red]🎥 Descargador de YouTube POO + MVC 🎥[/bold red]\n"
            "[dim]Desarrollado en solitario con fines académicos[/dim]"
        )
        self.console.print(Panel(banner_text, expand=False, border_style="red"))
    def mostrar_menu_principal(self) -> str:
        """
        Muestra las opciones del menú principal y solicita una selección.
        
        :return: Opción elegida por el usuario.
        """
        self.mostrar_banner()
        self.console.print("\n[bold cyan]Seleccione una opción del menú:[/bold cyan]")
        self.console.print(" [bold green]1.[/bold green] Buscar y analizar un video de YouTube")
        self.console.print(" [bold green]2.[/bold green] Descargar video analizado (Elegir resolución)")
        self.console.print(" [bold green]3.[/bold green] Descargar únicamente el audio en MP3")
        self.console.print(" [bold green]4.[/bold green] Salir de la aplicación")
        opcion = Prompt.ask(
            "\n[bold yellow]Opción[/bold yellow]", 
            choices=["1", "2", "3", "4"], 
            default="1"
        )
        return opcion
    def solicitar_url(self) -> str:
        """
        Solicita al usuario ingresar un enlace de YouTube.
        
        :return: URL limpia ingresada.
        """
        self.console.print("\n[bold cyan]🔗 Ingrese la URL del video de YouTube:[/bold cyan]")
        url = Prompt.ask("[bold yellow]URL[/bold yellow]").strip()
        return url
    def mostrar_detalles_video(self, detalles: dict) -> None:
        """
        Muestra la información y metadatos de un video analizado en una tabla formateada.
        
        :param detalles: Diccionario con la información del video obtenido del modelo.
        """
        # Convertir segundos de duración a formato MM:SS u HH:MM:SS
        segundos = detalles["duracion"]
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segundos_restantes = segundos % 60
        if horas > 0:
            duracion_formateada = f"{horas:02d}:{minutos:02d}:{segundos_restantes:02d}"
        else:
            duracion_formateada = f"{minutos:02d}:{segundos_restantes:02d}"
        table = Table(title="🔍 Datos del Video Analizado", title_style="bold magenta")
        table.add_column("Atributo", style="cyan", justify="right")
        table.add_column("Valor", style="white")
        table.add_row("Título", detalles["titulo"])
        table.add_row("Canal / Autor", detalles["autor"])
        table.add_row("Duración", duracion_formateada)
        table.add_row("Resoluciones Detectadas", ", ".join(detalles["resoluciones"]))
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n[bold green]✓ Video analizado con éxito y cargado en memoria.[/bold green]")
        self.esperar_tecla()
    def solicitar_resolucion(self, resoluciones: list[str]) -> str:
        """
        Muestra las calidades disponibles para un video y le pide elegir una.
        
        :param resoluciones: Lista de strings de resoluciones.
        :return: Resolución seleccionada.
        """
        self.console.print("\n[bold cyan]📺 Seleccione la resolución que desea descargar:[/bold cyan]")
        for i, res in enumerate(resoluciones, start=1):
            self.console.print(f" [bold green]{i}.[/bold green] {res}")
        opciones_validas = [str(i) for i in range(1, len(resoluciones) + 1)]
        opcion = Prompt.ask(
            "[bold yellow]Selección de resolución[/bold yellow]", 
            choices=opciones_validas, 
            default="1"
        )
        return resoluciones[int(opcion) - 1]
    def mostrar_mensaje_exito(self, mensaje: str) -> None:
        """Muestra un mensaje de éxito con formato agradable."""
        self.console.print(f"\n[bold green]🎉 ¡Éxito!: {mensaje}[/bold green]\n")
        self.esperar_tecla()
    def mostrar_error(self, error: str) -> None:
        """Muestra un mensaje de error con un recuadro de aviso."""
        self.console.print(f"\n[bold red]❌ ERROR: {error}[/bold red]\n")
        self.esperar_tecla()
    def mostrar_mensaje_estado(self, mensaje: str) -> None:
        """Muestra un mensaje de estado informativo rápido."""
        self.console.print(f"[dim yellow]{mensaje}[/dim yellow]")
    def esperar_tecla(self) -> None:
        """Genera una pausa para que el usuario pueda ver la pantalla."""
        Prompt.ask("\n[bold dim white]Presione Enter para continuar...[/bold dim white]", default="", show_choices=False, show_default=False)
    def crear_barra_progreso(self) -> Progress:
        """
        Construye una instancia personalizada de la barra de progreso de Rich.
        
        :return: Instancia de Progress configurada.
        """
        return Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn()
        )