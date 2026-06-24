from pathlib import Path


class LocaclFileCollector:
    def collect(self, file_path: str):
        return Path(file_path)


COLLECTOR = LocaclFileCollector()
