import { IApplicant, ISpecialty } from 'types/models.d';

export interface IActiveClientData {
    login: string;
    lastSignInDate: Date;
}

export interface IAlert {
	type: 'success' | 'warning' | 'danger';
	message: string;
	closeTimeout: number;
}

export interface IGetRequestApplicantData {
	ids?: number[];
    graduatedInstitutions?: string[];
    enrolled?: boolean;
    facultyId?: number;
    departmentId?: number;
    studyGroupId?: number;
    includeFacultyData?: boolean;
    includeDepartmentData?: boolean;
    includeStudyGroupData?: boolean;
    limitCount: number;
    offsetCount: number;
}

export interface IGetRequestOptionalApplicantData {
    facultyId?: number;
    departmentId?: number;
    studyGroupId?: number;
}

export interface IGetResponseApplicantData {
    applicantList: IApplicant[];
    nextApplicantsIsExists: boolean;
}

export interface ICreateRequestApplicantData {
    fullName: string;
    graduatedInstitutions: string[];
    departmentId: number;
    facultyId: number;
    studyGroupId: number;
    medal?: boolean;
}

export interface IUpdateRequestApplicantData {
    id: number;
    fullName?: string;
    graduatedInstitutions?: string[];
    medal?: boolean;
    enrolled?: boolean;
    facultyId?: number;
    departmentId?: number;
    studyGroupId?: number;
}

export interface IUpdateApplicantFormDefaultData {
    fullName: string;
    graduatedInstitutions: string;
    medal: boolean;
    enrolled: boolean;
    faculty: string;
    department: string;
    studyGroup: string;
}

export interface IGetRequestExamData {
    isConsultation?: boolean;
    studyGroupId?: number;
}

export interface IGetResponseSpecialtyData {
    specialtyList: ISpecialty[];
    commonPassingScore: number;
}

export interface IUpdateRequestExamData {
    id: number;
    isConsultation?: boolean;
    conductingDate?: Date;
    classroom?: string;
    studyGroupId?: number;
}