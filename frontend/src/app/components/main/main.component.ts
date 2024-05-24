import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormArray, FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { Observable } from 'rxjs';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { PipesModule } from '../../modules/pipes/pipes.module';

import { AppService } from '../../app.service';
import { MainService } from '../../services/main/main.service';

import { IActiveClientData, ICreateRequestApplicantData, IGetRequestApplicantData, IGetRequestExamData, IGetRequestOptionalApplicantData, IUpdateApplicantFormDefaultData, IUpdateRequestApplicantData } from 'types/global';
import { IApplicant, IDepartment, IExam, IFaculty, ISpecialty, IStudyGroup } from 'types/models';

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
    public examDataList: IExam[] = [];
    public specialtyDataList: ISpecialty[] = [];

    public nextApplicantsIsExists: boolean = false;

    public commonPassingScore: number = 0;

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

    public updateExamForm: FormGroup<{
        isConsultation: FormControl<boolean | null>;
        conductingDate: FormControl<string | null>;
        classroom: FormControl<string | null>;
        studyGroup: FormControl<string | null>;
    }>;

    public createApplicantFormAccordionIsCollapsed: boolean = true;

    public updateApplicantFormSubmitBtnIsHidden: boolean = true;
    public updateApplicantFormDefaultData: IUpdateApplicantFormDefaultData[] = [];
    public updateApplicantFormData: IUpdateRequestApplicantData[] = [];

    public currentExamDataIndex: number;
    public updateExamFormSubmitIsHidden: boolean = true;

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

        this.getExamData();

        this.getSpecialtyData();

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
        };

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

        const updateExamControls : {
            isConsultation: FormControl<boolean | null>;
            conductingDate: FormControl<string | null>;
            classroom: FormControl<string | null>;
            studyGroup: FormControl<string | null>;
        } = {
            'isConsultation': new FormControl(null),
            'conductingDate': new FormControl(null),
            'classroom': new FormControl(null),
            'studyGroup': new FormControl(null),
        };

        this.applicantSearchForm = new FormGroup(applicantSearchFormControls);
        this.createApplicantForm = new FormGroup(createApplicantFormControls);
        this.updateApplicantForm = new FormGroup({ 'applicants': updateApplicantFormArray });
        this.updateExamForm = new FormGroup(updateExamControls);
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
                this.nextApplicantsIsExists = data.nextApplicantsIsExists;

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

    public getExamData (examData?: IGetRequestExamData): void {
        this._mainService.getExamData(examData).subscribe({
            next: data => this.examDataList = data,
            error: () => this._appService.createAndAddErrorAlert()
        });
    }

    public inputExamChange (examDataIdStr: string): void {
        const examDataId: number = parseInt(examDataIdStr, 10);

        if ( !isNaN(examDataId) ) {
            const currentExamData: IExam = this.examDataList.find(data => data.id === examDataId) as IExam;

            this.updateExamFormSubmitIsHidden = false;

            this.currentExamDataIndex = examDataId;

            const conductingDate: Date = new Date(currentExamData.conductingDate);

            const conductingDateMonth: number = conductingDate.getMonth();
            const conductingDateMonthDay: number = conductingDate.getDate();

            let conductingDateParsed: string = `${ conductingDate.getFullYear() }-${ conductingDateMonth < 10 ? '0' + conductingDateMonth : conductingDateMonth }-${ conductingDateMonthDay < 10 ? '0' + conductingDateMonthDay : conductingDateMonthDay }`;

            this.updateExamForm.controls.isConsultation.setValue(currentExamData.isConsultation);
            this.updateExamForm.controls.conductingDate.setValue(conductingDateParsed);
            this.updateExamForm.controls.classroom.setValue(currentExamData.classroom);
            this.updateExamForm.controls.studyGroup.setValue(this.studyGroupList.at(currentExamData.study_groupId)?.title as string);
        } else {
            this.updateExamForm.reset();

            this.updateExamFormSubmitIsHidden = true;
        }
    }

    public updateExamFormSubmit (): void {
        const updateExamFormData = this.updateExamForm.value;



        console.log(updateExamFormData);



        /* this._mainService.updateExam({
            id: this.currentExamDataIndex,
            isConsultation: updateExamFormData.isConsultation as boolean,
            conductingDate: updateExamFormData.conductingDate as Date,
            classroom: updateExamFormData.classroom as string,
            studyGroupId: this.studyGroupList.find(studyGroupData => studyGroupData.title === updateExamFormData.studyGroup as string)?.id as number
        }); */
    }

    public getSpecialtyData (): void {
        this._mainService.getSpecialtyData().subscribe({
            next: data => {
                this.specialtyDataList = data.specialtyList;
                this.commonPassingScore = data.commonPassingScore;
            },
            error: () => this._appService.createAndAddErrorAlert()
        });
    }
}