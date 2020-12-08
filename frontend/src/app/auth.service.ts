import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, EMPTY } from 'rxjs';
import { ServerService } from './server.service';
import { catchError, tap } from "rxjs/operators";
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable()
export class AuthService {
  private loggedIn = new BehaviorSubject<boolean>(false);

  constructor(
    private router: Router,
    private server: ServerService,
    private snackBar: MatSnackBar,
  ) {
    console.log('Auth Service');
    const access = localStorage.getItem('access');
    if (access) {
      console.log('Logged in from memory');
      this.loggedIn.next(true);
    }
  }

  get isLoggedIn() {
    return this.loggedIn.asObservable();
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
          this.snackBar.open("Successfully Logged in", "Done", {
            duration: 5000, // 5 sec timeout
          });
        },
        error => {
          let error_message = '';
          if (error.error.detail != null) {
            error_message += error.error.detail;
          }
          if (error_message == '') {
            error_message = 'Something went wrong!';
          }
          this.snackBar.open(error_message, "Try Again", {
            duration: 5000, // 5 sec timeout
          });
        }
      );
    }
  }

  register(user: { username: string, password: string, password2: string }) {
    if (user.username !== '' && user.password !== '' && user.password2 !== '') {
      return this.server.post('/api/account/signup/', user, true).subscribe(
        response => {
          localStorage.setItem('access', response.access);
          localStorage.setItem('refresh', response.refresh);
          this.loggedIn.next(true);
          this.router.navigateByUrl('/dashboard');
          this.snackBar.open("Successfully Registered", "Done", {
            duration: 5000, // 5 sec timeout
          });
        },
        error => {
          let error_message = '';
          if (error.error.password != null) {
            error_message += error.error.password;
          }
          if (error.error.username != null) {
            error_message += error.error.username;
          }
          if (error_message == '') {
            error_message = 'Something went wrong!';
          }
          this.snackBar.open(error_message, "Try Again", {
            duration: 5000, // 5 sec timeout
          });
        }
      );
    }
  }

  logout() {
    this.loggedIn.next(false);
    localStorage.clear();
    this.router.navigateByUrl('/login');
    this.snackBar.open(' Successfully Logged out. Come back again!', "Done", {
      duration: 5000, // 5 sec timeout
    });
  }

  refresh() {
    const refresh = localStorage.getItem('refresh');
    return this.server.post('/api/token/refresh/', {
      refresh: refresh
    }, true).pipe(
      tap(response => {
        localStorage.setItem('access', response.access);
      }),
      catchError(error => {
        let error_message = '';
        if (error.error.detail != null) {
          error_message += error.error.detail;
        }
        if (error_message == '') {
          error_message = 'Something went wrong!';
        }
        this.snackBar.open(error_message + ' Logging out.', "Try Again", {
          duration: 5000, // 5 sec timeout
        });
        this.logout();
        return EMPTY;
      })
    )
  };
}
