import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ProfileViewComponent } from './profile-view/profile-view.component';
import { ProfileEditComponent } from './profile-edit/profile-edit.component';
import { ProfileChangepwdComponent } from './profile-changepwd/profile-changepwd.component';
import { OrgCreateComponent } from './org-create/org-create.component';
import { OrgJoinComponent } from './org-join/org-join.component';
import { OrgViewComponent } from './org-view/org-view.component';
import { OrgEditComponent } from './org-edit/org-edit.component';
import { UploadComponent } from './upload/upload.component';
import { ReportComponent } from './report/report.component';

import { AuthGuard } from './auth.guard';

// Specifies the route-component mapping
const routes: Routes = [
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'profile/view', component: ProfileViewComponent, canActivate: [AuthGuard] },
  { path: 'profile/edit', component: ProfileEditComponent, canActivate: [AuthGuard] },
  { path: 'profile/changepwd', component: ProfileChangepwdComponent, canActivate: [AuthGuard] },
  { path: 'org/create', component: OrgCreateComponent, canActivate: [AuthGuard] },
  { path: 'org/join', component: OrgJoinComponent, canActivate: [AuthGuard] },
  { path: 'org/view/:id', component: OrgViewComponent, canActivate: [AuthGuard] },
  { path: 'org/edit/:id', component: OrgEditComponent, canActivate: [AuthGuard] },
  { path: 'upload', component: UploadComponent, canActivate: [AuthGuard] },
  { path: 'report/:id/', component: ReportComponent, canActivate: [AuthGuard] },
  { path: '**', redirectTo: 'dashboard', },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
