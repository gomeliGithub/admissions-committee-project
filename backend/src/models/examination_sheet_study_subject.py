from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    mapped_column, 
    Mapped
)

from backend.src.database_connection import Base


class Examination_sheet_study_subject (Base):
    __tablename__ = 'examination_sheet_study_subjects'

    examination_sheet_id: Mapped[int] = mapped_column(ForeignKey('examination_sheets.id'), primary_key = True, autoincrement = 'auto')
    study_subject_id: Mapped[int] = mapped_column(ForeignKey('study_subjects.id'), primary_key = True, autoincrement = 'auto')