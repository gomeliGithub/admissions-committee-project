from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    relationship,
    mapped_column,
    Mapped
)

from backend.src.database_connection import Base

from backend.src.models.applicant import Applicant
from backend.src.models.exam import Exam


class Study_group (Base):
    __tablename__ = 'study_groups'

    id: Mapped[int] = mapped_column(primary_key = True, index = True, autoincrement = 'auto')
    title: Mapped[str] = mapped_column(nullable = False)

    exams: Mapped[List['Exam']] = relationship('exam')
    applicant: Mapped['Applicant'] = relationship('applicant', back_populates = 'study_group')

    applicant_id: Mapped[int] = mapped_column(ForeignKey('applicants.id'))