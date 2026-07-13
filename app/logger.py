import logging
from datetime import datetime
from pathlib import Path


def setup_logger(output_dir: Path):
    logs_dir = Path(output_dir) / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / f"execution_{datetime.now():%Y-%m-%d_%H%M%S}.log"

    logger = logging.getLogger("zabbix-report")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Log file: %s", log_file)
    return logger
