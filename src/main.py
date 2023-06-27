import logging
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.logger import AppInsightsMiddleware, initialize_logger
from routers.sets.router import router as sets_router

app = FastAPI(
    title="MTGCollection - API",
)

app.add_middleware(AppInsightsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(sets_router)


@app.on_event("startup")
def startup_event():
    sys.path.append("./core")
    load_dotenv()
    initialize_logger(os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"))
    logging.info("API_STARTUP")
