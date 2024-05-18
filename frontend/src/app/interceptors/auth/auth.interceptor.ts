import { HttpInterceptorFn } from '@angular/common/http';

export const AuthInterceptor: HttpInterceptorFn = (req, next) => {
    const authToken: string | null = localStorage.getItem('access_token');

    const authRequest = req.clone({
        setHeaders: {
            Authorization: `Bearer ${ authToken }`
        }
    });
  
    return next(authRequest);
};