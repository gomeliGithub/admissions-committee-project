from typing import Annotated

from fastapi import (
    Cookie, 
    Depends
)

from fastapi_controllers import (
    Controller, 
    get
)

from ..auth.auth_bearer import JWTBearer

from ..pydanticClasses.applicantData import Applicant_get_request_pydantic

from ..services.applicant_service import ApplicantService
from ..services.exam_service import ExamService
from ..services.common_service import CommonService


class CommonController (Controller):
    __applicantService: ApplicantService
    __examService: ExamService
    __commonService: CommonService


    def __init__ (self,
        applicantService: ApplicantService = Depends(ApplicantService), 
        examService: ExamService = Depends(ExamService),
        commonService: CommonService = Depends(CommonService),
    ) -> None:
        self.__applicantService = applicantService
        self.__examService = examService
        self.__commonService = commonService
    

    @get('/checkAccess', dependencies = [Depends(JWTBearer(auto_error = False))])
    async def checkAccessMain (self) -> bool: # jwt: Annotated[str, Depends(JWTBearer(auto_error = False))] # secure_fgp: str = Cookie()
        # return await self.__commonService.checkAccessMain(jwt, secure_fgp, self.__mainService)
        
        return True


    @get('/getAllData', dependencies = [Depends(JWTBearer())])
    async def getAllData (self, applicantData: Applicant_get_request_pydantic):
        return await self.__commonService.getAllData(self.__applicantService, self.__examService, applicantData)