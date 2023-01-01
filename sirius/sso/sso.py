from fastapi import Request, HTTPException, status
from fastapi.responses import Response
from pathlib import Path
from typing import Any
from onelogin.saml2.auth import OneLogin_Saml2_Auth


saml_path = str(Path(__file__).parent / "saml")


class SAMLException(HTTPException):
    def __init__(self, detail: dict[str, Any], headers: dict[str, Any] | None = None):
        super().__init__(status.HTTP_503_SERVICE_UNAVAILABLE, detail, headers)


class XMLResponse(Response):
    media_type = "application/xml"


def init_saml_auth(request: dict) -> OneLogin_Saml2_Auth:
    auth = OneLogin_Saml2_Auth(request, custom_base_path=saml_path)
    return auth


async def prepare_request(request: Request) -> dict[str, Any]:
    return {
        "http_host": request.url.hostname,
        "https": request.headers.get(
            "x-forwarded-ssl", "on" if request.url.scheme == "https" else "off"
        ),
        "script_name": request.url.path,
        "post_data": await request.form(),
        "get_data": request.query_params,
    }
