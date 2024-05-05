from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    relationship,
    mapped_column,
    Mapped
)

from backend.src.database_connection import Base

from backend.src.models.applicant import Applicant
from backend.src.models.department import Department


class Faculty (Base):
    __tablename__ = 'faculties'

    id: Mapped[int] = mapped_column(primary_key = True, index = True, autoincrement = 'auto')
    title: Mapped[str] = mapped_column(nullable = False)
    passingScore: Mapped[int] = mapped_column(nullable = False)

    departments: Mapped[List['Department']] = relationship('department')
    applicant: Mapped['Applicant'] = relationship('applicant', back_populates = 'faculty')

    applicant_id: Mapped[int] = mapped_column(ForeignKey('applicants.id'))