import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';

import { IApplicant } from 'types/models';

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

    public getApplicantList (): Observable<IApplicant[]> {  
        return this._http.get<IApplicant[]>(`${ this._apiURL }/applicant/getApplicantData`, { withCredentials: true, params: {
            limitCount: 5,
            offsetCount: 0
        }});
    }
}