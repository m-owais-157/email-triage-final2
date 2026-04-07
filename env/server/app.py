from fastapi import FastAPI
from env.main import app as main_app

app = FastAPI()
app.mount("/", main_app)
