import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

import { Observable } from 'rxjs';

import { SignService } from '../../services/sign/sign.service';

export const SignGuard: CanActivateFn = (route, state) => {
    route;
    state;
    
    const signService: SignService = inject(SignService)

    const router: Router = inject(Router)

    return new Observable<boolean>(obs => {
        signService.checkAccessMain().subscribe({
            next: () => obs.next(true),
            error: () => {
                router.navigateByUrl('/sign/in')

                obs.next(false);
            }
        })
    });
};