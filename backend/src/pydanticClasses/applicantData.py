from pydantic import (
    BaseModel, 
    Field,
    field_validator
)

from backend.src.models.applicant import Applicant


class Applicant_get_request_pydantic (BaseModel):
    ids: list[int] | None
    graduatedInstitutions: list[str] | None
    enrolled: bool | None = Field(default = None)
    departmentId: int | None = Field(default = None, gt = 0)
    facultyId: int | None = Field(default = None, gt = 0)
    studyGroupId: int | None = Field(default = None, ge = 3)
    limitCount: int = Field(default = 4, gt = 4)
    offsetCount: int = Field(default = 0, gt = 0)


    @field_validator('ids')
    @classmethod
    def ensure_ids_length (cls, value: list[int | str]) -> list[int | str] | None:
        return ensure_list_length(value, 1)
    

    @field_validator('graduatedInstitutions')
    @classmethod
    def ensure_graduatedInstitutions_length (cls, value: list[int | str]) -> list[int | str] | None:
        return ensure_list_length(value, 1)



class Applicant_create_request_pydantic (BaseModel):
    fullName: str = Field(min_length = 10)
    graduatedInstitutions: list[str] = Field()
    medal: bool | None = Field(default = None)
    departmentId: int = Field(gt = 0)
    facultyId: int = Field(gt = 0)
    studyGroupId: int = Field(ge = 3)
    enrolled: bool | None = Field(default = None)


class Applicant_update_request_pydantic (BaseModel):
    fullName: str | None = Field(default = None, min_length = 10)
    graduatedInstitutions: list[str] | None
    medal: bool | None = Field(default = None, min_length = 5)
    departmentId: int | None = Field(default = None, gt = 0)
    facultyId: int | None = Field(default = None, gt = 0)
    studyGroupId: int | None = Field(default = None, ge = 3)
    enrolled: bool | None = Field(default = None)


    @field_validator('graduatedInstitutions')
    @classmethod
    def ensure_graduatedInstitutions_length (cls, value: list[int | str]) -> list[int | str] | None:
        return ensure_list_length(value, 1)


class Applicant_get_response_pydantic (BaseModel):
    applicantList: list[Applicant]
    nextApplicantsIsExists: bool


def ensure_list_length (listValue: list[int | str], minLength: int) -> list[int | str] | None:
    if len(listValue) < minLength: raise ValueError()
    elif listValue == None: return None
        
    return listValue