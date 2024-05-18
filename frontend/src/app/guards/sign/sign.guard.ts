import { inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CanActivateFn } from '@angular/router';

import { catchError, map, of } from 'rxjs';

import { AppService } from '../../app.service';

import { environment } from '../../../environments/environment';

export const SignGuard: CanActivateFn = (route, state) => {
    route;
    state;
    
    const http: HttpClient = inject(HttpClient);

    const appService: AppService = inject(AppService);

    const apiURL: string = environment.apiURL;

    return http.get<boolean>(`${ apiURL }/main/checkAccess`, { withCredentials: true }).pipe(catchError(() => of(false)), map(checkAccessResult => {
        if ( checkAccessResult ) return true;
        else {
            appService.reloadComponent(false, '/sign/in', false);
    
            return false;
        }
    }));
};