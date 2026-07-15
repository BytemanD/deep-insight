import os
import shutil
from pathlib import Path

from loguru import logger
from markitdown import MarkItDown

from deep_insight.db.models import Doc


class LocaclFileCollector:
    def collect(self, file_path: str):
        src = Path(file_path)
        dst = Path("data", "raw", src.name)
        if dst.exists():
            logger.warning("delete doc {}", dst)
            os.remove(dst)
        logger.warning("copy doc {} -> {}", src, dst)
        shutil.copyfile(src, dst)
        return self._convert_to_md(dst)

    def _convert_to_md(self, src: Path):
        md = MarkItDown()
        logger.info("convert {}", src)
        results = md.convert(src)
        print(results)
        print("xxxxx", src)
        return Doc()


COLLECTOR = LocaclFileCollector()
