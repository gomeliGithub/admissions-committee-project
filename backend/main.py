import os
from typing import (
    Dict,
    List, 
    Set,
    cast
)
from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from src.prisma import prisma
from prisma.types import (
    DepartmentCreateWithoutRelationsInput,
    SpecialtyCreateWithoutRelationsInput,
    ExamWhereUniqueInput
)
from prisma.models import (
    Admissions_committee_secretary,
    Faculty,
    Study_group
)

from argon2 import PasswordHasher

from src.controllers.applicant_controller import ApplicantController
from src.controllers.study_controller import StudyController
from src.controllers.sign_controller import SignController
from src.controllers.common_controller import CommonController

from src.config.config import settings

os.environ['DATABASE_URL'] = settings['DATABASE_URL']

FACULTIES_AND_DEPARTMENTS_TITLE_DICT: Dict[ str, Dict[ str, Set[str]  | Dict[ str, set[str] ] ] ] = settings['FACULTIES_AND_DEPARTMENTS_TITLE_DICT']
STUDY_SUBJECT_SET: Set[str] = settings['STUDY_SUBJECT_SET']
STUDY_GROUPS_TITLE_SET: Set[str] = settings['STUDY_GROUPS_TITLE_SET']


@asynccontextmanager
async def lifespan (app: FastAPI):
    await prisma.connect()

    await createOrUpdateAdmissionsCommitteeSecretary()
    await createStudyData()

    yield

    await prisma.disconnect()


app = FastAPI(lifespan = lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings['CORS_ORIGIN'],
    allow_credentials = True,
    allow_methods = [ 'GET', 'POST', 'PUT', 'OPTIONS' ],
    allow_headers = [ '*' ]
)

app.include_router(ApplicantController.create_router(), prefix = '/api/applicant')
app.include_router(StudyController.create_router(), prefix = '/api/study')
app.include_router(SignController.create_router(), prefix = '/api/sign')
app.include_router(CommonController.create_router(), prefix = '/api/main')


async def createOrUpdateAdmissionsCommitteeSecretary () -> None:
    existingSecretaryData: Admissions_committee_secretary | None = await prisma.admissions_committee_secretary.find_unique(where = { 'id': 1 })

    passwordHasher = PasswordHasher()

    passwordHash: str = passwordHasher.hash('12345Admin')

    if existingSecretaryData == None: 
        await prisma.admissions_committee_secretary.create(data = {
            'login': 'mainSecretary',
            'password': passwordHash
        })
    else: await prisma.admissions_committee_secretary.update(data = { 'password': passwordHash }, where = { 'id': 1 })


async def createStudyData () -> None:
    for facultyTitle in FACULTIES_AND_DEPARTMENTS_TITLE_DICT:
        existingFacultyData: Faculty | None = await prisma.faculty.find_unique(where = { 'title': facultyTitle })

        if existingFacultyData == None:
            currentFacultyRelationDict: Dict[str, Set[str] | Dict[str, set[str]]] = cast(Dict[str, Set[str] | Dict[str, set[str]]], FACULTIES_AND_DEPARTMENTS_TITLE_DICT.get(facultyTitle))
            currentDepartmentsTitleList: List[DepartmentCreateWithoutRelationsInput] = []
            currentSpecialtiesTitleList: List[SpecialtyCreateWithoutRelationsInput] = []
            
            for departmentTitle in currentFacultyRelationDict['departmentsTitle']:
                currentDepartmentsTitleList.append({ 'title': departmentTitle })
            
            for specialtyTitle in currentFacultyRelationDict['specialtiesTitle']:
                currentSpecialtiesTitleList.append({ 'title': specialtyTitle })

            await prisma.faculty.create(data = {
                'title': facultyTitle,
                'departments': {
                    'create': currentDepartmentsTitleList
                },
                'specialties': {
                    'create': currentSpecialtiesTitleList
                }
            })

    datetimeNow: datetime = datetime.now()
    index: int = 0

    commonExamCount: int = await prisma.exam.count()

    for _ in STUDY_SUBJECT_SET:
        index += 1

        if commonExamCount == 0:
            await prisma.exam.create(data = {
                'conductingDate': datetimeNow + timedelta(days = index + 1),
                'classroom': f'Т-{ index }'
            })

    index = 1

    for studyGroupTitle in STUDY_GROUPS_TITLE_SET:
        existingStudyGroupData: Study_group | None = await prisma.study_group.find_unique(where = { 'title': studyGroupTitle })

        if existingStudyGroupData == None:
            currentExamIdsList: List[ExamWhereUniqueInput] = []

            for examId in range(index, index + 3):
                currentExamIdsList.append({ 'id': examId })

                index += 1

            await prisma.study_group.create(data = {
                'title': studyGroupTitle,
                'exams': { 'connect': currentExamIdsList }
            })