from typing import (
    Dict, 
    List,
    cast
)

from src.prisma import prisma
from prisma.models import (
    Applicant,
    Department
)

from python_ms import ms

from ..config.config import settings

from ..pydanticClasses.applicantData import Applicant_get_request_pydantic

from ..services.applicant_service import ApplicantService


class CommonService:
    def __init__ (self):
        pass


    cookieParameters = {
        'max_age': cast(int, ms.parse_time(settings['COOKIE_MAXAGE_TIME'])),
        'expires': None,
        'path': '/',
        'domain': None,
        'secure': False,
        'httponly': False,
        'samesite': 'strict'
    }

    async def getAllData (self, applicantService: ApplicantService, applicantData: Applicant_get_request_pydantic) -> Dict[ str, Dict[str, List[Applicant] | bool] | List[int] | list[Dict[str, str | int]] | int ]:
        applicantDataList: Dict[ str, List[ Applicant ] | bool ] = cast(Dict[ str, List[ Applicant ] | bool ], await applicantService.getApplicantData(applicantData))
        facultiesPassingScore: List[int] = [ passingScore for passingScore in map(lambda faculty: faculty.passingScore, await prisma.faculty.find_many(where = { 'passingScore': True })) ]
        departmentsPassingScore: List[int] = [ passingScore for passingScore in map(lambda department: department.passingScore, await prisma.department.find_many(where = { 'passingScore': True })) ]

        universityPassingScore: int = 0
        commonCount: int = 0
        index: int = 0

        while index < len(facultiesPassingScore) - 1:
            currentCount: str | int | None = facultiesPassingScore[index]

            commonCount += currentCount

            index =+ 1
        else:
            universityPassingScore = commonCount // len(facultiesPassingScore)

        enrolledApplicantDepartmentsCount: List[ Dict[ str, str | int ] ] = [ ]
        departmentsData: List[Department] = await prisma.department.find_many()

        for department in departmentsData:
            applicantCount: int = await prisma.applicant.count(where = { 'enrolled': True, 'departmentId': department.id })

            enrolledApplicantDepartmentsCount.append({ 'title': department.title, 'count': applicantCount })

        enrolledApplicantUniversityCount: int = 0
        commonCount: int = 0
        index = 0

        while index < len(enrolledApplicantDepartmentsCount) - 1:
            currentObj: Dict[str, str | int] = enrolledApplicantDepartmentsCount[index]
            currentCount: str | int | None = currentObj.get('count')

            if currentCount != None: commonCount += int(currentCount)

            index =+ 1
        else:
            enrolledApplicantUniversityCount = commonCount

        return {
            'applicantDataList': applicantDataList,
            'facultiesPassingScore': facultiesPassingScore,
            'departmentsPassingScore': departmentsPassingScore,
            'universityPassingScore': universityPassingScore,
            'enrolledApplicantDepartmentsCount': enrolledApplicantDepartmentsCount,
            'enrolledApplicantUniversityCount': enrolledApplicantUniversityCount
        }