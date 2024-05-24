from typing import List

from prisma.models import (
    Exam,
    Faculty,
    Department,
    Study_group,
    Specialty
)
from prisma.types import (
    ExamWhereInput,
    FacultyWhereInput,
    DepartmentWhereInput,
    Study_groupWhereInput,
    SpecialtyWhereInput,
    ExamUpdateInput
)
from src.prisma import prisma

from ..pydanticClasses.studyData import (
    Department_get_request_pydantic,
    Exam_get_request_pydantic,
    Exam_update_request_pydantic
)


class StudyService:
    def __init__ (self):
        pass
    

    async def getFacultyData (self) -> List[Faculty]:
        whereParams: FacultyWhereInput = { }

        facultyDataList: List[Faculty] = await prisma.faculty.find_many(where = whereParams)

        return facultyDataList


    async def getDepartmentData (self, examData: Department_get_request_pydantic) -> List[Department]:
        whereParams: DepartmentWhereInput = { }

        if examData.studentsAreShortage != None: whereParams['studentsAreShortage'] = examData.studentsAreShortage

        departmentDataList: List[Department] = await prisma.department.find_many(where = whereParams)

        return departmentDataList
    

    async def getStudyGroupData (self) -> List[Study_group]:
        whereParams: Study_groupWhereInput = { }

        studyGroupList: List[Study_group] = await prisma.study_group.find_many(where = whereParams)

        return studyGroupList
    

    async def getExamData (self, examData: Exam_get_request_pydantic):
        whereParams: ExamWhereInput = { }

        if examData.studyGroupId != None: whereParams['study_group'] = { 'is': { 'id': examData.studyGroupId }}
        if examData.isConsultation != None: whereParams['isConsultation'] = examData.isConsultation

        examDataList: List[Exam] = await prisma.exam.find_many(where = whereParams)

        return examDataList
    

    async def getSpecialtyData (self):
        specialtyDataList: List[Specialty] = await prisma.specialty.find_many()

        commonPassingScore: int = 0

        for data in specialtyDataList:
            commonPassingScore += data.passingScore
        
        commonPassingScore = commonPassingScore // len(specialtyDataList)

        return {
            'specialtyList': specialtyDataList,
            'commonPassingScore': commonPassingScore
        }
    

    async def updateExam (self, examData: Exam_update_request_pydantic) -> None:
        updateData: ExamUpdateInput = { }

        if examData.isConsultation != None: updateData['isConsultation'] = examData.isConsultation
        if examData.conductingDate != None: updateData['conductingDate'] = examData.conductingDate
        if examData.classroom != None: updateData['classroom'] = examData.classroom

        if examData.studyGroupId != None: updateData['study_group'] = { 'connect': { 'id': examData.studyGroupId } }

        await prisma.exam.update(data = updateData, where = { 'id': examData.id })