import pytest
import os
from app.models.video import Video
from app.models.descargador import Descargador
def test_validar_url_correcta():
    """Prueba que el método validar_url acepte formatos válidos de YouTube."""
    urls_validas = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ"
    ]
    for url in urls_validas:
        assert Video.validar_url(url) is True
def test_inicializacion_video_valido():
    """Prueba que un objeto Video se instancie correctamente con su URL."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    video = Video(url)
    assert video.url == url
def test_creacion_directorios_descargador(tmp_path):
    """Prueba que el Descargador cree correctamente las carpetas de almacenamiento."""
    ruta_temporal = os.path.join(tmp_path, "DescargasTest")
    descargador = Descargador(ruta_destino_base=ruta_temporal)
    assert os.path.exists(descargador.ruta_videos) is True
def test_inicializacion_url_invalida():
    """Prueba que la clase Video lance ValueError al recibir una URL ajena a YouTube."""
    url_invalida = "https://www.google.com"
    with pytest.raises(ValueError):
        Video(url_invalida)