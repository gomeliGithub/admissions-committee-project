import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';

import { IRequestApplicantData, IResponseApplicantData } from 'types/global';

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

        return this._http.get<IResponseApplicantData>(`${ this._apiURL }/applicant/getApplicantData`, { withCredentials: true, params });
    }
}