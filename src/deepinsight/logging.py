"""Logging Configuration using Loguru"""

import sys
from pathlib import Path

from loguru import logger

from augur_common.config import CONF


def setup_logging() -> None:
    """Setup loguru logging configuration"""

    # Remove default handler
    logger.remove()
    # Determine log level (DEBUG if debug mode, otherwise use config)
    log_level = "DEBUG" if CONF.debug else CONF.log.level
    # Console handler
    logger.add(
        sys.stdout,
        level=log_level,
        format=CONF.log.format,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # File handler
    log_path = Path(CONF.log.file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.add(
        CONF.log.file,
        level=log_level,
        format=CONF.log.format,
        rotation=CONF.log.rotation,
        retention=CONF.log.retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
