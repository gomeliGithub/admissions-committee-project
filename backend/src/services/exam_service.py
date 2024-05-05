from typing import Tuple

from sqlalchemy import (
    ColumnElement,
    Insert,
    Select,
    insert,
    select
)
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.department import Department
from backend.src.models.exam import Exam
from backend.src.models.specialty import Specialty
from backend.src.models.study_group import Study_group
from backend.src.models.study_subject import Study_subject

from backend.src.pydanticClasses.examData import (
    Department_get_request_pydantic,
    Exam_create_request_pydantic, 
    Exam_get_request_pydantic,
    Specialty_get_request_pydantic
)


class ExamService:
    def __init__ (self):
        pass


    async def getExamData (self, databaseSession: AsyncSession, examData: Exam_get_request_pydantic):
        selectQuery: Select[Tuple[Exam]] = select(Exam)

        whereParams: list[ColumnElement[bool]] = [ ]

        if examData.studySubjectId != None: selectQuery = selectQuery.join(Study_subject, Study_subject.id == examData.studySubjectId)
        if examData.isConsultation != None: whereParams.append(Exam.isConsultation == examData.isConsultation)

        selectQuery = selectQuery.where(*whereParams)

        examDataList = ( await databaseSession.execute(selectQuery) ).all()

        return examDataList
    

    async def getDepartmentData (self, databaseSession: AsyncSession, examData: Department_get_request_pydantic):
        selectQuery: Select[Tuple[Department]] = select(Department)

        whereParams: list[ColumnElement[bool]] = [ ]

        if examData.studentsAreShortage != None: whereParams.append(Department.studentsAreShortage == examData.studentsAreShortage)

        selectQuery = selectQuery.where(*whereParams)

        departmentDataList = ( await databaseSession.execute(selectQuery) ).all()

        return departmentDataList
    

    async def getSpecialtyData (self, databaseSession: AsyncSession, specialtyData: Specialty_get_request_pydantic):
        specialtyFields: list[InstrumentedAttribute[int]] = [ ]

        if specialtyData.includePassingScore == True: specialtyFields.append(Specialty.passingScore)
        if specialtyData.includeCompetition == True: specialtyFields.append(Specialty.competition)

        selectQuery: Select[Tuple[Specialty]] = select(*specialtyFields)

        specialtyDataList = ( await databaseSession.execute(selectQuery) ).all()

        return specialtyDataList
    

    async def createExam (self, databaseSession: AsyncSession, examData: Exam_create_request_pydantic) -> None:
        insertQuery: Insert = insert(Exam)

        studyGroupInstance: Study_group | None = None

        if examData.studyGroupId != None: studyGroupInstance = await databaseSession.get(Study_group, examData.studyGroupId)
        del examData.studyGroupId

        insertQuery = insertQuery.values(examData.model_dump())

        examInstance: Exam | None = ( await databaseSession.execute(insertQuery) ).scalars().unique().first()

        if examInstance != None and studyGroupInstance != None: studyGroupInstance.exams.append(examInstance)