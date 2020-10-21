import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Router } from '@angular/router';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  t: boolean;

  constructor(
    private auth: AuthService,
    private router: Router
  ) {
    console.log('Guard constructed');
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    console.log('Guard checking');
    this.auth.isLoggedIn.subscribe(t => {
      this.t = t;
    });
    console.log(state.url)
    if (this.t) {
      return true;
    } else {
      this.router.navigate(['/login'], {
        queryParams: {
          return: state.url
        }
      }); // Need to use navigate over navigateByUrl, don't replace
      return false;
    }
  }
}
