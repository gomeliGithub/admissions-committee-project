from typing import List

from fastapi import Depends

from fastapi_controllers import (
    Controller,
    get
)

from ..auth.auth_bearer import JWTBearer

from prisma.models import (
    Exam,
    Faculty,
    Department,
    Study_group,
    Specialty
)

from ..pydanticClasses.examData import (
    Department_get_request_pydantic,
    Exam_create_request_pydantic, 
    Exam_get_request_pydantic,
    Specialty_get_request_pydantic
)

from ..services.exam_service import ExamService


class ExamController (Controller):
    __examService: ExamService


    def __init__ (self, examService: ExamService = Depends(ExamService)) -> None:
        self.__examService = examService


    @get('/getExamData', dependencies = [Depends(JWTBearer())], response_class = List[Exam])
    async def getExamData (self, examData: Exam_get_request_pydantic):
        return await self.__examService.getExamData(examData)
    

    @get('/getFacultyData', dependencies = [Depends(JWTBearer())])
    async def getFacultyData (self) -> List[Faculty]:
        return await self.__examService.getFacultyData()
    

    @get('/getDepartmentData', dependencies = [Depends(JWTBearer())])
    async def getDepartmentData (self, examData: Department_get_request_pydantic = Depends()) -> List[Department]:
        return await self.__examService.getDepartmentData(examData)
    

    @get('/getStudyGroupData', dependencies = [Depends(JWTBearer())])
    async def getStudyGroupData (self) -> List[Study_group]:
        return await self.__examService.getStudyGroupData()


    @get('/getSpecialtyData', dependencies = [Depends(JWTBearer())], response_class = List[Specialty])
    async def getSpecialtyData (self, specialtyData: Specialty_get_request_pydantic):
        return await self.__examService.getSpecialtyData(specialtyData)
    

    @get('/createExam', dependencies = [Depends(JWTBearer())], response_class = None)
    async def createExam (self, examData: Exam_create_request_pydantic) -> None:
        return await self.__examService.createExam(examData)