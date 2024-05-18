import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from src.prisma import prisma
from prisma.models import Admissions_committee_secretary

from argon2 import PasswordHasher

from src.controllers.applicant_controller import ApplicantController
from src.controllers.exam_controller import ExamController
from src.controllers.sign_controller import SignController
from src.controllers.common_controller import CommonController

from src.config.config import settings

os.environ['DATABASE_URL'] = settings['DATABASE_URL']


@asynccontextmanager
async def lifespan (app: FastAPI):
    await prisma.connect()

    await createAdmissionsCommitteeSecretary()

    yield

    await prisma.disconnect()


app = FastAPI(lifespan = lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings['CORS_ORIGIN'],
    allow_credentials = True,
    allow_methods = [ 'GET', 'POST', 'PUT', 'OPTIONS' ],
    allow_headers = [ 'Access-Control-Allow-Headers' , 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin' ]
)

app.include_router(ApplicantController.create_router(), prefix = '/api/applicant')
app.include_router(ExamController.create_router(), prefix = '/api/exam')
app.include_router(SignController.create_router(), prefix = '/api/sign')
app.include_router(CommonController.create_router(), prefix = '/api/main')


async def createAdmissionsCommitteeSecretary () -> None:
    existingSecretary: Admissions_committee_secretary | None = await prisma.admissions_committee_secretary.find_unique(where = { 'id': 1 })

    passwordHasher = PasswordHasher()

    passwordHash: str = passwordHasher.hash('12345Admin')

    if existingSecretary == None: 
        await prisma.admissions_committee_secretary.create(data = {
            'login': 'mainSecretary',
            'password': passwordHash
        })
    else: await prisma.admissions_committee_secretary.update(data = { 'password': passwordHash }, where = { 'id': 1 })