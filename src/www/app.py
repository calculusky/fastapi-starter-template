from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.auth.router import auth
from modules.user.router import user
from core.exception.http.httpException import httpExceptionHandler




   


def initApp(app: FastAPI, whiteListedDomains: list[str]):
    
    app.add_middleware(
        CORSMiddleware, 
        allow_origins=whiteListedDomains, 
        allow_credentials=True,
        allow_methods=["GET", "PUT", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "X-Requested-With", "Content-Type"]
    )

    app.include_router(auth.router)
    app.include_router(user.router)

    httpExceptionHandler(app)
    
    
    return app