import hashlib
import json


def file_sha256(file_path: str) -> str:
    """计算文件的二进制哈希值"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # 分块读取，避免大文件内存溢出
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def text_sha256(text: str) -> str:
    """计算文件的二进制哈希值"""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(text.encode(encoding="utf-8"))
    return sha256_hash.hexdigest()


def text_shorten(text: str, width=100):
    if isinstance(text, list):
        text = json.dumps(text)

    if len(text) <= width:
        return text
    return text[:width] + "..."
