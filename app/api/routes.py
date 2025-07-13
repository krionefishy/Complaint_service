import logging
from fastapi import APIRouter, Depends, HTTPException
from app.models.models import FeedbackCreate, FeedbackResponse
from app.core.accessor import FeedbackAcessor
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db

router = APIRouter(prefix="/feedback", tags=["Feedback"])

logger = logging.getLogger("Routes")


@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackCreate, db_session: AsyncSession = Depends(get_db)):
    logger.info("received new feedback")
    logger.debug(f"received text = {request.text}")

    accessor = FeedbackAcessor(db_session)
    try: 
        feedback = await accessor.create_feedback(text = request.text)
        return FeedbackResponse.model_validate(feedback, from_attributes=True)
    except Exception as err:
        logger.error("Failed to create feedback: %s", str(err), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    

@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(feedback_id: int, db_session: AsyncSession = Depends(get_db)):
    logger.info(f"received feedback_id {feedback_id}")
    accessor = FeedbackAcessor(db_session)
    feedback = await accessor.get_task_by_id(feedback_id)

    if not feedback:
        logger.warning("Feedback with ID %s not found", feedback_id)
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    return FeedbackResponse.model_validate(feedback, from_attributes=True)