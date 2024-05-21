from typing import (
    Dict, 
    List,
    cast
)

import json

from prisma import Json
from prisma.models import Applicant
from prisma.types import (
    ApplicantWhereInput,
    ApplicantCreateInput,
    ApplicantUpdateInput
)
from src.prisma import prisma

from ..pydanticClasses.applicantData import (
    Applicant_create_request_pydantic, 
    Applicant_get_request_pydantic, 
    Applicant_update_request_pydantic
)


class ApplicantService:
    def __init__ (self):
        pass


    async def getApplicantData (self, applicantData: Applicant_get_request_pydantic) -> Dict[ str, List[ Applicant ] | bool ] | List[ Applicant | None ]:
        if applicantData.ids != None and len(applicantData.ids) == 1:
            applicantSingleData: Applicant | None = await prisma.applicant.find_unique(where = { 'id': applicantData.ids[0] })

            return [ applicantSingleData ]
        else:
            whereParams: ApplicantWhereInput = { }

            if applicantData.ids != None: whereParams['id'] = { 'in': applicantData.ids }
            if applicantData.graduatedInstitutions != None: whereParams['graduatedInstitutions'] = cast(Json, json.dumps(applicantData.graduatedInstitutions))
            if applicantData.enrolled != None: whereParams['enrolled'] = applicantData.enrolled

            if applicantData.departmentId != None or applicantData.facultyId != None or applicantData.studyGroupId != None:
                if applicantData.departmentId != None: whereParams['department'] = { 
                    'is': { 
                        'id': applicantData.departmentId 
                    }
                }
                    
                if applicantData.facultyId != None: whereParams['faculty'] = { 
                    'is': { 
                        'id': applicantData.facultyId 
                    }
                }
                    
                if applicantData.studyGroupId != None: whereParams['study_group'] = { 
                    'is': { 
                        'id': applicantData.studyGroupId 
                    }
                }
                    
            applicantDataList: List[Applicant] = await prisma.applicant.find_many(where = whereParams, skip = applicantData.offsetCount, take = applicantData.limitCount)
            commonApplicantCount: int | None = await prisma.applicant.count()


            nextApplicantsIsExists: bool = False

            if commonApplicantCount and ( commonApplicantCount > applicantData.offsetCount + len(applicantDataList) and commonApplicantCount > applicantData.limitCount ):
                nextApplicantsIsExists = True

            return { 
                'applicantList': applicantDataList,
                'nextApplicantsIsExists': nextApplicantsIsExists
            }


    async def createApplicant (self, applicantData: Applicant_create_request_pydantic) -> None:
        createData: ApplicantCreateInput = {
            'fullName': applicantData.fullName,
            'graduatedInstitutions': cast(Json, json.dumps(applicantData.graduatedInstitutions)),
            'department': { 'connect': { 'id': applicantData.departmentId } },
            'faculty': { 'connect': { 'id': applicantData.facultyId } },
            'study_group': { 'connect': { 'id': applicantData.studyGroupId } }
        }

        if applicantData.medal != None: createData['medal'] = applicantData.medal

        await prisma.applicant.create(data = createData)


    async def updateApplicant (self, applicantData: Applicant_update_request_pydantic) -> None:
        updateData: ApplicantUpdateInput = { }

        if applicantData.fullName != None: updateData['fullName'] = applicantData.fullName
        if applicantData.graduatedInstitutions != None: updateData['graduatedInstitutions'] = cast(Json, json.dumps(applicantData.graduatedInstitutions))
        if applicantData.medal != None: updateData['medal'] = applicantData.medal
        if applicantData.enrolled != None: updateData['enrolled'] = applicantData.enrolled

        if applicantData.departmentId != None: updateData['department'] = { 'connect': { 'id': applicantData.departmentId } }
        if applicantData.facultyId != None: updateData['faculty'] = { 'connect': { 'id': applicantData.facultyId } }
        if applicantData.studyGroupId != None: updateData['study_group'] = { 'connect': { 'id': applicantData.studyGroupId } }

        await prisma.applicant.update(data = updateData, where = { 'id': applicantData.id })