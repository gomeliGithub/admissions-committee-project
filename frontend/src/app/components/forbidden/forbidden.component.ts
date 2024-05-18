import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-forbidden',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './forbidden.component.html',
    styleUrl: './forbidden.component.css'
})
export class ForbiddenComponent {
    constructor () { }
}