from typing import (
    Dict, 
    List,
    Tuple,
    cast
)

import random
import json

from prisma import Json
from prisma.models import (
    Applicant,
    Department,
    Examination_sheet
)
from prisma.types import (
    ApplicantWhereInput,
    ApplicantInclude,
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


    async def getApplicantData (self, applicantData: Applicant_get_request_pydantic) -> Dict[ str, List[ Applicant ] | bool ] | List[Applicant]:
        includeParams: ApplicantInclude = { }

        if applicantData.includeFacultyData != None: includeParams['faculty'] = applicantData.includeFacultyData
        if applicantData.includeDepartmentData != None: includeParams['department'] = applicantData.includeDepartmentData
        if applicantData.includeStudyGroupData != None: includeParams['study_group'] = applicantData.includeStudyGroupData

        if applicantData.ids != None and len(applicantData.ids) == 1:
            applicantSingleData: Applicant | None = await prisma.applicant.find_unique(
                where = { 'id': applicantData.ids[0] }, 
                include = includeParams
            )

            if applicantSingleData == None: return [ ]
            else: return [ applicantSingleData ]
        else:
            whereParams: ApplicantWhereInput = { }

            if applicantData.ids != None: whereParams['id'] = { 'in': applicantData.ids }
            if applicantData.graduatedInstitutions != None: whereParams['graduatedInstitutions'] = cast(Json, json.dumps(applicantData.graduatedInstitutions))
            if applicantData.enrolled != None: whereParams['enrolled'] = applicantData.enrolled

            if applicantData.departmentId != None or applicantData.facultyId != None or applicantData.studyGroupId != None:  
                if applicantData.facultyId != None: whereParams['faculty'] = { 
                    'is': { 
                        'id': applicantData.facultyId 
                    }
                }
                    
                if applicantData.departmentId != None: whereParams['department'] = { 
                    'is': { 
                        'id': applicantData.departmentId 
                    }
                }
                    
                if applicantData.studyGroupId != None: whereParams['study_group'] = { 
                    'is': { 
                        'id': applicantData.studyGroupId 
                    }
                }
                    
            applicantDataList: List[Applicant] = await prisma.applicant.find_many(
                where = whereParams, 
                include = includeParams, 
                skip = applicantData.offsetCount, 
                take = applicantData.limitCount
            )
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
            'examination_sheet': {
                'create': { }
            },
            'faculty': { 'connect': { 'id': applicantData.facultyId }},
            'department': { 'connect': { 'id': applicantData.departmentId }},
            'study_group': { 'connect': { 'id': applicantData.studyGroupId }}
        }

        if applicantData.medal != None: createData['medal'] = applicantData.medal

        await prisma.applicant.create(data = createData)


    async def updateApplicant (self, applicantData: Applicant_update_request_pydantic) -> None:
        updateData: ApplicantUpdateInput = { }

        if applicantData.fullName != None: updateData['fullName'] = applicantData.fullName
        if applicantData.graduatedInstitutions != None: updateData['graduatedInstitutions'] = cast(Json, json.dumps(applicantData.graduatedInstitutions))
        if applicantData.medal != None: updateData['medal'] = applicantData.medal
        if applicantData.enrolled != None: updateData['enrolled'] = applicantData.enrolled

        if applicantData.facultyId != None: updateData['faculty'] = { 'connect': { 'id': applicantData.facultyId }}
        if applicantData.departmentId != None: updateData['department'] = { 'connect': { 'id': applicantData.departmentId }}
        if applicantData.studyGroupId != None: updateData['study_group'] = { 'connect': { 'id': applicantData.studyGroupId }}

        await prisma.applicant.update(data = updateData, where = { 'id': applicantData.id })

    
    async def fillRandomApplicantExamData (self):
        take: int = 4
        skip: int = 0

        commonApplicantCount: int = await prisma.applicant.count()

        await self.__fillRandomApplicantExamDataRecursive(commonApplicantCount, take, skip)
    

    async def __fillRandomApplicantExamDataRecursive (self, commonApplicantCount: int, take: int, skip: int, applicantData: List[Applicant] | None = None) -> None:
        if applicantData == None: applicantData = await prisma.applicant.find_many(take, skip)

        if len(applicantData) == 0: return

        for data in applicantData:
            await prisma.examination_sheet.update(data = { 
                'russianLanguage': random.randint(0, 101),
                'belarusianLanguage': random.randint(0, 101),
                'foreignLanguage': random.randint(0, 101),
                'worldHistory': random.randint(0, 101),
                'belarusHistory': random.randint(0, 101),
                'greatPatrioticWarHistory': random.randint(0, 101),
                'socialStudies': random.randint(0, 101),
                'socialScience': random.randint(0, 101),
                'mathematics': random.randint(0, 101)
            }, where = { 'id': data.id })

        skip += len(applicantData)

        if commonApplicantCount == skip: return
        else: await self.__fillRandomApplicantExamDataRecursive(commonApplicantCount, take, skip, None)
    

    async def createEnrolledApplicantList (self) -> None:
        departmentDataList: List[Department] = await prisma.department.find_many(include = { 'applicants': True })

        for departmentData in departmentDataList:
            currentApplicantDataList: List[Applicant] = cast(List[Applicant], departmentData.applicants)

            currentDepartmentPlacesNumber: int = departmentData.placesNumber
            currentSummaryApplicantExamsScoreList: List[ Tuple[ int, int, bool ] ] = await self.__culcSummaryApplicantExamsScoreList(currentApplicantDataList)

            suitableApplicantIds: List[int] = [ ]

            applicantExamsScoreWithMedalList: List[ Tuple[ int, int, bool ] ] = [ data for data in filter(lambda data: data[2] == True, currentSummaryApplicantExamsScoreList) ]

            if len(applicantExamsScoreWithMedalList) != 0: suitableApplicantIds.extend(map(lambda data: data[0], applicantExamsScoreWithMedalList))

            for applicantExamsScoreData in currentSummaryApplicantExamsScoreList:
                if len(suitableApplicantIds) != currentDepartmentPlacesNumber: suitableApplicantIds.append(applicantExamsScoreData[0])
            
            if len(suitableApplicantIds) != 0:
                for id in suitableApplicantIds: await prisma.applicant.update(data = { 'enrolled': True }, where = { 'id': id })
        

    async def __culcSummaryApplicantExamsScoreList (self, currentApplicantDataList: List[Applicant]) -> List[ Tuple[ int, int, bool ] ]:
        nonScoreExaminationSheetFields = ( 'id', 'applicantId' )

        currentSummaryApplicantExamsScoreList: List[ Tuple[ int, int, bool ] ] = [ ]

        for applicantData in currentApplicantDataList:
            currentExaminationSheet: Examination_sheet = cast(Examination_sheet, cast(Applicant, await prisma.applicant.find_first(where = { 'id': applicantData.id }, include = { 'examination_sheet': True })).examination_sheet)
            currentAverageApplicantExamsScore: int = 0
        
            for examinationSheetData in currentExaminationSheet:
                if examinationSheetData[0] not in nonScoreExaminationSheetFields and type(examinationSheetData[1]) == int:
                    currentAverageApplicantExamsScore += examinationSheetData[1]
                
            currentAverageApplicantExamsScore //= len(currentExaminationSheet.model_dump()) - len(nonScoreExaminationSheetFields)
                
            if applicantData.medal == False: currentSummaryApplicantExamsScoreList.append(( applicantData.id, currentAverageApplicantExamsScore, False ))
            else: currentSummaryApplicantExamsScoreList.append(( applicantData.id, currentAverageApplicantExamsScore, True ))
        
        return currentSummaryApplicantExamsScoreList