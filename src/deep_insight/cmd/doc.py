from pathlib import Path

import click

from deep_insight.apps.master.manager import MANAGER
from deep_insight.apps.vector.manager import get_vector_driver

driver = get_vector_driver()

from . import app


@app.command()
@click.argument("source")
def ingest(source: str):
    """ingest doc from file/url"""

    src = Path(source)
    click.echo(f"import file: {src}")
    doc = MANAGER.upload_doc(src.name, src.read_bytes())

    click.secho(f"created doc: {doc.uuid}({doc.file_path})", fg="green")
    click.echo("parse doc ...")
    doc = MANAGER.parse_doc(doc.uuid)
    click.secho("ingest success", fg="green")


if __name__ == "__main__":
    app()
