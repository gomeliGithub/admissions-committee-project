import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable, map } from 'rxjs';

import { environment } from '../../../environments/environment';

import { IRequestApplicantData, IResponseApplicantData } from 'types/global';
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

    public getApplicantList (applicantData: IRequestApplicantData): Observable<IResponseApplicantData> {
        let params: HttpParams = new HttpParams();

        params = params.append('limitCount', applicantData.limitCount)
        params = params.append('offsetCount', applicantData.offsetCount)

        if ( applicantData.ids ) params = params.append('ids', JSON.stringify(applicantData.ids))
        if ( applicantData.graduatedInstitutions ) params = params.append('graduatedInstitutions', JSON.stringify(applicantData.graduatedInstitutions))
        if ( applicantData.enrolled ) params = params.append('enrolled', applicantData.enrolled)
        if ( applicantData.departmentId ) params = params.append('departmentId', applicantData.departmentId)
        if ( applicantData.facultyId ) params = params.append('facultyId', applicantData.facultyId)
        if ( applicantData.studyGroupId ) params = params.append('studyGroupId', applicantData.studyGroupId)

        return this._http.get<IResponseApplicantData>(`${ this._apiURL }/applicant/getApplicantData`, { withCredentials: true, params }).pipe(map(applicantData => {
            applicantData.applicantList.forEach(item => {
                if ( item.graduatedInstitutions ) {
                    const parsedGraduatedInstitutions: string[] = JSON.parse(item.graduatedInstitutions);

                    item.graduatedInstitutions = parsedGraduatedInstitutions.join(', ');
                }
            });



            console.log(applicantData);



            return applicantData;
        }));
    }

    public getFacultyData (): Observable<IFaculty[]> {
        return this._http.get<IFaculty[]>(`${ this._apiURL }/exam/getFacultyData`, { withCredentials: true });
    }

    public getDepartmentData (): Observable<IDepartment[]> {
        return this._http.get<IDepartment[]>(`${ this._apiURL }/exam/getDepartmentData`, { withCredentials: true });
    }

    public getStudyGroupData (): Observable<IStudyGroup[]> {
        return this._http.get<IStudyGroup[]>(`${ this._apiURL }/exam/getStudyGroupData`, { withCredentials: true });
    }
}