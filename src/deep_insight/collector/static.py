import os
import shutil
from pathlib import Path

from loguru import logger
from markitdown import MarkItDown

from deep_insight.db.models import Doc


class StaticHTMLCollector:
    def __init__(self):
        self.md = MarkItDown()

    def collect(self, source: str):
        if source.startswith("http"):
            logger.info("convert from URL: {}", source)
            dst = source
            raw_name = source.replace("/", "_").replace(":", "_") + ".md"
            meta = {"source": source}
        else:
            src = Path(source)
            dst = Path("data", "raw", src.name)
            if dst.exists():
                logger.warning("delete doc {}", dst)
                os.remove(dst)
            logger.warning("copy doc {} -> {}", src, dst)
            shutil.copyfile(src, dst)
            raw_name = dst.with_suffix(".md").name
            meta = {"source": raw_name}

        result = self.md.convert(dst)
        raw_path = Path("data", "raw", raw_name)
        with open(raw_path, "w", encoding="utf-8") as f:
            logger.debug("save to {} ...", raw_path)
            f.write(result.text_content)
        return Doc(
            project_uuid="xxxxxx",
            file_path=meta.get("source"),
            file_size=raw_path.stat().st_size,
        )


COLLECTOR = StaticHTMLCollector()
