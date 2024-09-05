from fastapi.security import OAuth2PasswordBearer
from app.auth.domain.service import AuthService
from app.auth.domain.repository import AuthRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.tools.application.dependencies import get_db
from app.auth.domain.constants import TokenType
from fastapi import Depends


def get_auth_repository(db: AsyncSession = Depends(get_db)) -> AuthRepository:
    return AuthRepository(db=db)


def get_auth_service(
    auth_repository: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthService(repository=auth_repository)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_account(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    account = await auth_service.get_account(
        token=token, _token_type=TokenType.ACCESS_TOKEN
    )
    return account
