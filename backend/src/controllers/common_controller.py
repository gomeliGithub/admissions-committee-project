from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_controllers import (
    Controller, 
    get
)

from backend.src.database_connection import get_async_database_session

from backend.src.pydanticClasses.applicantData import Applicant_get_request_pydantic

from backend.src.services.applicant_service import ApplicantService
from backend.src.services.exam_service import ExamService
from backend.src.services.common_service import CommonService


class ApplicantController (Controller):
    __databaseSession: AsyncSession
    __applicantService: ApplicantService
    __examService: ExamService
    __commonService: CommonService


    def __init__ (self, databaseSession: AsyncSession = Depends(get_async_database_session), 
        applicantService: ApplicantService = Depends(ApplicantService), 
        examService: ExamService = Depends(ExamService), 
        commonService: CommonService = Depends(CommonService)
    ) -> None:
        self.__databaseSession = databaseSession
        self.__applicantService = applicantService
        self.__examService = examService
        self.__commonService = commonService
    

    @get('/getAllData')
    async def getAllData (self, applicantData: Applicant_get_request_pydantic):
        return await self.__commonService.getAllData(self.__databaseSession, self.__applicantService, self.__examService, applicantData)