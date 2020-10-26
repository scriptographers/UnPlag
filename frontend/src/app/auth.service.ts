import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, EMPTY } from 'rxjs';
import { ServerService } from './server.service';
import { catchError, tap } from "rxjs/operators";

@Injectable()
export class AuthService {
  private loggedIn = new BehaviorSubject<boolean>(false);
  get isLoggedIn() {
    return this.loggedIn.asObservable();
  }

  constructor(private router: Router, private server: ServerService) {
    console.log('Auth Service');
    const access = localStorage.getItem('access');
    if (access) {
      console.log('Logged in from memory');
      this.loggedIn.next(true);
    }
  }

  login(user: { username: string, password: string }, ret: string) {
    if (user.username !== '' && user.password !== '') {
      return this.server.post('/api/token/', user, true).subscribe(
        response => {
          console.log(response);
          localStorage.setItem('access', response.access);
          localStorage.setItem('refresh', response.refresh);
          this.loggedIn.next(true);
          this.router.navigateByUrl(ret);
        },
        error => {
          console.log(error.error.detail);
        }
      );
    }
  }

  register(user: { username: string, password: string, password2: string }) {
    if (user.username !== '' && user.password !== '' && user.password2 !== '') {
      return this.server.post('/api/account/signup/', user, true).subscribe(
        response => {
          console.log(response);
          localStorage.setItem('access', response.access);
          localStorage.setItem('refresh', response.refresh);
          this.loggedIn.next(true);
          this.router.navigateByUrl('/dashboard');
        },
        error => {
          if (error.error.password != null) {
            console.log(error.error.password)
          }
          else if (error.error.username != null) {
            console.log(error.error.username)
          }
        }
      );
    }
  }

  logout() {
    this.loggedIn.next(false);
    localStorage.clear();
    this.router.navigateByUrl('/login');
  }

  refresh() {
    const refresh = localStorage.getItem('refresh');
    return this.server.post('/api/token/refresh/', {
      refresh: refresh
    }, true).pipe(
      tap(response => {
        console.log(response);
        localStorage.setItem('access', response.access);
      }),
      catchError(error => {
        console.log(error.error.detail);
        this.logout();
        return EMPTY;
      })
    )
  };
}
