import os

import click
import dotenv
from pystonic import conf, log

from deep_insight.common import context

dotenv.load_dotenv()
context.project_id.set(os.getenv("PROJECT_ID"))

CONF = conf.BaseAppConfig()


@click.group()
@click.option("-v", "--verbose", count=True)
def app(verbose: int):
    log.setup_logger(CONF.log, versbose=verbose + 1, remove=True)
