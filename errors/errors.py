from typing import Union, Optional, Any, Dict
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

class CustomErrParams(HTTPException):
    def __init__(self, status_code: int, detail: Any = None, headers: Dict[str, str] | None = None, message: str = "An error has occured!"):
        super(HTTPException).__init__(
            status_code = status_code,
            detail = detail,
            headers = headers
        )
        self.message = message
        self.ok = False
