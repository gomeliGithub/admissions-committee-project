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
    departmentId?: number;
    facultyId?: number;
    studyGroupId?: number;
    limitCount: number;
    offsetCount: number;
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