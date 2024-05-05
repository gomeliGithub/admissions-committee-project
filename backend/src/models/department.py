from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    relationship,
    mapped_column, 
    Mapped
)

from backend.src.database_connection import Base

from backend.src.models.applicant import Applicant


class Department (Base):
    __tablename__ = 'departments'

    id: Mapped[int] = mapped_column(primary_key = True, index = True, autoincrement = 'auto')
    title: Mapped[str] = mapped_column(nullable = False)
    placesNumber: Mapped[int] = mapped_column(nullable = False)
    passingScore: Mapped[int] = mapped_column(nullable = False)
    studentsAreShortage: Mapped[bool] = mapped_column(nullable = False, default = False)

    applicant: Mapped['Applicant'] = relationship('applicant', back_populates = 'examination_sheet')

    applicant_id: Mapped[int] = mapped_column(ForeignKey('applicants.id'))
    faculty_id: Mapped[int] = mapped_column(ForeignKey('faculties.id'))