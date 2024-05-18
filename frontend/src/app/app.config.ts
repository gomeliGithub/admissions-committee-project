import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { HttpClientModule, provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';

import { AuthInterceptor } from './interceptors/auth/auth.interceptor';
// import { ErrorInterceptor } from './interceptors/error/error.interceptor';

export const appConfig: ApplicationConfig = {
    providers: [
        provideRouter(routes),
        importProvidersFrom(HttpClientModule),
        provideHttpClient(withFetch(), withInterceptors([ AuthInterceptor ])) // ErrorInterceptor
    ]
};