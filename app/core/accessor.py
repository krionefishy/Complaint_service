from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Feedback
from sqlalchemy import select, update
from app.services.analyze_service import AnalyzeService
import logging


class FeedbackAcessor:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.logger = logging.getLogger("Database")
        self.service = AnalyzeService()

    async def create_feedback(
            self,
            text: str,
            status: str = "open",
            sentiment: str = "neutral",
            category: str = "other"
    ):
        try:
            self.logger.debug(f"received text = {text}, status = {status}, sent = {sentiment}, category = {category}")
            feedback = Feedback(
                text=text,
                status=status,
                sentiment=sentiment,
                category=category
            )

            self.session.add(feedback)
            await self.session.commit()
            await self.session.refresh(feedback)
            
            sentiment = await self.service.analyze_sentiment(text)
            await self.update_feedback(feedback.id, sentiment=sentiment)

            category = await self.service.classify_category(text)
            updated_feedback = await self.update_feedback(feedback.id, category=category)


            return updated_feedback
        except SQLAlchemyError as err:
            await self.session.rollback()
            self.logger.error(f"Database error {str(err)}")
            raise err
        except Exception as err:
            await self.session.rollback()
            self.logger.error(f"Unexpected error: {str(err)}", exc_info=True)
            raise err
        

    async def get_task_by_id(self, id: int):
        self.logger.debug(f"Received feedback id {id}")
        result = await self.session.execute(
                select(Feedback)
                .where(Feedback.id == id)
                )
        feedback = result.scalars().first()
        return feedback
    

    async def update_feedback(self, feedback_id: int, *, sentiment: str = None, category: str = None):
        if sentiment is None and category is None:
            self.logger.warning("No fields to update")
            return None

        values = {}
        if sentiment:
            values["sentiment"] = sentiment
        if category:
            values["category"] = category

        stmt = update(Feedback).where(Feedback.id == feedback_id).values(**values).returning(Feedback)

        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        
        
        except SQLAlchemyError as err:
            await self.session.rollback()
            self.logger.error(f"Database error during update: {str(err)}")
            raise err