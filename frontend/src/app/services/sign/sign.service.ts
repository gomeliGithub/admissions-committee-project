import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable } from 'rxjs';

import { AppService } from '../../app.service';

import { environment } from '../../../environments/environment';

import { IActiveClientData } from 'types/global';

@Injectable({
    providedIn: 'root'
})
export class SignService {
    private readonly _apiURL: string;

    constructor (
        private readonly _http: HttpClient,

        private readonly _appService: AppService
    ) { 
        this._apiURL = environment.apiURL;
    }

    public signIn (signData: Partial<{
        clientLogin: string | null;
        clientPassword: string | null;
    }>): void {
        this._http.post(`${ this._apiURL }/sign/in`, {
            login: signData.clientLogin,
            password: signData.clientPassword
        }, { responseType: 'text', withCredentials: true }).subscribe({
            next: access_token => {
                localStorage.setItem('access_token', access_token);

                this._appService.reloadComponent(false, '');
            },
            error: () => this._appService.createAndAddErrorAlert()
        });
    }

    public signOut (): Observable<void> {
        return this._http.put<void>(`${ this._apiURL }/sign/out`, { }, { withCredentials: true });
    }

    public getActiveClient (): Observable<IActiveClientData | null> {
        return this._http.get<IActiveClientData | null>(`${ this._apiURL }/sign/getActiveClient`, { withCredentials: true });
    }

    public checkAccessMain (): Observable<boolean> {
        return this._http.get<boolean>(`${ this._apiURL }/main/checkAccess`, { withCredentials: true });
    }
}