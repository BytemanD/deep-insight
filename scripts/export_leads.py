"""
将线索数据导入数据库
"""

from deepinsight.db.models.base import create_all_tables


def main():

    create_all_tables()


if __name__ == "__main__":
    main()
