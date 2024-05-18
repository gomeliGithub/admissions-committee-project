import { inject } from '@angular/core';
import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

import { AppService } from '../../app.service';

export const ErrorInterceptor: HttpInterceptorFn = (req, next) => {
    const authRequest = req.clone();

    const appService: AppService = inject(AppService);

    return next(authRequest).pipe(
        catchError((err: any) => {
            if ( err instanceof HttpErrorResponse ) {
                // Handle HTTP errors
                if ( err.status === 403 ) {
                    // Specific handling for forbidden errors         
                    console.error('Forbidden request:', err);
                    // You might trigger a re-authentication flow or redirect the user here

                    appService.reloadComponent(false, '/forbidden');
                } else {
                    // Handle other HTTP error codes
                    console.error('HTTP error:', err);
                }
            } else {
                // Handle non-HTTP errors
                console.error('An error occurred:', err);
            }
    
            // Re-throw the error to propagate it further
            return throwError(() => err); 
        })
    );
};