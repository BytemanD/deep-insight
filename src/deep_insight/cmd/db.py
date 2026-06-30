from deep_insight.db import models

from . import app


@app.group()
def init():
    """Init db"""
    models.create_all_tables()


if __name__ == "__main__":
    app()
