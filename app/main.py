from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from app.core.database import db 
from app.utils.config import setup_config

settings = setup_config()
logger = logging.getLogger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level = settings.LOGGING_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger.info("Starting application...")
    
    await db.connect(settings.DATABASE_URL)
    yield
    logger.info("shutting down")
    await db.disconnect()

app = FastAPI(title="Feedback Service", lifespan=lifespan)

from app.api.routes import router as feedback_routes
app.include_router(feedback_routes)

