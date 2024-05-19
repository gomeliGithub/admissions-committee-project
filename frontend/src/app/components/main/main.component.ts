import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { Observable } from 'rxjs';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppService } from '../../app.service';
import { MainService } from '../../services/main/main.service';

import { IActiveClientData, IResponseApplicantData } from 'types/global';
import { IApplicant, IDepartment, IFaculty, IStudyGroup } from 'types/models';

@Component({
    selector: 'app-main',
    standalone: true,
    imports: [ CommonModule, ReactiveFormsModule, NgbModule ],
    templateUrl: './main.component.html',
    styleUrl: './main.component.css'
})
export class MainComponent {
    public activeClientData: IActiveClientData | null;
    
    public applicantList: IApplicant[] = [];
    public facultyList: IFaculty[] = [];
    public departmentList: IDepartment[] = [];
    public studyGroupList: IStudyGroup[] = [];

    public applicantSearchForm: FormGroup<{
        faculty: FormControl<string | null>
        department: FormControl<string | null>
        studyGroup: FormControl<string | null>
    }>;

    constructor (
        private readonly _appService: AppService,
        private readonly _mainService: MainService
    ) {
        this.activeClientData = this._appService.activeClientData;

        this.getApplicantList().subscribe({
            next: data => !data.nextApplicantsIsExists ? this.applicantList = data.applicantList : this.applicantList.push(...data.applicantList),
            error: () => this._appService.createAndAddErrorAlert()
        });

        this.getFacultyData().subscribe({
            next: data => this.facultyList = data,
            error: () => this._appService.createAndAddErrorAlert()
        });

        this.getDepartmentData().subscribe({
            next: data => this.departmentList = data,
            error: () => this._appService.createAndAddErrorAlert()
        });

        this.getStudyGroupData().subscribe({
            next: data => this.studyGroupList = data,
            error: () => this._appService.createAndAddErrorAlert()
        });

        const formControls: {
            faculty: FormControl<string | null>,
            department: FormControl<string | null>,
            studyGroup: FormControl<string | null>
        } = {
            'faculty': new FormControl(this.facultyList.length !== 0 ? this.facultyList[0].title : '', Validators.required),
            'department': new FormControl(this.departmentList.length !== 0 ? this.departmentList[0].title : '', Validators.required),
            'studyGroup': new FormControl(this.studyGroupList.length !== 0 ? this.studyGroupList[0].title : '', Validators.required)
        };

        this.applicantSearchForm = new FormGroup(formControls);
    }

    public getApplicantList (): Observable<IResponseApplicantData> {
        return this._mainService.getApplicantList({
            limitCount: 5,
            offsetCount: this.applicantList.length
        });
    }

    public getFacultyData (): Observable<IFaculty[]> {
        return this._mainService.getFacultyData();
    }

    public getDepartmentData (): Observable<IDepartment[]> {
        return this._mainService.getDepartmentData();
    }

    public getStudyGroupData (): Observable<IStudyGroup[]> {
        return this._mainService.getStudyGroupData();
    }

    public applicantSearchFormSubmit (): void {
        const applicantSearchFormValue = this.applicantSearchForm.value;

        console.log(applicantSearchFormValue);
    }
}