from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import traceback
from config import config



    
def httpExceptionHandler(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    def httpExceptionHandler(request: Request, exc: StarletteHTTPException):
        jsonObj = {
                "success": False, 
                "message": exc.detail, 
            }
        if config.isDevEnvironment:
            jsonObj.update({ "stack": traceback.format_exception(exc) })
        return JSONResponse(
            status_code=exc.status_code or 500,
            
            content=jsonable_encoder(jsonObj),
        )
        
    @app.exception_handler(RequestValidationError)
    async def validationExceptionHandler(request: Request, exc: RequestValidationError):
          jsonObj = {
                "success": False, 
                "message": "Failed Validation", 
                "errors": exc.errors(),
            }
          if config.isDevEnvironment:
            jsonObj.update({ "stack": traceback.format_exception(exc) })
            
          return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonObj)
