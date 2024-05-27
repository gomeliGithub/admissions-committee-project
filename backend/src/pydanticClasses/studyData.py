from typing import List

from datetime import (
    datetime
)

from fastapi import Query

from pydantic import (
    BaseModel, 
    Field
)

from prisma.models import Specialty


class Exam_get_request_pydantic (BaseModel):
    isConsultation: bool | None = Field(Query(default = None))
    studyGroupId: int | None = Field(Query(default = None, ge = 1))


class Department_get_request_pydantic (BaseModel):
    studentsAreShortage: bool | None = Field(Query(default = None))


class Exam_update_request_pydantic (BaseModel):
    id: int = Field(ge = 1)
    isConsultation: bool | None = Field(default = None)
    conductingDate: datetime | None = Field(default = None)
    classroom: str | None = Field(default = None)
    studyGroupId: int = Field(ge = 1)


class Specialty_get_response_pydantic (BaseModel):
    specialtyList: List[Specialty]
    commonPassingScore: int