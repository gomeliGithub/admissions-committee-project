export interface IApplicant {
    id: number;
    fullName: string;
    graduatedInstitutions: string;
    medal: boolean;
    enrolled: boolean;
    study_group: IStudyGroup;
    examination_sheet: IExaminationSheet;
    department: IDepartment;
    faculty: IFaculty;
}

export interface IStudyGroup {
    id: number;
    title: string;
    applicant: IApplicant;
    exams: IExam[];
}

export interface IExaminationSheet {
    id: number;
    applicant: IApplicant;
    studySubjects: IStudySubject[];
}

export interface IDepartment {
    id: number;
    title: string;
    placesNumber: number;
    passingScore: number;
    studentsAreShortage: boolean;
    applicants: IApplicant[];             
    faculty: IFaculty;
    specialty: ISpecialty;
}

export interface IFaculty {
    id: number;
    title: string;
    passingScore: number;
    applicants: IApplicant[]; 
    departments: IDepartment[];                    
    specialty: ISpecialty;
}

export interface IExam {
    id: number;
    isConsultation: boolean;
    conductingDate: Date;
    classroom: string;
    createDate: Date;
    studyGroup: IStudyGroup;
}

export interface IStudySubject {
    id: number;
    title: string;
    score: number;
    examinationSheets: IExaminationSheet[];
}

export interface ISpecialty {
    id: number;
    passingScore: number;
    competition: number;
    faculty: IFaculty;
    department: IDepartment;
}