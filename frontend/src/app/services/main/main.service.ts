import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable, map } from 'rxjs';

import { environment } from '../../../environments/environment';

import { ICreateRequestApplicantData, IGetRequestApplicantData, IGetResponseApplicantData, IUpdateRequestApplicantData } from 'types/global';
import { IDepartment, IFaculty, IStudyGroup } from 'types/models';

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
        if ( applicantData.enrolled ) params = params.append('enrolled', applicantData.enrolled)
        if ( applicantData.facultyId ) params = params.append('facultyId', applicantData.facultyId)
        if ( applicantData.departmentId ) params = params.append('departmentId', applicantData.departmentId)
        if ( applicantData.studyGroupId ) params = params.append('studyGroupId', applicantData.studyGroupId)
        if ( applicantData.includeFacultyData ) params = params.append('includeFacultyData', applicantData.includeFacultyData)
        if ( applicantData.includeDepartmentData ) params = params.append('includeDepartmentData', applicantData.includeDepartmentData)
        if ( applicantData.includeStudyGroupData ) params = params.append('includeStudyGroupData', applicantData.includeStudyGroupData)
        
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
}