from fastapi import Depends

from fastapi_controllers import (
    Controller, 
    get, 
    post, 
    put
)

from ..auth.auth_bearer import JWTBearer

from ..pydanticClasses.applicantData import ( 
    Applicant_create_request_pydantic,
    Applicant_get_request_pydantic, 
    Applicant_get_response_pydantic,
    Applicant_update_request_pydantic 
)

from ..services.applicant_service import ApplicantService


class ApplicantController (Controller):
    __applicantService: ApplicantService


    def __init__ (self, applicantService: ApplicantService = Depends(ApplicantService)) -> None:
        self.__applicantService = applicantService


    @get('/getApplicantData', dependencies = [Depends(JWTBearer())], response_model = Applicant_get_response_pydantic)
    async def getApplicantData (self, applicantData: Applicant_get_request_pydantic = Depends()):
        return await self.__applicantService.getApplicantData(applicantData)
    

    @post('/createApplicant', dependencies = [Depends(JWTBearer())], response_class = None)
    async def createApplicant (self, applicantData: Applicant_create_request_pydantic) -> None:
        return await self.__applicantService.createApplicant(applicantData)
    

    @put('/updateApplicant', dependencies = [Depends(JWTBearer())], response_class = None)
    async def updateApplicant (self, applicantData: Applicant_update_request_pydantic) -> None:
        return await self.__applicantService.updateApplicant(applicantData)