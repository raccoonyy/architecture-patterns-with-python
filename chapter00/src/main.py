from fastapi import FastAPI
from src.app import create_app

app: FastAPI = create_app()
