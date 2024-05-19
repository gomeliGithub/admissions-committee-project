export interface IActiveClientData {
    login: string;
    lastSignInDate: Date;
}

export interface IAlert {
	type: 'success' | 'warning' | 'danger';
	message: string;
	closeTimeout: number;
}

export interface IRequestApplicantData {
	ids?: number[];
    graduatedInstitutions?: string[];
    enrolled?: boolean;
    departmentId?: number;
    facultyId?: number;
    studyGroupId?: number;
    limitCount: number;
    offsetCount: number;
}

export interface IResponseApplicantData {
    applicantList: IApplicant[];
    nextApplicantsIsExists: boolean;
}