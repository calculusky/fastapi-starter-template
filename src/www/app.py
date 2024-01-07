from fastapi import FastAPI
from modules.auth.router import auth
from core.exception.http.httpException import httpExceptionHandler



   


def initApp(app: FastAPI):

    app.include_router(auth.router)
    httpExceptionHandler(app)
    
    
    return app