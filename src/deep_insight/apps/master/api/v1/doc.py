from fastapi import APIRouter, BackgroundTasks, UploadFile, File

from deep_insight.apps.master.manager import MANAGER

router = APIRouter(prefix="/docs")


@router.get("")
async def list_docs():
    docs = MANAGER.list_docs()
    return {"docs": docs}


@router.post("/upload")
async def upload_doc(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
):
    content = await file.read()
    doc = MANAGER.upload_doc(file.filename, content)
    background_tasks.add_task(MANAGER.parse_doc, doc.uuid)
    return {"message": "ok"}
