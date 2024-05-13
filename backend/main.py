from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.prisma import prisma

from src.controllers.applicant_controller import ApplicantController
from backend.src.controllers.exam_controller import ExamController


@asynccontextmanager
async def lifespan (app: FastAPI):
    await prisma.connect()

    yield

    await prisma.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(ApplicantController.create_router())
app.include_router(ExamController.create_router())