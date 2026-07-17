from fastapi import FastAPI
from contextlib import asynccontextmanager

from dotenv import load_dotenv

import os
import shutil

from api.upload import router as upload_router
from api.search import router as search_router

load_dotenv()


def reset_storage():

    if os.path.exists("./uploads"):
        shutil.rmtree("./uploads")

    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")

    os.makedirs("./uploads", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    reset_storage()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(upload_router)
app.include_router(search_router)