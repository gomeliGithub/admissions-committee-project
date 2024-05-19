# import datetime as datetime_module
from datetime import (
    datetime, 
    timedelta
)

from fastapi import Query
from pydantic import (
    BaseModel, 
    Field,
    field_validator
)


class Exam_get_request_pydantic (BaseModel):
    studySubjectId: int | None = Field(Query(default = None, ge = 0))
    isConsultation: bool | None = Field(Query(default = None))


class Department_get_request_pydantic (BaseModel):
    studentsAreShortage: bool | None = Field(Query(default = None))


class Specialty_get_request_pydantic (BaseModel):
    includePassingScore: bool = Field(Query(default = True))
    includeCompetition: bool = Field(Query(default = True))


class Exam_create_request_pydantic (BaseModel):
    isConsultation: bool | None = Field(default = None)
    conductingDate: datetime
    classroom: str = Field(min_length = 10)
    studyGroupId: int = Field(gt = 0)


    @field_validator('conductingDate')
    def ensure_date_range (cls, value: datetime) -> datetime:
        if datetime.now() + timedelta(15) <= value: raise ValueError()
        
        return value