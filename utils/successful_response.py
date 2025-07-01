import typing
from starlette.background import BackgroundTask
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

def SuccessfulResponse(
        content: typing.Any, status_code: int = 200, headers: typing.Mapping[str, str] | None = None,
        media_type: str | None = None, background: BackgroundTask | None = None):
    return JSONResponse(content, status_code, headers, media_type, background)