"""从 data 目录导入 JSON 线索数据到数据库"""

import json
import os
from pathlib import Path

from loguru import logger

from augur_api.services.lead_service import lead_service
from augur_common import logging, objects
from augur_common.db import init_db


def main(data_dir: str = "data"):
    """从指定目录导入所有 JSON 线索文件"""
    logging.setup_logging()
    init_db.create_all_tables()
    data_path = Path(data_dir)

    if not data_path.exists():
        logger.error(f"错误: 目录 {data_dir} 不存在")
        return

    # 查找所有子目录下的 JSON 文件
    json_files = list(data_path.rglob("*.json"))

    if not json_files:
        logger.warning(f"在 {data_dir} 目录下未找到 JSON 文件")
        return

    logger.info(f"找到 {len(json_files)} 个 JSON 文件")

    for json_file in json_files:
        try:
            logger.info("import data from {}", json_file.name)
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)

            # 创建 Lead 对象
            obj = objects.Lead.model_validate(data, extra="ignore")

            if not obj.raw_file and obj.source:
                logger.warning("原始文件为空，重新下载 ...")

                pdf_path = json_file.parent.joinpath(json_file.name.replace(".json", ".pdf"))
                os.system(f"agent-browser open {obj.source}")
                os.system(f"agent-browser pdf {pdf_path}")
                if not pdf_path.exists():
                    raise Exception("PDF 下载失败")
                obj.raw_file = str(pdf_path)

            lead_service.create(obj)
            logger.success(f"导入成功: {data.get('name', json_file.name)}")
            os.remove(json_file)

        except Exception as e:
            logger.error(f"导入失败 {json_file}: {str(e)}")

    logger.success("导入完成!")


if __name__ == "__main__":
    main()
