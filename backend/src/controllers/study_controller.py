from typing import List

from fastapi import Depends

from fastapi_controllers import (
    Controller,
    get,
    put
)

from ..auth.auth_bearer import JWTBearer

from prisma.models import (
    Exam,
    Faculty,
    Department,
    Study_group
)

from ..pydanticClasses.studyData import (
    Department_get_request_pydantic,
    Exam_get_request_pydantic,
    Exam_update_request_pydantic,
    Specialty_get_response_pydantic
)

from ..services.study_service import StudyService


class StudyController (Controller):
    __studyService: StudyService


    def __init__ (self, studyService: StudyService = Depends(StudyService)) -> None:
        self.__studyService = studyService

    
    @get('/getFacultyData', dependencies = [Depends(JWTBearer())])
    async def getFacultyData (self) -> List[Faculty]:
        return await self.__studyService.getFacultyData()
    

    @get('/getDepartmentData', dependencies = [Depends(JWTBearer())])
    async def getDepartmentData (self, examData: Department_get_request_pydantic = Depends()) -> List[Department]:
        return await self.__studyService.getDepartmentData(examData)
    

    @get('/getStudyGroupData', dependencies = [Depends(JWTBearer())])
    async def getStudyGroupData (self) -> List[Study_group] :
        return await self.__studyService.getStudyGroupData()
    

    @get('/getExamData', dependencies = [Depends(JWTBearer())])
    async def getExamData (self, examData: Exam_get_request_pydantic = Depends()) -> List[Exam]:
        return await self.__studyService.getExamData(examData)


    @get('/getSpecialtyData', dependencies = [Depends(JWTBearer())], response_model = Specialty_get_response_pydantic)
    async def getSpecialtyData (self):
        return await self.__studyService.getSpecialtyData()
    

    @put('/updateExam', dependencies = [Depends(JWTBearer())])
    async def updateExam (self, examData: Exam_update_request_pydantic) -> None:
        return await self.__studyService.updateExam(examData)