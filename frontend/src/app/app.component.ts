import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [ RouterOutlet, RouterLink, NgbModule ],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})
export class AppComponent {
    title = 'frontend';

    public isMenuCollapsed = true;
}