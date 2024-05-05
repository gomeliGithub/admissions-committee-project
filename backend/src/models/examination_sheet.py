from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    relationship, 
    mapped_column, 
    Mapped
)

from backend.src.database_connection import Base

from backend.src.models.applicant import Applicant
from backend.src.models.study_subject import Study_subject


class Examination_sheet (Base):
    __tablename__ = 'examination_sheets'

    id: Mapped[int] = mapped_column(primary_key = True, index = True, autoincrement = 'auto')

    applicant: Mapped['Applicant'] = relationship('applicant', back_populates = 'examination_sheet')
    study_subjects: Mapped[List['Study_subject']] = relationship(secondary = 'examination_sheet_study_subjects', back_populates = 'examination_sheets')

    applicant_id: Mapped[int] = mapped_column(ForeignKey('applicants.id'))