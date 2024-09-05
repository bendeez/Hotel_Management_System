from fastapi import Depends
from app.business.domain.repository import BusinessRepository
from app.business.domain.service import BusinessService
from app.tools.application.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession


def get_business_repository(db: AsyncSession = Depends(get_db)) -> BusinessRepository:
    return BusinessRepository(db=db)


def get_business_service(
    business_user_repository: BusinessRepository = Depends(get_business_repository),
) -> BusinessService:
    return BusinessService(repository=business_user_repository)
