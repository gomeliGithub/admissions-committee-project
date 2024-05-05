from sqlalchemy.orm import (
    relationship,
    mapped_column, 
    Mapped
)

from backend.src.database_connection import Base

from backend.src.models.department import Department
from backend.src.models.faculty import Faculty


class Specialty (Base):
    __tablename__ = 'specialties'

    id: Mapped[int] = mapped_column(primary_key = True, index = True, autoincrement = 'auto')
    passingScore: Mapped[int] = mapped_column(nullable = False)
    competition: Mapped[int] = mapped_column(nullable = False)

    faculty: Mapped[Faculty] = relationship('faculty', back_populates = 'specialty', uselist = False)
    department: Mapped[Department] = relationship('department', back_populates = 'specialty', uselist = False)