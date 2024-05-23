import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormArray, FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { Observable } from 'rxjs';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { PipesModule } from '../../modules/pipes/pipes.module';

import { AppService } from '../../app.service';
import { MainService } from '../../services/main/main.service';

import { IActiveClientData, ICreateRequestApplicantData, IGetRequestApplicantData, IGetRequestOptionalApplicantData, IUpdateApplicantFormDefaultData, IUpdateRequestApplicantData } from 'types/global';
import { IApplicant, IDepartment, IFaculty, IStudyGroup } from 'types/models';

@Component({
    selector: 'app-main',
    standalone: true,
    imports: [ CommonModule, ReactiveFormsModule, NgbModule, PipesModule ],
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
        faculty: FormControl<string | null>;
        department: FormControl<string | null>;
        studyGroup: FormControl<string | null>;
        medal?: FormControl<boolean | null>;
    }>;

    public updateApplicantForm: FormGroup<{
        applicants: FormArray<FormGroup<{
            fields: FormGroup<{
                fullName: FormControl<string | null>;
                graduatedInstitutions: FormControl<string | null>;
                medal: FormControl<boolean | null>;
                enrolled: FormControl<boolean | null>;
                faculty: FormControl<string | null>;
                department: FormControl<string | null>;
                studyGroup: FormControl<string | null>;
            }>
        }>>
    }>;

    public createApplicantFormAccordionIsCollapsed: boolean = true;

    public updateApplicantFormSubmitBtnIsHidden: boolean = true;
    public updateApplicantFormDefaultData: IUpdateApplicantFormDefaultData[] = [];
    public updateApplicantFormData: IUpdateRequestApplicantData[] = [];

    constructor (
        private readonly _appService: AppService,
        private readonly _mainService: MainService
    ) {
        this.activeClientData = this._appService.activeClientData;

        this.getApplicantList();

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
            'faculty': new FormControl(null),
            'department': new FormControl(null),
            'studyGroup': new FormControl(null)
        };

        const createApplicantFormControls: {
            fullName: FormControl<string | null>;
            graduatedInstitutions: FormControl<string | null>;
            faculty: FormControl<string | null>;
            department: FormControl<string | null>;
            studyGroup: FormControl<string | null>;
            medal?: FormControl<boolean | null>;
        } = {
            'fullName': new FormControl(null, Validators.required),
            'graduatedInstitutions': new FormControl(null, Validators.required),
            'faculty': new FormControl(null, Validators.required),
            'department': new FormControl(null, Validators.required),
            'studyGroup': new FormControl(null, Validators.required),
            'medal': new FormControl(null)
        }

        const updateApplicantFormArray: FormArray<FormGroup<{
            fields: FormGroup<{
                fullName: FormControl<string | null>;
                graduatedInstitutions: FormControl<string | null>;
                medal: FormControl<boolean | null>;
                enrolled: FormControl<boolean | null>;
                faculty: FormControl<string | null>;
                department: FormControl<string | null>;
                studyGroup: FormControl<string | null>;
            }>
        }>> = new FormArray([
            new FormGroup({
                'fields': new FormGroup({ 
                    'fullName': ( new FormControl(null) ) as FormControl<string | null>,
                    'graduatedInstitutions': ( new FormControl(null) ) as FormControl<string | null>,
                    'medal': ( new FormControl(null) ) as FormControl<boolean | null>,
                    'enrolled': ( new FormControl(null) ) as FormControl<boolean | null>,
                    'faculty': ( new FormControl(null) ) as FormControl<string | null>,
                    'department': ( new FormControl(null) ) as FormControl<string | null>,
                    'studyGroup': ( new FormControl(null) ) as FormControl<string | null>
                })
            })
        ]);

        this.applicantSearchForm = new FormGroup(applicantSearchFormControls);
        this.createApplicantForm = new FormGroup(createApplicantFormControls);
        this.updateApplicantForm = new FormGroup({ 'applicants': updateApplicantFormArray });
    }

    ngOnInit (): void { 

    }

    public getApplicantList (applicantData?: IGetRequestOptionalApplicantData): void {
        const applicantGetData: IGetRequestApplicantData = {
            limitCount: 5, 
            offsetCount: this.applicantList.length,
            includeFacultyData: true,
            includeDepartmentData: true,
            includeStudyGroupData: true
        };

        if ( applicantData ) {
            applicantGetData.facultyId = applicantData.facultyId;
            applicantGetData.departmentId = applicantData.departmentId;
            applicantGetData.studyGroupId = applicantData.studyGroupId;
        }

        this._mainService.getApplicantList(applicantGetData).subscribe({
            next: data => {
                if ( !data.nextApplicantsIsExists ) {
                    this.applicantList = data.applicantList;

                    this._setUpdateApplicantFormControlsData();
                } else {
                    this.applicantList.push(...data.applicantList);

                    this.applicantList.forEach(data => {
                        this.updateApplicantForm.controls['applicants'].push(new FormGroup({
                            'fields': new FormGroup({
                                'fullName': new FormControl(data['fullName']),
                                'graduatedInstitutions': new FormControl(data['graduatedInstitutions']),
                                'medal': new FormControl(data['medal']),
                                'enrolled': new FormControl(data['enrolled']),
                                'faculty': new FormControl(data['faculty'].title),
                                'department': new FormControl(data['department'].title),
                                'studyGroup': new FormControl(data['study_group'].title)
                            })
                        }));

                        this.updateApplicantFormDefaultData.push({
                            'fullName': data['fullName'],
                            'graduatedInstitutions': data['graduatedInstitutions'],
                            'medal': data['medal'],
                            'enrolled': data['enrolled'],
                            'faculty': data['faculty'].title,
                            'department': data['department'].title,
                            'studyGroup': data['study_group'].title
                        });
                    });
                }
            },
            error: () => this._appService.createAndAddErrorAlert()
        });
    }

    private _setUpdateApplicantFormControlsData () {
        this.applicantList.forEach(( data, index ) => { 
            const group: FormGroup<{
                fullName: FormControl<string | null>;
                graduatedInstitutions: FormControl<string | null>;
                medal: FormControl<boolean | null>;
                enrolled: FormControl<boolean | null>;
                faculty: FormControl<string | null>;
                department: FormControl<string | null>;
                studyGroup: FormControl<string | null>;
            }> = new FormGroup({
                'fullName': new FormControl(data['fullName']),
                'graduatedInstitutions': new FormControl(data['graduatedInstitutions']),
                'medal': new FormControl(data['medal']),
                'enrolled': new FormControl(data['enrolled']),
                'faculty': new FormControl(data['faculty'].title),
                'department': new FormControl(data['department'].title),
                'studyGroup': new FormControl(data['study_group'].title)
            });
            
            index === 0 ? this.updateApplicantForm.controls['applicants'] = new FormArray([
                new FormGroup({ 
                    'fields': group
                })
            ]) : this.updateApplicantForm.controls['applicants'].push(new FormGroup({ 'fields': group }));

            this.updateApplicantFormDefaultData.push({
                'fullName': data['fullName'],
                'graduatedInstitutions': data['graduatedInstitutions'],
                'medal': data['medal'],
                'enrolled': data['enrolled'],
                'faculty': data['faculty'].title,
                'department': data['department'].title,
                'studyGroup': data['study_group'].title
            });
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

        this.applicantList = [];

        this.getApplicantList({
            facultyId: this.facultyList.find(facultyData => facultyData.title === applicantSearchFormValue.faculty as string)?.id as number,
            departmentId: this.departmentList.find(departmentData => departmentData.title === applicantSearchFormValue.department as string)?.id as number,
            studyGroupId: this.studyGroupList.find(studyGroupData => studyGroupData.title === applicantSearchFormValue.studyGroup as string)?.id as number
        });
    }

    public applicantSearchFormReset (): void {
        this.applicantSearchForm.reset();
    }

    public createApplicantFormSubmit (): void {
        const createApplicantFormValue = this.createApplicantForm.value;
        
        const applicantData: ICreateRequestApplicantData = {
            fullName: createApplicantFormValue.fullName as string,
            graduatedInstitutions: createApplicantFormValue.graduatedInstitutions?.split(', ') as string[],
            facultyId: this.facultyList.find(facultyData => facultyData.title === createApplicantFormValue.faculty as string)?.id as number,
            departmentId: this.departmentList.find(departmentData => departmentData.title === createApplicantFormValue.department as string)?.id as number,
            studyGroupId: this.studyGroupList.find(studyGroupData => studyGroupData.title === createApplicantFormValue.studyGroup as string)?.id as number,
            medal: createApplicantFormValue.medal as boolean
        }

        this._mainService.createApplicant(applicantData).subscribe({
            next: () => {
                this.createApplicantForm.reset();
                this.createApplicantFormAccordionIsCollapsed = true;

                this._appService.createAndAddSuccessAlert("Абитуриент успешно зарегистрирован");

                this.getApplicantList();
            },
            error: () => this._appService.createAndAddErrorAlert()
        });
    }

    public updateApplicantFormSubmit (): void {
        this._updateApplicantRecursive(this.updateApplicantFormData, 0);
    }

    private _updateApplicantRecursive (applicantData: IUpdateRequestApplicantData[], index: number): void {
        this._mainService.updateApplicant(applicantData[index]).subscribe({
            next: () => {
                if ( applicantData.length - 1 === index ) {
                    this._appService.createAndAddSuccessAlert("Данные успешно изменены");

                    this.updateApplicantFormSubmitBtnIsHidden = true;

                    return;
                }

                this._updateApplicantRecursive(applicantData, index + 1);
            },
            error: () => this._appService.createAndAddErrorAlert()
        });
    }

    public updateApplicantFormControlChange (applicantId: number, applicantGroup: FormGroup<{
        fields: FormGroup<{
            fullName: FormControl<string | null>;
            graduatedInstitutions: FormControl<string | null>;
            medal: FormControl<boolean | null>;
            enrolled: FormControl<boolean | null>;
            faculty: FormControl<string | null>;
            department: FormControl<string | null>;
            studyGroup: FormControl<string | null>;
        }>
    }>): void {
        const defaultApplicantData: IUpdateApplicantFormDefaultData = this.updateApplicantFormDefaultData.at(applicantId) as IUpdateApplicantFormDefaultData;
        const defaultApplicantDataKeys: string[] = Object.keys(defaultApplicantData);

        const updatedDataIndex: number = this.updateApplicantFormData.findIndex(data => data.id === this.applicantList.at(applicantId)?.id as number); 

        defaultApplicantDataKeys.forEach(key => {
            const currentResult: boolean = defaultApplicantData[key as keyof IUpdateApplicantFormDefaultData] !== applicantGroup.controls.fields.get(key)?.value;

            if ( currentResult ) {
                if ( updatedDataIndex === -1 ) {
                    const updateData: IUpdateRequestApplicantData = {
                        id: this.applicantList.at(applicantId)?.id as number
                    };

                    Object.defineProperty(updateData, key, { value: applicantGroup.controls.fields.get(key)?.value, configurable: true, enumerable: true, writable: true });

                    this.updateApplicantFormData.push(updateData);
                } else Object.defineProperty(this.updateApplicantFormData[updatedDataIndex], key, { value: applicantGroup.controls.fields.get(key)?.value, configurable: true, enumerable: true, writable: true });
            } else {
                if ( updatedDataIndex !== -1 && this.updateApplicantFormData.length !== 0 && this.updateApplicantFormData.at(updatedDataIndex) && Object.keys(this.updateApplicantFormData[updatedDataIndex]).includes(key) ) {
                    const updatedFieldsCount: number = Object.keys(this.updateApplicantFormData[updatedDataIndex]).length;

                    if ( updatedFieldsCount === 2 ) this.updateApplicantFormData.splice(updatedDataIndex, 1);
                    else delete this.updateApplicantFormData[updatedDataIndex][key as keyof IUpdateRequestApplicantData];
                }
            }
        });

        this.updateApplicantFormSubmitBtnIsHidden = this.updateApplicantFormData.length ? false : true;
    }
}