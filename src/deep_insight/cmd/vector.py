from pathlib import Path

import click
from loguru import logger
from pystonic.pretty import output

from deep_insight.apps.vector.manager import get_vector_driver
from deep_insight.collector import fs, static
from deep_insight.common import context
from deep_insight.common.utils import text_shorten

driver = get_vector_driver()

from . import app


@app.command()
def list_docs():
    """List docs"""
    logger.debug("project id: {}", context.project_id.get())
    docs = driver.list_docs()
    output.print_models(docs, fields=["id", "name"])


@app.command("import")
@click.argument("file_path")
def import_markdown(file_path: str):
    """Import markdown file"""
    driver.import_file(file_path)
    click.echo("imported success", color="green")


@app.command()
@click.argument("text")
def query(text: str):
    """Query docs by content"""
    results = driver.query(text, n_results=1)
    for doc in results:
        click.secho(f"ID:   {doc.id}", fg="cyan")
        click.secho(f"Name: {doc.name}", fg="cyan")
        click.secho("Content:", fg="cyan")
        click.echo(text_shorten(doc.content))
        click.echo()


@app.command()
@click.argument("source")
def ingest(source: str):
    """ingest doc from file/url"""

    if source.startswith("http"):
        doc_path = static.COLLECTOR.collect(source)
    elif Path(source).exists():
        doc_path = fs.COLLECTOR.collect(source)
    else:
        raise click.ClickException("source not exists")

    click.echo("import to chromadb ...")
    driver.import_file(doc_path)

    click.secho("ingest success", fg="green")


if __name__ == "__main__":
    app()
