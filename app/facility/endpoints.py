from fastapi import APIRouter, Depends, status
from app.facility.schemas import FacilityCreate, FacilityOut
from typing import List
from app.facility.service import FacilityService
from app.auth.service import get_account
from app.accounts.models import Accounts


facility_router = APIRouter()


@facility_router.post(
    "/facility", response_model=FacilityOut, status_code=status.HTTP_201_CREATED
)
async def create_facility(
    facility: FacilityCreate,
    facility_service: FacilityService = Depends(FacilityService),
    account: Accounts = Depends(get_account),
):
    facility = await facility_service.create_facility(
        facility=facility, account=account
    )
    return facility


@facility_router.get("/facilities", response_model=List[FacilityOut])
async def get_account_facilities(
    facility_service: FacilityService = Depends(FacilityService),
    account: Accounts = Depends(get_account),
):
    facilities = await facility_service.get_all_account_facilities(account=account)
    return facilities


@facility_router.delete(
    "/facility/{facility_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def create_chat_log(
    facility_id: int,
    facility_service: FacilityService = Depends(FacilityService),
    account: Accounts = Depends(get_account),
):
    await facility_service.delete_account_facility(
        facility_id=facility_id, account=account
    )
