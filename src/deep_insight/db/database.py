from typing import Optional

from sqlalchemy import Select
from sqlmodel import Sequence, Session, SQLModel, create_engine

engine = create_engine("sqlite:///data/di.db")


def exec(statement) -> Optional[Sequence]:
    with Session(engine) as session:
        results = session.exec(statement)
        if not isinstance(statement, Select):
            session.commit()
            return
        return [x for x in results]


def query_first(statement: Select) -> SQLModel | None:
    with Session(engine) as session:
        return session.exec(statement).first()


def add(model: SQLModel):
    with Session(engine) as session:
        session.add(model)
        session.commit()
        session.refresh(model)


def update(model: SQLModel):
    with Session(engine) as session:
        session.add(model)
        session.commit()
        session.refresh(model)
