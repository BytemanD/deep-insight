from typing import Optional

import click
from pystonic.pretty import output

from deep_insight.db import models
from deep_insight.db.models import Project, Session


@click.group()
def app():
    models.create_all_tables()
    pass


@app.group()
def project():
    """Project manager"""


@project.command("list")
def list_project():
    items = Project.query()

    output.print_models(items)


@project.command("create")
@click.argument("name")
@click.option("-d", "--description", help="Project description")
def create_project(name: str, description: Optional[str]):
    item = Project(name=name, description=description)
    item.create()
    output.print_model(item)


@project.command("delete")
@click.argument("uuid")
def delete_dialog(uuid: str):
    db_model = Project.get_by_uuid(uuid)
    if not db_model:
        raise click.ClickException(f"Project {uuid} not found")

    db_model.delete()


@app.group()
def dialog():
    """Session manager"""


@dialog.command("list")
def list_dialog():
    """Project manager"""
    items = Session.query()
    output.print_models(items)


@dialog.command("create")
@click.argument("name")
@click.argument("project")
def create_dialog(name: str, project: Optional[str]):
    db_project = Project.get_by_uuid(project)
    if not db_project:
        raise click.ClickException(f"Project {project} not found")
    item = models.Session(project_uuid=project, name=name)
    item.create()
    output.print_model(item)


@dialog.command("delete")
@click.argument("uuid")
def delete_dialog(uuid: str):
    db_dialog = Session.get_by_uuid(uuid)
    if not db_dialog:
        raise click.ClickException(f"Session {uuid} not found")

    db_dialog.delete()


if __name__ == "__main__":
    app()
