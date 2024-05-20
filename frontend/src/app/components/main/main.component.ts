import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { Observable } from 'rxjs';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppService } from '../../app.service';
import { MainService } from '../../services/main/main.service';

import { IActiveClientData, ICreateRequestApplicantData, IGetResponseApplicantData } from 'types/global';
import { IApplicant, IDepartment, IFaculty, IStudyGroup } from 'types/models';

@Component({
    selector: 'app-main',
    standalone: true,
    imports: [ CommonModule, ReactiveFormsModule, NgbModule ],
    templateUrl: './main.component.html',
    styleUrl: './main.component.css'
})
export class MainComponent implements OnInit {
    public activeClientData: IActiveClientData | null;
    
    public applicantList: IApplicant[] = [];
    public facultyList: IFaculty[] = [];
    public departmentList: IDepartment[] = [];
    public studyGroupList: IStudyGroup[] = [];

    public applicantSearchForm: FormGroup<{
        faculty: FormControl<string | null>;
        department: FormControl<string | null>;
        studyGroup: FormControl<string | null>;
    }>;

    public createApplicantForm: FormGroup<{
        fullName: FormControl<string | null>;
        graduatedInstitutions: FormControl<string | null>;
        facultyTitle: FormControl<string | null>;
        departmentTitle: FormControl<string | null>;
        studyGroupTitle: FormControl<string | null>;
        medal?: FormControl<boolean | null>;
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

        const applicantSearchFormControls: {
            faculty: FormControl<string | null>;
            department: FormControl<string | null>;
            studyGroup: FormControl<string | null>;
        } = {
            'faculty': new FormControl(null, Validators.required),
            'department': new FormControl(null, Validators.required),
            'studyGroup': new FormControl(null, Validators.required)
        };

        const createApplicantFormControls: {
            fullName: FormControl<string | null>;
            graduatedInstitutions: FormControl<string | null>;
            facultyTitle: FormControl<string | null>;
            departmentTitle: FormControl<string | null>;
            studyGroupTitle: FormControl<string | null>;
            medal?: FormControl<boolean | null>;
        } = {
            'fullName': new FormControl(null, Validators.required),
            'graduatedInstitutions': new FormControl(null, Validators.required),
            'facultyTitle': new FormControl(null, Validators.required),
            'departmentTitle': new FormControl(null, Validators.required),
            'studyGroupTitle': new FormControl(null, Validators.required),
            'medal': new FormControl(null)
        }

        this.applicantSearchForm = new FormGroup(applicantSearchFormControls);
        this.createApplicantForm = new FormGroup(createApplicantFormControls);
    }

    ngOnInit (): void {
        this.applicantSearchForm.controls['faculty'].setValue(this.facultyList.length !== 0 ? this.facultyList[0].title : null);
        this.applicantSearchForm.controls['department'].setValue(this.departmentList.length !== 0 ? this.departmentList[0].title : null);
        this.applicantSearchForm.controls['studyGroup'].setValue(this.studyGroupList.length !== 0 ? this.studyGroupList[0].title : null);
    }

    public getApplicantList (): Observable<IGetResponseApplicantData> {
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

    public createApplicantFormSubmit (): void {
        const createApplicantFormValue = this.createApplicantForm.value;
        
        const applicantData: ICreateRequestApplicantData = {
            fullName: createApplicantFormValue.fullName as string,
            graduatedInstitutions: createApplicantFormValue.graduatedInstitutions as string,
            facultyId: this.facultyList.findIndex(facultyData => facultyData.title === createApplicantFormValue.facultyTitle as string),
            departmentId: this.departmentList.findIndex(departmentData => departmentData.title === createApplicantFormValue.departmentTitle as string),
            studyGroupId: this.studyGroupList.findIndex(studyGroupData => studyGroupData.title === createApplicantFormValue.studyGroupTitle as string),
            medal: createApplicantFormValue.medal as boolean
        }



        console.log(applicantData);


        /*
        this._mainService.createApplicant(applicantData).subscribe({
            next: () => null,
            error: () => this._appService.createAndAddErrorAlert()
        });
        */
    }
}