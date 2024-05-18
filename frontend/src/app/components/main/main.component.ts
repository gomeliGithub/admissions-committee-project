import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { Observable } from 'rxjs';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppService } from '../../app.service';
import { MainService } from '../../services/main/main.service';

import { IActiveClientData } from 'types/global';
import { IApplicant } from 'types/models';

@Component({
    selector: 'app-main',
    standalone: true,
    imports: [ CommonModule, NgbModule ],
    templateUrl: './main.component.html',
    styleUrl: './main.component.css'
})
export class MainComponent {
    public activeClientData: IActiveClientData | null;
    
    public applicantList: Observable<IApplicant[]>;

    constructor (
        private readonly _appService: AppService,
        private readonly _mainService: MainService
    ) {
        this.activeClientData = this._appService.activeClientData;

        this.applicantList = this.getApplicantList();
    }

    public getApplicantList (): Observable<IApplicant[]> {
        return this._mainService.getApplicantList();
    }
}