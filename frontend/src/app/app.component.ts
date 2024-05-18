import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterOutlet } from '@angular/router';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppService } from './app.service';
import { SignService } from './services/sign/sign.service';

import { IActiveClientData, IAlert } from 'types/global';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [ CommonModule, RouterOutlet, RouterLink, NgbModule ],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
    public isMenuCollapsed = true;

    public activeClientData: IActiveClientData | null;

    public alerts: IAlert[] = [];

    constructor (
        private readonly _appService: AppService,
        private readonly _signService: SignService
    ) {
        this._appService.alertsAddChange.subscribe(value => this.addAlert(value));
        this._appService.alertsCloseChange.subscribe(value => this.closeAlert(value));
    }

    ngOnInit (): void {
        this._signService.getActiveClient().subscribe({
            next: clientData => {
                this.activeClientData = clientData;

                this._appService.activeClientData = clientData;
            },
            error: () => this._appService.createAndAddErrorAlert()
        });
    }

    public addAlert (alert: IAlert): void {
        this.alerts.push(alert);

        setTimeout(() => this.closeAlert(alert), alert.closeTimeout);
    }

    public closeAlert (alert: IAlert): void {
		this.alerts.splice(this.alerts.indexOf(alert), 1);
	}

    public signOut (): void {
        this._signService.signOut().subscribe({
            next: () => this._appService.reloadComponent(false, '/'),
            error: () => this._appService.createAndAddErrorAlert()
        });
    }
}