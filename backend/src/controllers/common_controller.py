from fastapi import Depends

from fastapi_controllers import (
    Controller, 
    get
)

from backend.src.pydanticClasses.applicantData import Applicant_get_request_pydantic

from backend.src.services.applicant_service import ApplicantService
from backend.src.services.exam_service import ExamService
from backend.src.services.common_service import CommonService


class ApplicantController (Controller):
    __applicantService: ApplicantService
    __examService: ExamService
    __commonService: CommonService


    def __init__ (self,
        applicantService: ApplicantService = Depends(ApplicantService), 
        examService: ExamService = Depends(ExamService), 
        commonService: CommonService = Depends(CommonService)
    ) -> None:
        self.__applicantService = applicantService
        self.__examService = examService
        self.__commonService = commonService
    

    @get('/getAllData')
    async def getAllData (self, applicantData: Applicant_get_request_pydantic):
        return await self.__commonService.getAllData(self.__applicantService, self.__examService, applicantData)