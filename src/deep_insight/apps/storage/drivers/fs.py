import os
import uuid
from pathlib import Path

from loguru import logger

from deep_insight.common.conf import CONF
from deep_insight.db.models import Doc


class FSDriver:
    def __init__(self):
        self.path = Path(CONF.storage.fs.path)
        self.path.mkdir(parents=True, exist_ok=True)

    def save(self, doc: Doc, content: bytes):
        doc.file_path = str(Path(doc.project_uuid, f"{uuid.uuid4()}_{doc.name}"))

        abs_path = self.path / doc.file_path
        abs_path.parent.mkdir(parents=True, exist_ok=True)

        doc.status = "saving"
        doc.update()
        abs_path.write_bytes(content)
        doc.status = "saved"
        doc.update()

    def delete(self, doc: Doc):
        abs_path = self.path / doc.file_path

        if not abs_path.exists():
            logger.warning("file {} does not exist", abs_path)

        logger.info("Deleting doc {}")
        os.remove(abs_path)

    def get_content(self, doc: Doc):
        abs_path = self.path / doc.file_path
        return abs_path.read_bytes()
