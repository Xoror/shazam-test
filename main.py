import os
import uvicorn
import magic
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException

from typing import Union, Any

from .utils.file_validation import validateFile
from .utils.successful_response import SuccessfulResponse
from .errors.errors import CustomErrParams
from .schemas.product import Product

app = FastAPI()

upload_path = "uploads"
os.makedirs(upload_path, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=upload_path))
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    status_code = exc.status_code
    detail = exc.detail
    headers = exc.headers
    return JSONResponse(
        status_code = status_code,
        content = jsonable_encoder({"message": detail["msg"], "ok": False}),
        headers = headers
    )

@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.get("/uploads/{file_name}")
async def getFile(file_name:str):
    file_name1 = file_name.replace("%20", " ")
    file_path = os.path.join(upload_path, file_name1)
    print("get upload ", file_name1)
    try:
        with open(file_path, "r") as file:
            data = file.read()
            return FileResponse(path=file_path, status_code=201)
    except:
        raise HTTPException(status_code=404, detail={"msg":"File doesn't exist!"})

@app.post("/submit")
async def submit(image: UploadFile | list[UploadFile], product: Product = Depends(Product)):
    listFiles = []
    if type(image) is list:
        listFiles = image
    elif type(image) is UploadFile:
        listFiles = [image]
    else:
        raise HTTPException(status_code=404, detail={"msg":"Something went wrong with your upload!"})
    #raise HTTPException(status_code=404, detail={"msg":"testing the message"})
    
    isValidFile = None
    for file in listFiles:
        if file.filename is None or file is None:
            raise HTTPException(status_code=404, detail={"msg":"You have to provide a file!"})
            return
        
        isValidFile = await validateFile(file=file, validFormats={"audio/mpeg", "audio/ogg"})
        if isValidFile.ok is False:
            raise HTTPException(status_code=isValidFile.status_code, detail={"msg":isValidFile.message})
            return

        file_path = os.path.join(upload_path, file.filename)
        with open(file_path, "wb") as f:
            fileB = await file.read()
            f.write(fileB)
    return SuccessfulResponse(
        status_code=201,
        content={
            "name": product.name,
            "image": [file.filename for file in listFiles],
            "fileType": isValidFile.fileType if isValidFile is not None else None,
            "ok": True
        }
    )
    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1")
'''
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(base_id: int, item: Item):
    return {"item_name": item.price, "base_id": base_id}
'''