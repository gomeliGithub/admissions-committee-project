import { Routes } from '@angular/router';

import { MainComponent } from './components/main/main.component';

import { SignGuard } from './guards/sign/sign.guard';

import { SignComponent } from './components/sign/sign.component';
import { ForbiddenComponent } from './components/forbidden/forbidden.component';

export const routes: Routes = [
    { path: '', redirectTo: '/main', pathMatch: 'full' },
    { path: 'main', component: MainComponent, canActivate: [SignGuard] },
    { path: 'sign/in', component: SignComponent },
    { path: 'forbidden', component: ForbiddenComponent }
];