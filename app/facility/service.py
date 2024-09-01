from fastapi import Depends
from app.facility.models import Facility
from app.facility.schemas import FacilityCreate, FacilityDelete
from app.facility.repository import FacilityRepository
from app.accounts.models import Accounts
from app.facility.exceptions import FacilityNotFound


class FacilityService:
    def __init__(self, repository: FacilityRepository = Depends(FacilityRepository)):
        self.repository = repository

    async def create_facility(
        self, facility: FacilityCreate, account: Accounts
    ) -> Facility:
        facility = await self.repository.create(
            Facility(**facility.model_dump(), account_id=account.id)
        )
        return facility

    async def get_all_account_facilities(self, account: Accounts) -> list[Facility]:
        facilities = await self.repository.get_all_account_facilities(
            account_id=account.id
        )
        return facilities

    async def delete_account_facility(
        self, facility: FacilityDelete, account: Accounts
    ):
        facility = await self.repository.get_account_facility_by_id(
            account_id=account.id, facility_id=facility.facility_id
        )
        if facility is None:
            raise FacilityNotFound()
        await self.repository.delete(model_instance=facility)
