from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_controllers import (
    Controller,
    get
)

from backend.src.database_connection import get_async_database_session

from backend.src.models.exam import Exam
from backend.src.models.specialty import Specialty

from backend.src.pydanticClasses.examData import (
    Department_get_request_pydantic,
    Exam_create_request_pydantic, 
    Exam_get_request_pydantic,
    Specialty_get_request_pydantic
)

from backend.src.services.exam_service import ExamService


class ExamController (Controller):
    __databaseSession: AsyncSession
    __examService: ExamService


    def __init__ (self, databaseSession: AsyncSession = Depends(get_async_database_session), examService: ExamService = Depends(ExamService)) -> None:
        self.__databaseSession = databaseSession
        self.__examService = examService


    @get('/getExamData', response_class = list[Exam])
    async def getExamData (self, examData: Exam_get_request_pydantic):
        return await self.__examService.getExamData(self.__databaseSession, examData)
    

    @get('/getDepartmentData', response_class = list[str])
    async def getDepartmentData (self, examData: Department_get_request_pydantic):
        return await self.__examService.getDepartmentData(self.__databaseSession, examData)


    @get('/getSpecialtyData', response_class = list[Specialty])
    async def getSpecialtyData (self, specialtyData: Specialty_get_request_pydantic):
        return await self.__examService.getSpecialtyData(self.__databaseSession, specialtyData)
    

    @get('/createExam', response_class = None)
    async def createExam (self, examData: Exam_create_request_pydantic) -> None:
        return await self.__examService.createExam(self.__databaseSession, examData)