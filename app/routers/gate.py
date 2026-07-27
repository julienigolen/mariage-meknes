from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from app.config import settings
from app.gate import code_matches, has_gate, make_gate_cookie
from app.i18n.context import lang_context
from app.templates_engine import templates

router = APIRouter()


@router.get("/entree")
def gate_page(request: Request):
    if has_gate(request):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request, "gate.html", {"error": False, **lang_context(request)})


@router.post("/entree")
def gate_submit(request: Request, code: str = Form("")):
    if not code_matches(code):
        return templates.TemplateResponse(
            request, "gate.html", {"error": True, **lang_context(request)}, status_code=401
        )
    resp = RedirectResponse("/", status_code=303)
    resp.set_cookie(
        settings.gate_cookie_name,
        make_gate_cookie(),
        max_age=settings.gate_max_age,
        httponly=True,
        samesite="lax",
        secure=settings.env == "prod",
    )
    return resp
