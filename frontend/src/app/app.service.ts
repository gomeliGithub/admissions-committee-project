import { EventEmitter, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpHeaders } from '@angular/common/http';

import { IActiveClientData, IAlert } from 'types/global';

@Injectable({
    providedIn: 'root'
})
export class AppService {
    constructor (
        private readonly _router: Router
    ) { }

    public alertsAddChange: EventEmitter<IAlert> = new EventEmitter();
    public alertsCloseChange: EventEmitter<IAlert> = new EventEmitter();

    public signInIsCurrentPageChange: EventEmitter<boolean> = new EventEmitter();

    public activeClientData: IActiveClientData | null;

    public createAndAddSuccessAlert (message: string, closeTimeout: number = 3000): void {
        this.addAlert({ type: 'success', message, closeTimeout });
    }

    public createAndAddWarningAlert (message: string, closeTimeout: number = 3000): void {
        this.addAlert({ type: 'warning', message, closeTimeout });
    }

    public createAndAddErrorAlert (message?: string, closeTimeout: number = 3000): void {
        this.addAlert({ type: 'danger', message: message ?? 'Что-то пошло не так. Попробуйте ещё раз', closeTimeout });
    }

    public addAlert (value: IAlert): void {
        this.alertsAddChange.emit(value);
    }

    public closeAlert (value: IAlert): void {
        this.alertsCloseChange.emit(value);
    }

    public setSignInAsCurrentPage (value: boolean): void {
        this.signInIsCurrentPageChange.emit(value);
    }

    public async reloadComponent (self: boolean, urlToNavigateTo?: string, reloadPage = true): Promise<void> {
        const url: string | undefined = self ? this._router.url : urlToNavigateTo;

        return this._router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
            this._router.navigate([ url ]).then(() => {
                if ( reloadPage ) window.location.reload();
            });
        })
    }
}