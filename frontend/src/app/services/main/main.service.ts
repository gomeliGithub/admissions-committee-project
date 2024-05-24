import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable, map } from 'rxjs';

import { environment } from '../../../environments/environment';

import { ICreateRequestApplicantData, IGetRequestApplicantData, IGetRequestExamData, IGetResponseApplicantData, IGetResponseSpecialtyData, IUpdateRequestApplicantData, IUpdateRequestExamData } from 'types/global';
import { IDepartment, IExam, IFaculty, ISpecialty, IStudyGroup } from 'types/models';

@Injectable({
    providedIn: 'root'
})
export class MainService {
    private readonly _apiURL: string;

    constructor (
        private readonly _http: HttpClient
    ) { 
        this._apiURL = environment.apiURL;
    }

    public getApplicantList (applicantData: IGetRequestApplicantData): Observable<IGetResponseApplicantData> {
        let params: HttpParams = new HttpParams();

        params = params.append('limitCount', applicantData.limitCount);
        params = params.append('offsetCount', applicantData.offsetCount);

        if ( applicantData.ids ) params = params.append('ids', JSON.stringify(applicantData.ids))
        if ( applicantData.graduatedInstitutions ) params = params.append('graduatedInstitutions', JSON.stringify(applicantData.graduatedInstitutions))
        if ( applicantData.hasOwnProperty('enrolled') ) params = params.append('enrolled', applicantData.enrolled as boolean)
        if ( applicantData.facultyId ) params = params.append('facultyId', applicantData.facultyId)
        if ( applicantData.departmentId ) params = params.append('departmentId', applicantData.departmentId)
        if ( applicantData.studyGroupId ) params = params.append('studyGroupId', applicantData.studyGroupId)
        if ( applicantData.hasOwnProperty('includeFacultyData') ) params = params.append('includeFacultyData', applicantData.includeFacultyData as boolean)
        if ( applicantData.hasOwnProperty('includeDepartmentData') ) params = params.append('includeDepartmentData', applicantData.includeDepartmentData as boolean)
        if ( applicantData.hasOwnProperty('includeStudyGroupData') ) params = params.append('includeStudyGroupData', applicantData.includeStudyGroupData as boolean)
        
        return this._http.get<IGetResponseApplicantData>(`${ this._apiURL }/applicant/getApplicantData`, { withCredentials: true, params });
    }

    public getFacultyData (): Observable<IFaculty[]> {
        return this._http.get<IFaculty[]>(`${ this._apiURL }/study/getFacultyData`, { withCredentials: true });
    }

    public getDepartmentData (): Observable<IDepartment[]> {
        return this._http.get<IDepartment[]>(`${ this._apiURL }/study/getDepartmentData`, { withCredentials: true });
    }

    public getStudyGroupData (): Observable<IStudyGroup[]> {
        return this._http.get<IStudyGroup[]>(`${ this._apiURL }/study/getStudyGroupData`, { withCredentials: true });
    }

    public createApplicant (applicantData: ICreateRequestApplicantData): Observable<void> {
        return this._http.post<void>(`${ this._apiURL }/applicant/createApplicant`, applicantData, { withCredentials: true });
    }

    public updateApplicant (applicantData: IUpdateRequestApplicantData): Observable<void> {
        return this._http.put<void>(`${ this._apiURL }/applicant/updateApplicant`, applicantData, { withCredentials: true });
    }

    public getExamData (examData?: IGetRequestExamData): Observable<IExam[]> {
        let params: HttpParams = new HttpParams();

        if ( examData && examData.studyGroupId ) params = params.append('studySubjectId', examData.studyGroupId);
        if ( examData && examData.hasOwnProperty('isConsultation') ) params = params.append('isConsultation', examData.isConsultation as boolean);

        return this._http.get<IExam[]>(`${ this._apiURL }/study/getExamData`, { withCredentials: true, params });
    }

    public getSpecialtyData (): Observable<IGetResponseSpecialtyData> {
        return this._http.get<IGetResponseSpecialtyData>(`${ this._apiURL }/study/getSpecialtyData`, { withCredentials: true });
    }

    public updateExam (examData: IUpdateRequestExamData): Observable<void> {
        return this._http.put<void>(`${ this._apiURL }/study/updateExam`, examData, { withCredentials: true });
    }

    public getStudentsAreShortageData (data: IDepartment[]): IDepartment[] {
        const sorted: IDepartment[] = data.filter(data => data.studentsAreShortage);

        return sorted;
    }
}