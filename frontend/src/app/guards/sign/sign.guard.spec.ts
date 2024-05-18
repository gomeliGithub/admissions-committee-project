import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { SignGuard } from './sign.guard';

describe('demoGuard', () => {
    const executeGuard: CanActivateFn = (...guardParameters) => 
    TestBed.runInInjectionContext(() => SignGuard(...guardParameters));

    beforeEach(() => {
        TestBed.configureTestingModule({});
    });

    it('should be created', () => {
        expect(executeGuard).toBeTruthy();
    });
});