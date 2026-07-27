from datetime import date

from fastapi import APIRouter, Request

from app.gate import gate_redirect
from app.i18n.context import lang_context
from app.templates_engine import templates

router = APIRouter()

WEDDING_DATE = date(2026, 10, 23)


@router.get("/")
def home(request: Request):
    if (r := gate_redirect(request)) is not None:
        return r
    days_left = (WEDDING_DATE - date.today()).days
    return templates.TemplateResponse(
        request, "home.html", {"days_left": days_left, **lang_context(request)}
    )
