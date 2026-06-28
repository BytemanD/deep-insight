from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from deep_insight.db.models import Dialog

router = APIRouter(prefix="/dialogs")


class DialogCreate(BaseModel):
    project_uuid: str
    name: Optional[str] = None


class DialogUpdate(BaseModel):
    name: Optional[str] = None


class DialogResponse(BaseModel):
    uuid: str
    project_uuid: str
    name: Optional[str] = None
    created_at: str
    updated_at: str


def _to_response(d: Dialog) -> DialogResponse:
    return DialogResponse(
        uuid=d.uuid,
        project_uuid=d.project_uuid,
        name=d.name,
        created_at=d.created_at.isoformat(),
        updated_at=d.updated_at.isoformat(),
    )


@router.get("")
async def list_dialogs(project_uuid: Optional[str] = None):
    if project_uuid:
        dialogs = Dialog.query(Dialog.project_uuid == project_uuid)
    else:
        dialogs = Dialog.query()
    return {"dialogs": [_to_response(d) for d in dialogs]}


@router.get("/{uuid}")
async def get_dialog(uuid: str):
    dialog = Dialog.get_by_uuid(uuid)
    if not dialog:
        raise HTTPException(status_code=404, detail="Dialog not found")
    return _to_response(dialog)


@router.post("", status_code=201)
async def create_dialog(body: DialogCreate):
    dialog = Dialog(project_uuid=body.project_uuid, name=body.name)
    dialog.create()
    return _to_response(dialog)


@router.put("/{uuid}")
async def update_dialog(uuid: str, body: DialogUpdate):
    dialog = Dialog.get_by_uuid(uuid)
    if not dialog:
        raise HTTPException(status_code=404, detail="Dialog not found")

    if body.name is not None:
        dialog.name = body.name

    dialog.update()
    return _to_response(dialog)


@router.delete("/{uuid}", status_code=204)
async def delete_dialog(uuid: str):
    dialog = Dialog.get_by_uuid(uuid)
    if not dialog:
        raise HTTPException(status_code=404, detail="Dialog not found")
    dialog.delete()
