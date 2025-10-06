"""Módulo de logging centralizado.

Provee un logger con RotatingFileHandler localizado en la carpeta `log/`.
Exporta `get_logger()` y `nombre_fichero` para compatibilidad con el código existente.
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime

LOG_DIR = Path(__file__).parent / 'log'
LOG_DIR.mkdir(exist_ok=True)
fecha = datetime.now().strftime("%d%m%Y").lower()
nombre_fichero = str(LOG_DIR / f"{fecha}_HEROESYVILLANOS.log")


def get_logger(name='heroesyvillanos', level=logging.INFO, max_bytes=1024*1024, backup_count=3):
	logger = logging.getLogger(name)
	if logger.handlers:
		return logger
	logger.setLevel(level)
	fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	handler = RotatingFileHandler(nombre_fichero, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8')
	handler.setFormatter(fmt)
	logger.addHandler(handler)
	# also add a console handler for convenience
	ch = logging.StreamHandler()
	ch.setFormatter(fmt)
	logger.addHandler(ch)
	return logger


def log(msg, level='info'):
	logger = get_logger()
	getattr(logger, level)(msg)