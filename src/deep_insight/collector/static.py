from pathlib import Path

from loguru import logger
from markitdown import MarkItDown


class StaticHTMLCollector:
    def __init__(self):
        self.md = MarkItDown()

    def collect(self, url: str):
        logger.info("convert from URL: {}", url)
        result = self.md.convert(url)
        output_path = Path(
            "data", "raw", url.replace("/", "_").replace(":", "_") + ".md"
        )
        with open(output_path, "w", encoding="utf-8") as f:
            logger.debug("save to {} ...", output_path)
            f.write(result.text_content)
        return output_path


COLLECTOR = StaticHTMLCollector()
