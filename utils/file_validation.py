import magic
from pydantic import BaseModel
from typing import Optional, Literal, Union
from fastapi import UploadFile

class InvalidFile(BaseModel):
    ok: Literal[False] = False
    status_code: int
    message: str
class ValidFile(BaseModel):
    ok: Literal[True]
    fileType: str | None = None

async def validateFile(
        file: UploadFile | None, validFormats: Optional[set[str]] = None , 
        validSize: float = 50*1024*1024) -> Union[ValidFile, InvalidFile]:
    if file is None:
        return InvalidFile(ok=False, status_code=404, message="Please provide valid file!")
    print(file)
    fileRead = await file.read()
    fileType = magic.from_buffer(fileRead, mime=True)
    if validFormats is not None:
        print(fileType)
        if fileType not in validFormats:
            return InvalidFile(ok=False, status_code=415, message="Invalid media type!")
    if len(fileRead) > validSize:
        return InvalidFile(ok=False, status_code=413, message="File is too large!")
    
    await file.seek(0)
    
    return ValidFile(ok=True, fileType=fileType)
    
    