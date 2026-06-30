import asyncio
from typing import Optional

import click
from pystonic.pretty import output

from deep_insight.apps.master.manager import MANAGER
from deep_insight.research.ai import ResearchAI

from . import app

AI = ResearchAI()


@app.command()
@click.argument("text")
def query(text: str):
    """AI"""
    asyncio.run(AI.query(text))


@app.group()
def project():
    """Project manager"""


@project.command("list")
def list_project():
    output.print_models(MANAGER.list_project())


@project.command("create")
@click.argument("name")
@click.option("-d", "--description", help="Project description")
def create_project(name: str, description: Optional[str]):
    output.print_model(MANAGER.create_project(name=name, description=description))


@project.command("delete")
@click.argument("uuid")
def delete_project(uuid: str):
    MANAGER.delete_project(uuid)


@app.group()
def session():
    """Session manager"""


@session.command("list")
def list_dialog():
    """Project manager"""
    output.print_models(MANAGER.list_session())


@session.command("create")
@click.argument("name")
@click.argument("project")
def create_dialog(name: str, project: Optional[str]):
    output.print_model(MANAGER.create_session(name, project))


@session.command("delete")
@click.argument("uuid")
def delete_session(uuid: str):
    MANAGER.delete_session(uuid)


if __name__ == "__main__":
    app()
