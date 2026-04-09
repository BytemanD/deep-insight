from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/leads")
def get_leads(request: Request) -> dict:
    return {"leads": []}
