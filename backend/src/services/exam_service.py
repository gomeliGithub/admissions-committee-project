from typing import List, Tuple

from prisma.models import (
    Exam,
    Department,
    Specialty
)
from prisma.types import (
    ExamWhereInput,
    DepartmentWhereInput,
    SpecialtyWhereInput,
    ExamCreateInput
)
from src.prisma import prisma

from backend.src.pydanticClasses.examData import (
    Department_get_request_pydantic,
    Exam_create_request_pydantic, 
    Exam_get_request_pydantic,
    Specialty_get_request_pydantic
)


class ExamService:
    def __init__ (self):
        pass


    async def getExamData (self, examData: Exam_get_request_pydantic):
        whereParams: ExamWhereInput = { }

        # if examData.studySubjectId != None: selectQuery = selectQuery.join(Study_subject, Study_subject.id == examData.studySubjectId)
        if examData.isConsultation != None: whereParams['isConsultation'] = examData.isConsultation

        examDataList: List[Exam] = await prisma.exam.find_many(where = whereParams)

        return examDataList
    

    async def getDepartmentData (self, examData: Department_get_request_pydantic):
        whereParams: DepartmentWhereInput = { }

        if examData.studentsAreShortage != None: whereParams['studentsAreShortage'] = examData.studentsAreShortage

        departmentDataList: List[Department] = await prisma.department.find_many(where = whereParams)

        return departmentDataList
    

    async def getSpecialtyData (self, specialtyData: Specialty_get_request_pydantic):
        whereParams: SpecialtyWhereInput = { }

        if specialtyData.includePassingScore == True: whereParams['passingScore'] = True
        if specialtyData.includeCompetition == True: whereParams['competition'] = True

        specialtyDataList: List[Specialty] = await prisma.specialty.find_many(where = whereParams)

        return specialtyDataList
    

    async def createExam (self, examData: Exam_create_request_pydantic) -> None:
        whereParams: ExamCreateInput = {
            'isConsultation': examData.isConsultation,
            'conductingDate': examData.conductingDate,
            'classroom': examData.classroom
        }

        if examData.studyGroupId != None: whereParams['study_group'] = { 'connect': { 'id': examData.studyGroupId } }

        await prisma.exam.create(data = whereParams)