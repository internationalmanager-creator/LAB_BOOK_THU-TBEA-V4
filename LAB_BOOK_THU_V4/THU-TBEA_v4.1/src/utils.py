# src/utils.py - utilidades compartidas del pipeline THU-TBEA v4.1
import time


def save_fig(fig, path, **kwargs):
    """Guarda una figura con reintentos ante errores transitorios de E/S
    (discos de red, antivirus, sincronizacion OneDrive/Dropbox, etc.)."""
    last_err = None
    for _ in range(4):
        try:
            fig.savefig(path, **kwargs)
            return
        except OSError as err:
            last_err = err
            time.sleep(0.5)
    raise last_err
