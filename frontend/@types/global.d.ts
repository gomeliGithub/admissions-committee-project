export interface IActiveClientData {
    login: string;
    lastSignInDate: Date;
}

export interface IAlert {
	type: 'success' | 'warning' | 'danger';
	message: string;
	closeTimeout: number;
}