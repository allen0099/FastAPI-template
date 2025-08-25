from fastapi import FastAPI

from .factory import create_app

app: FastAPI = create_app()
