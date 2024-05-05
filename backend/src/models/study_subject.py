from typing import List

from sqlalchemy.orm import (
    relationship, 
    mapped_column, 
    Mapped
)

from backend.src.database_connection import Base

from backend.src.models.examination_sheet import Examination_sheet


class Study_subject (Base):
    __tablename__ = 'study_subjects'

    id: Mapped[int] = mapped_column(primary_key = True, index = True, autoincrement = 'auto')
    title: Mapped[str] = mapped_column(nullable = False)
    score: Mapped[int] = mapped_column(nullable = False, default = 0)

    examination_sheets: Mapped[List['Examination_sheet']] = relationship(secondary = 'examination_sheet_study_subjects', back_populates = 'study_subjects')