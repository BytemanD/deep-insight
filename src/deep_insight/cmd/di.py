import asyncio
from pathlib import Path

import click
import uvicorn

from deep_insight.collector import fs, static
from deep_insight.doc import store
from deep_insight.doc.store import SERVICE
from deep_insight.research.ai import ResearchAI

AI = ResearchAI()


@click.group()
def app():
    pass


@app.group()
def chromadb():
    """ChromaDB"""


@chromadb.command("docs")
def list_docs():
    """List docs"""
    docs = SERVICE.list_docs()
    print(docs)


@chromadb.command("import")
@click.argument("file_path")
def import_markdown(file_path: str):
    """Import markdown file"""
    SERVICE.import_file(file_path)
    click.echo("imported success", color="green")


@chromadb.command("query")
def query(text: str):
    """Query docs"""
    results = SERVICE.query(text, n_results=1)
    print(results)


@app.group()
def ai():
    """AI"""


@ai.command()
@click.argument("text")
def query(text: str):
    """AI"""
    asyncio.run(AI.query(text))


@app.group()
def doc():
    """Docs manager"""


@doc.command()
@click.argument("source")
def ingest(source: str):
    """ingest from file/url"""

    if source.startswith("http"):
        doc_path = static.COLLECTOR.collect(source)
    elif Path(source).exists():
        doc_path = fs.COLLECTOR.collect(source)
    else:
        raise click.ClickException("source not exists")

    click.echo("import to chromadb ...")
    store.SERVICE.import_file(doc_path)

    click.secho("ingest success", fg="green")


@app.command()
def master():
    """Start master server"""

    uvicorn.run("deep_insight.master.wsgi:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    app()
