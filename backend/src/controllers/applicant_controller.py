from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_controllers import (
    Controller, 
    get, 
    post, 
    put
)

from backend.src.database_connection import get_async_database_session

from backend.src.pydanticClasses.applicantData import ( 
    Applicant_create_request_pydantic,
    Applicant_get_request_pydantic, 
    Applicant_get_response_pydantic,
    Applicant_update_request_pydantic 
)

from backend.src.services.applicant_service import ApplicantService


class ApplicantController (Controller):
    __databaseSession: AsyncSession
    __applicantService: ApplicantService


    def __init__ (self, databaseSession: AsyncSession = Depends(get_async_database_session), applicantService: ApplicantService = Depends(ApplicantService)) -> None:
        self.__databaseSession = databaseSession
        self.__applicantService = applicantService
    

    @get('/getApplicantData', response_class = Applicant_get_response_pydantic)
    async def getApplicantData (self, applicantData: Applicant_get_request_pydantic):
        return await self.__applicantService.getApplicantData(self.__databaseSession, applicantData)
    

    @post('/createApplicant', response_class = None)
    async def createApplicant (self, applicantData: Applicant_create_request_pydantic) -> None:
        return await self.__applicantService.createApplicant(self.__databaseSession, applicantData)
    

    @put('/updateApplicant', response_class = None)
    async def updateApplicant (self, applicantData: Applicant_update_request_pydantic) -> None:
        return await self.__applicantService.updateApplicant(self.__databaseSession, applicantData)