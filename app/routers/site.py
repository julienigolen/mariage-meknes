from fastapi import APIRouter, Request

from app.gate import gate_redirect
from app.templates_engine import templates

router = APIRouter()


@router.get("/")
def home(request: Request):
    if (r := gate_redirect(request)) is not None:
        return r
    return templates.TemplateResponse(request, "home.html", {})
