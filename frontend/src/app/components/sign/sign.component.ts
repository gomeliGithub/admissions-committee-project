import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppService } from '../../app.service';
import { SignService } from '../../services/sign/sign.service';

import { IActiveClientData } from 'types/global';

@Component({
    selector: 'app-sign',
    standalone: true,
    imports: [ CommonModule, ReactiveFormsModule, NgbModule ],
    templateUrl: './sign.component.html',
    styleUrl: './sign.component.css'
})
export class SignComponent {
    public activeClientData: IActiveClientData | null;

    public signInForm: FormGroup<{
        clientLogin: FormControl<string | null>
        clientPassword: FormControl<string | null>
    }>;

    constructor (
        private readonly _appService: AppService,
        private readonly _signService: SignService
    ) {
        this._appService.setSignInAsCurrentPage(true);

        const formControls: {
            clientLogin: FormControl<string | null>
            clientPassword: FormControl<string | null>
        } = {
            'clientLogin': new FormControl('', Validators.required),
            'clientPassword': new FormControl('', Validators.required)
        };

        this.signInForm = new FormGroup(formControls);
    }

    public signInFormSubmit (): void {
        const clientSignData = this.signInForm.value;

        this._signService.signIn(clientSignData);
    }
}