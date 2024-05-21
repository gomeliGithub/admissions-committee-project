from fastapi import Depends

from fastapi_controllers import (
    Controller, 
    get
)

from ..auth.auth_bearer import JWTBearer

from ..pydanticClasses.applicantData import Applicant_get_request_pydantic

from ..services.applicant_service import ApplicantService
from ..services.common_service import CommonService


class CommonController (Controller):
    __applicantService: ApplicantService
    __commonService: CommonService


    def __init__ (self,
        applicantService: ApplicantService = Depends(ApplicantService), 
        commonService: CommonService = Depends(CommonService),
    ) -> None:
        self.__applicantService = applicantService
        self.__commonService = commonService
    

    @get('/checkAccess', dependencies = [Depends(JWTBearer())])
    async def checkAccessMain (self) -> bool:
        return True


    @get('/getAllData', dependencies = [Depends(JWTBearer())])
    async def getAllData (self, applicantData: Applicant_get_request_pydantic):
        return await self.__commonService.getAllData(self.__applicantService, applicantData)