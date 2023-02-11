from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response

from ..models.User import *
from ..sso import sso

saml_path = str(Path(__file__).parent / "saml")


router = APIRouter(
    prefix="/realms/uwcs/broker/warwick_sso",
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


@router.get("/descriptor", response_class=sso.XMLResponse)
async def warwick_sso_metadata(request: Request):
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


@router.post("/endpoint")
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
            # return await create_user_from_warwick_sso(data)
    else:
        raise sso.SAMLException(
            {"last_error": auth.get_last_error_reason(), "errors": errors}
        )
