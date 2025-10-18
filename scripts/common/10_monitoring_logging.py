# ======================================================
# CityMind - 10 Monitoring & Logging
# Centralized logging and execution monitoring
# ======================================================

import logging
import time
from pathlib import Path
from datetime import datetime

# ======================================================
# 1️⃣ Logger configuration
# ======================================================
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / "pipeline.log"

logger = logging.getLogger("citymind_monitor")
logger.setLevel(logging.INFO)

# Avoid duplicate handlers
if not logger.hasHandlers():
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

# ======================================================
# 2️⃣ Context manager for step timing
# ======================================================
class PipelineStep:
    """Context manager to measure and log execution time of each step."""

    def __init__(self, step_name: str):
        self.step_name = step_name

    def __enter__(self):
        self.start_time = time.time()
        logger.info(f"▶️ Starting step: {self.step_name}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed = time.time() - self.start_time
        if exc_type:
            logger.error(f"❌ Error in step '{self.step_name}': {exc_value}")
        else:
            logger.info(f"✅ Completed step: {self.step_name} in {elapsed:.2f} seconds\n")

# ======================================================
# 3️⃣ Example usage (only runs if executed directly)
# ======================================================
if __name__ == "__main__":
    with PipelineStep("example_task"):
        time.sleep(2)
        logger.info("Simulated task running...")
