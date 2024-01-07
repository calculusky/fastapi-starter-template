from fastapi import FastAPI
from modules.auth.router import auth
from modules.user.router import user
from core.exception.http.httpException import httpExceptionHandler



   


def initApp(app: FastAPI):

    app.include_router(auth.router)
    app.include_router(user.router)

    httpExceptionHandler(app)
    
    
    return app