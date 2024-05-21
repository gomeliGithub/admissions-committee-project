from typing import cast
import json

from fastapi import Query
from pydantic import (
    BaseModel, 
    Field,
    field_validator
)

from prisma.models import Applicant


class Applicant_get_request_pydantic (BaseModel):
    ids: list[int] | None = Field(Query(default = None))
    graduatedInstitutions: list[str] | None = Field(Query(default = None))
    enrolled: bool | None = Field(Query(default = None))
    departmentId: int | None = Field(Query(default = None, gt = 0))
    facultyId: int | None = Field(Query(default = None, gt = 0))
    studyGroupId: int | None = Field(Query(default = None, ge = 3))
    limitCount: int = Field(Query(default = 4, gt = 4))
    offsetCount: int = Field(Query(default = 0, ge = 0))


    @field_validator('ids')
    @classmethod
    def ensure_ids_length (cls, value: str | None) -> list[int | str] | None:
        return listLengthValidator(value, 1)
    

    @field_validator('graduatedInstitutions')
    @classmethod
    def ensure_graduatedInstitutions_length (cls, value: str | None) -> list[int | str] | None:
        return listLengthValidator(value, 1)



class Applicant_create_request_pydantic (BaseModel):
    fullName: str = Field(min_length = 10)
    graduatedInstitutions: list[str] = Field()
    medal: bool | None = Field(default = None)
    departmentId: int = Field(gt = 0)
    facultyId: int = Field(gt = 0)
    studyGroupId: int = Field(ge = 1)

    @field_validator('graduatedInstitutions')
    @classmethod
    def ensure_graduatedInstitutions_length (cls, value: str) -> list[int | str] | None:
        return listLengthValidator(value, 1)


class Applicant_update_request_pydantic (BaseModel):
    id: int = Field(ge = 1)
    fullName: str | None = Field(default = None, min_length = 10)
    graduatedInstitutions: list[str] | None = Field()
    medal: bool | None = Field(default = None, min_length = 5)
    departmentId: int | None = Field(default = None, gt = 0)
    facultyId: int | None = Field(default = None, gt = 0)
    studyGroupId: int | None = Field(default = None, ge = 3)
    enrolled: bool | None = Field(default = None)


    @field_validator('graduatedInstitutions')
    @classmethod
    def ensure_graduatedInstitutions_length (cls, value: list[int | str] | None) -> list[int | str] | None:
        return listLengthValidator(value, 1)


class Applicant_get_response_pydantic (BaseModel):
    applicantList: list[Applicant]
    nextApplicantsIsExists: bool


def listLengthValidator (value: str | list[int | str] | None, minLength: int) -> list[int | str] | None:
    decodedListValue: list[ int | str ] | None = None

    if value != None and type(value) == "<class 'str'>": decodedListValue = json.loads(cast(str, value))
    else: decodedListValue = cast(list[int | str] | None, value)

    if decodedListValue == None: return decodedListValue

    if len(decodedListValue) < minLength: raise ValueError()
    elif decodedListValue == None: return None
        
    return decodedListValue