from sqlalchemy import JSON
from sqlalchemy.orm import (
    relationship,
    mapped_column,
    Mapped
)

from backend.src.database_connection import Base

from backend.src.models.department import Department
from backend.src.models.examination_sheet import Examination_sheet
from backend.src.models.faculty import Faculty
from backend.src.models.study_group import Study_group


class Applicant (Base):
    __tablename__ = 'applicants'
    
    id: Mapped[int] = mapped_column(primary_key = True, index = True, autoincrement = 'auto')
    fullName: Mapped[str] = mapped_column(nullable = False)
    graduatedInstitutions: Mapped[ list[str] ] = mapped_column(type_ = JSON, nullable = False)
    medal: Mapped[bool] = mapped_column(nullable = False, default = False)
    enrolled: Mapped[bool] = mapped_column(nullable = False, default = False)

    study_group: Mapped[Study_group] = relationship('study_group', back_populates = 'applicant', uselist = False)
    examination_sheet: Mapped[Examination_sheet] = relationship('examination_sheet', back_populates = 'applicant', uselist = False)
    department: Mapped[Department] = relationship('department', back_populates = 'applicant', uselist = False)
    faculty: Mapped[Faculty] = relationship('faculty', back_populates = 'applicant', uselist = False)