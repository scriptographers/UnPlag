import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { EditPasswordComponent } from './edit-password/edit-password.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ProfileComponent } from './profile/profile.component';
import { EditProfileComponent } from './edit-profile/edit-profile.component';
import { UploadComponent } from './upload/upload.component';
import { DisplayComponent } from './display/display.component';
import { AuthGuard } from './auth.guard';

// Specifies the route-component mapping
const routes: Routes = [
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'changepwd', component: EditPasswordComponent, canActivate: [AuthGuard] },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },
  { path: 'profile/edit', component: EditProfileComponent, canActivate: [AuthGuard] },
  { path: 'upload', component: UploadComponent, canActivate: [AuthGuard] },
  { path: 'display/:id', component: DisplayComponent, canActivate: [AuthGuard] },
  { path: '**', redirectTo: 'dashboard', },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
