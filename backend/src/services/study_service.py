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
    ExamCreateInput
)
from src.prisma import prisma

from ..pydanticClasses.examData import (
    Department_get_request_pydantic,
    Exam_create_request_pydantic, 
    Exam_get_request_pydantic,
    Specialty_get_request_pydantic
)


class StudyService:
    def __init__ (self):
        pass


    async def getExamData (self, examData: Exam_get_request_pydantic):
        whereParams: ExamWhereInput = { }

        # if examData.studySubjectId != None: selectQuery = selectQuery.join(Study_subject, Study_subject.id == examData.studySubjectId)
        if examData.isConsultation != None: whereParams['isConsultation'] = examData.isConsultation

        examDataList: List[Exam] = await prisma.exam.find_many(where = whereParams)

        return examDataList
    

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
    

    async def getSpecialtyData (self, specialtyData: Specialty_get_request_pydantic):
        whereParams: SpecialtyWhereInput = { }

        if specialtyData.includePassingScore == True: whereParams['passingScore'] = True
        if specialtyData.includeCompetition == True: whereParams['competition'] = True

        specialtyDataList: List[Specialty] = await prisma.specialty.find_many(where = whereParams)

        return specialtyDataList
    

    async def createExam (self, examData: Exam_create_request_pydantic) -> None:
        whereParams: ExamCreateInput = {
            'conductingDate': examData.conductingDate,
            'classroom': examData.classroom
        }

        if examData.isConsultation != None: whereParams['isConsultation'] = examData.isConsultation

        if examData.studyGroupId != None: whereParams['study_group'] = { 'connect': { 'id': examData.studyGroupId } }

        await prisma.exam.create(data = whereParams)