from fastapi import FastAPI

from backend.src.database_connection import bind_engine

from src.controllers.applicant_controller import ApplicantController
from backend.src.controllers.exam_controller import ExamController

bind_engine()

app = FastAPI() # создаем экземпляр приложения через конструктор

app.include_router(ApplicantController.create_router())
app.include_router(ExamController.create_router())