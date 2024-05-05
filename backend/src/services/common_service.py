from typing import Tuple
from sqlalchemy import (
    Select,
    func,
    select
)
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.applicant import Applicant
from backend.src.models.examination_sheet import Examination_sheet
from backend.src.models.faculty import Faculty
from backend.src.models.department import Department

from backend.src.pydanticClasses.applicantData import Applicant_get_request_pydantic

from backend.src.services.applicant_service import ApplicantService
from backend.src.services.exam_service import ExamService


class CommonService:
    def __init__ (self):
        pass


    async def getAllData (self, databaseSession: AsyncSession, applicantService: ApplicantService, examService: ExamService, applicantData: Applicant_get_request_pydantic):
        selectApplicantQuery: Select[Tuple[Applicant]] = select(Applicant).join(Examination_sheet.study_subjects).limit(applicantData.limitCount).offset(applicantData.offsetCount).group_by(Applicant.department)
        selectFacultiesPassingScoreQuery: Select[Tuple[int]] = select(Faculty.passingScore)
        selectDepartmentsPassingScoreQuery: Select[Tuple[int]] = select(Department.passingScore)
        enrolledApplicantDepartmentQuery: Select[Tuple[int]] = select(func.count().label('enrolledApplicants')).select_from(Applicant).where(Applicant.enrolled == True).group_by(Applicant.department)

        enrolledApplicantDepartmentQueryResult = ( await databaseSession.execute(enrolledApplicantDepartmentQuery) ).all()

        applicantDataList = ( await databaseSession.execute(selectApplicantQuery) ).all()

        facultiesPassingScore = ( await databaseSession.execute(selectFacultiesPassingScoreQuery) ).all()
        departmentsPassingScore = ( await databaseSession.execute(selectDepartmentsPassingScoreQuery) ).all()
        universityPassingScore: int = len(facultiesPassingScore) + len(departmentsPassingScore)

        enrolledApplicantDepartmentCount = enrolledApplicantDepartmentQueryResult
        enrolledApplicantUniversityCount = len(enrolledApplicantDepartmentQueryResult)

        return {
            applicantDataList: applicantDataList,
            facultiesPassingScore: facultiesPassingScore,
            departmentsPassingScore: departmentsPassingScore,
            universityPassingScore: universityPassingScore,
            enrolledApplicantDepartmentCount: enrolledApplicantDepartmentCount,
            enrolledApplicantUniversityCount: enrolledApplicantUniversityCount
        }