from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response
from pathlib import Path

from ..sso import sso


saml_path = str(Path(__file__).parent / "saml")


router = APIRouter(
    prefix="/sso/warwick",
    responses={
        503: {
            "description": "Service provider error",
            "content": {
                "application/json": {
                    "example": {
                        "last_error": "invalid SP",
                        "errors": ["error 1", "error 2"],
                    }
                }
            },
        }
    },
)


@router.get("/", response_class=sso.XMLResponse)
async def warwick_sso_metadata(request: Request) -> sso.XMLResponse:
    req = await sso.prepare_request(request)
    auth = sso.init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        return sso.XMLResponse(content=metadata)
    else:
        raise sso.SAMLException(
            {"last_error": auth.get_last_error_reason(), "errors": errors}
        )


@router.get("/login", response_class=RedirectResponse)
async def warwick_sso_login(request: Request):
    req = await sso.prepare_request(request)
    auth = sso.init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        callback_url = auth.login()
        return RedirectResponse(callback_url)
    else:
        raise sso.SAMLException(
            {"last_error": auth.get_last_error_reason(), "errors": errors}
        )


@router.post("/acs")
async def warwick_sso_callback(request: Request):
    req = await sso.prepare_request(request)
    auth = sso.init_saml_auth(req)
    auth.process_response()
    errors = auth.get_errors()
    if len(errors) == 0:
        if not auth.is_authenticated():
            return Response("User not authenticated", status_code=401)
        else:
            data = auth.get_attributes()
            return data
    else:
        raise sso.SAMLException(
            {"last_error": auth.get_last_error_reason(), "errors": errors}
        )
