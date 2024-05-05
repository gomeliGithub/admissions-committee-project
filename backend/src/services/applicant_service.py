from sqlalchemy import (
    ColumnElement, 
    Insert,
    Select,
    Update, 
    func, 
    insert, 
    select, 
    update
)
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.department import Department
from backend.src.pydanticClasses.applicantData import (
    Applicant_create_request_pydantic, 
    Applicant_get_request_pydantic, 
    Applicant_update_request_pydantic
)

from backend.src.models.applicant import Applicant
from backend.src.models.faculty import Faculty
from backend.src.models.study_group import Study_group


class ApplicantService:
    def __init__ (self):
        pass
    

    async def getApplicantData (self, databaseSession: AsyncSession, applicantData: Applicant_get_request_pydantic):
        if applicantData.ids != None and len(applicantData.ids) == 1:
            applicantSingleData: Applicant | None = await databaseSession.get(Applicant, applicantData.ids[0])

            return [ applicantSingleData ]
        else:
            selectQuery: Select[tuple[Applicant]] = select(Applicant)
            countQuery: Select[tuple[int]] = select(func.count()).select_from(Applicant)

            whereParams: list[ColumnElement[bool]] = [ ]

            if applicantData.ids != None: whereParams.append(Applicant.id == applicantData.ids)
            if applicantData.graduatedInstitutions != None: whereParams.append(Applicant.graduatedInstitutions == applicantData.graduatedInstitutions)
            if applicantData.enrolled != None: whereParams.append(Applicant.enrolled == applicantData.enrolled)

            ####################################################################################################################



            if applicantData.departmentId != None or applicantData.facultyId != None or applicantData.studyGroupId != None:
                if applicantData.departmentId != None: selectQuery = selectQuery.join(Department, Department.id == applicantData.departmentId)
                if applicantData.facultyId != None: selectQuery = selectQuery.join(Faculty, Faculty.id == applicantData.facultyId)
                if applicantData.studyGroupId != None: selectQuery = selectQuery.join(Study_group, Study_group.id == applicantData.studyGroupId)



            ####################################################################################################################

            selectQuery = selectQuery.where(*whereParams)
            selectQuery = selectQuery.limit(applicantData.limitCount)
            selectQuery = selectQuery.offset(applicantData.offsetCount)
            
            applicantDataList = ( await databaseSession.execute(selectQuery) ).all()
            # applicantDataList: list[Applicant] = []
            commonApplicantCount: int | None = ( await databaseSession.execute(countQuery) ).scalar()

            ####################################################################################################################



            # if applicantData.facultyId != None or applicantData.studyGroupId != None:
            #    applicantDataList = await self.__sortApplicantData(databaseSession, applicantData, selectQuery)



            ####################################################################################################################
            
            nextApplicantsIsExists: bool = False

            if commonApplicantCount and ( commonApplicantCount > applicantData.offsetCount + len(applicantDataList) and commonApplicantCount > applicantData.limitCount ):
                nextApplicantsIsExists = True

            return { 
                'applicantList': applicantDataList,
                'nextApplicantsIsExists': nextApplicantsIsExists
            }


    async def createApplicant (self, databaseSession: AsyncSession, applicantData: Applicant_create_request_pydantic) -> None:
        insertQuery: Insert = insert(Applicant)

        await self.__executeChangeQuery(databaseSession, insertQuery, applicantData.model_dump(), applicantData)


    async def updateApplicant (self, databaseSession: AsyncSession, applicantData: Applicant_update_request_pydantic):
        updateQuery: Update = update(Applicant)

        updateValues: dict[ str, str | int | bool | dict[ int, str ] | list[str] ] = {}

        if applicantData.fullName != None: updateValues['fullName'] = applicantData.fullName
        if applicantData.graduatedInstitutions != None: updateValues['graduatedInstitutions'] = applicantData.graduatedInstitutions
        if applicantData.medal != None: updateValues['medal'] = applicantData.medal

        await self.__executeChangeQuery(databaseSession, updateQuery, updateValues, applicantData)


    async def __executeChangeQuery (self, databaseSession: AsyncSession, query: Insert | Update, 
        values: dict[ str, str | int | bool | dict[ int, str ] | list[str] ], 
        applicantData: Applicant_create_request_pydantic | Applicant_update_request_pydantic
    ) -> None:
        departmentInstance: Department | None = None
        facultyInstance: Faculty | None = None
        studyGroupInstance: Study_group | None = None

        applicantInstance: Applicant | None = None

        if applicantData.departmentId != None: departmentInstance = await databaseSession.get(Department, applicantData.departmentId)
        if applicantData.facultyId != None: facultyInstance = await databaseSession.get(Faculty, applicantData.facultyId)
        if applicantData.studyGroupId != None: studyGroupInstance = await databaseSession.get(Study_group, applicantData.studyGroupId)

        del applicantData.facultyId
        del applicantData.studyGroupId
    
        query = query.values(values)

        applicantInstance: Applicant | None = ( await databaseSession.execute(query) ).scalars().unique().first()

        if applicantInstance != None:
            if departmentInstance != None: applicantInstance.department = departmentInstance
            if facultyInstance != None: applicantInstance.faculty = facultyInstance
            if studyGroupInstance != None: applicantInstance.study_group = studyGroupInstance
    
    ####################################################################################################################
    

    
    async def __sortApplicantData (self, databaseSession: AsyncSession, applicantData: Applicant_get_request_pydantic, selectQuery: Select[tuple[Applicant]]) -> list[Applicant]:
        applicantDataList = ( await databaseSession.execute(selectQuery) ).all()
        applicantDataSortedList: list[Applicant] = []

        if applicantData.departmentId != None or applicantData.facultyId != None or applicantData.studyGroupId != None:
            for applicantDataRow in applicantDataList:
                applicantDataDict: dict[ str, int | str | bool ] = applicantDataRow._asdict()

                applicantInstance: Applicant | None = await databaseSession.get(Applicant, applicantDataDict['id'])

                departmentInstance: Department | None = None
                facultyInstance: Faculty | None = None
                studyGroupInstance: Study_group | None = None

                if applicantInstance != None:
                    if applicantData.departmentId != None:
                        departmentInstance = applicantInstance.department

                        if departmentInstance and departmentInstance.id != applicantData.departmentId: del applicantData.departmentId
                    if applicantData.facultyId != None: 
                        facultyInstance = applicantInstance.faculty

                        if facultyInstance and facultyInstance.id != applicantData.facultyId: del applicantInstance.faculty
                    
                    if applicantData.studyGroupId != None: 
                        studyGroupInstance = applicantInstance.study_group

                        if studyGroupInstance and studyGroupInstance.id != applicantData.studyGroupId: del applicantInstance.study_group
                    
                    applicantDataSortedList.append(applicantInstance)
        
        return applicantDataSortedList
    


    ####################################################################################################################