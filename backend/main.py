from fastapi import FastAPI
from core.base_router import router as api_router
# importing all the models at the starting to register at the start
from core.models_registry import *
app = FastAPI()


app.include_router(api_router, prefix="/apis")
