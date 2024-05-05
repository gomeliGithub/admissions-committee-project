import datetime as datetime_module
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    mapped_column, 
    Mapped
)

from backend.src.database_connection import Base


class Exam (Base):
    __tablename__ = 'exams'

    id: Mapped[int] = mapped_column(primary_key = True, index = True, autoincrement = 'auto')
    isConsultation: Mapped[bool] = mapped_column(nullable = False, default = False)
    conductingDate: Mapped[datetime] = mapped_column(nullable = False)
    classroom: Mapped[str] = mapped_column(nullable = False)
    createDate: Mapped[datetime] = mapped_column(nullable = False, default = datetime.now(datetime_module.timezone.utc))

    study_group_id: Mapped[Optional[int]] = mapped_column(ForeignKey('study_groups.id'), nullable = True)