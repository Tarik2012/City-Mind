# ======================================================
# CityMind - 10 Monitoring & Logging (v3, compatible con Windows)
# ======================================================

import logging
import time
from pathlib import Path
from datetime import datetime
import csv

# ======================================================
# 1. Configuración de carpetas
# ======================================================
BASE_LOG_DIR = Path("logs")
BASE_LOG_DIR.mkdir(exist_ok=True)

# Crear nueva carpeta con timestamp
timestamp = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")
LOG_DIR = BASE_LOG_DIR / timestamp
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Rutas de archivos
log_file = LOG_DIR / "citymind_monitor.log"
summary_file = LOG_DIR / "pipeline_summary.csv"

# ======================================================
# 2. Configuración del logger
# ======================================================
logger = logging.getLogger("citymind_monitor")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

logger.info(f"=== Nueva sesión CityMind iniciada ===")
logger.info(f"Carpeta de logs: {LOG_DIR.resolve()}")

# ======================================================
# 3. Clase PipelineStep (context manager + resumen CSV)
# ======================================================
class PipelineStep:
    """Gestiona y registra la ejecución de cada paso del pipeline."""

    def __init__(self, step_name):
        self.step_name = step_name
        self.start_time = time.time()
        logger.info(f"Starting step: {self.step_name}")

    def end(self, status="SUCCESS", message=""):
        end_time = time.time()
        duration = round(end_time - self.start_time, 2)
        timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        header = ["timestamp", "step_name", "status", "duration_sec", "message"]
        write_header = not summary_file.exists()

        with open(summary_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(header)
            writer.writerow([timestamp_now, self.step_name, status, duration, message])

        if status == "SUCCESS":
            logger.info(f"Completed step: {self.step_name} in {duration}s. {message}")
        elif status == "FAILED":
            logger.error(f"Step failed: {self.step_name}. {message}")
        else:
            logger.warning(f"Step ended with status={status}: {self.step_name}. {message}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        status = "FAILED" if exc_type else "SUCCESS"
        message = str(exc_value) if exc_value else ""
        self.end(status=status, message=message)
        return False  # relanza la excepción si la hay

# ======================================================
# 4. Ejemplo manual
# ======================================================
if __name__ == "__main__":
    with PipelineStep("example_task"):
        time.sleep(1)
        logger.info("Simulated task running...")

    step = PipelineStep("manual_example")
    time.sleep(1.5)
    step.end(status="SUCCESS", message="Manual task completed successfully.")
