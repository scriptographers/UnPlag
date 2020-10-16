import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { ServerService } from './server.service';

@Injectable()
export class AuthService {
  private loggedIn = new BehaviorSubject<boolean>(false);
  private access: string;

  get isLoggedIn() {
    return this.loggedIn.asObservable();
  }

  constructor(private router: Router, private server: ServerService) {
    console.log('Auth Service');
    const userData = localStorage.getItem('user');
    if (userData) {
      console.log('Logged in from memory');
      const user = JSON.parse(userData);
      this.access = user.access;
      this.server.setLoggedIn(true, this.access);
      this.loggedIn.next(true);
    }
  }

  login(user: { username: string, password: string }) {
    if (user.username !== '' && user.password !== '') {
      return this.server.request('POST', '/api/token/', {
        username: user.username,
        password: user.password
      }).subscribe(
        response => {
          console.log(response);
          if (response.access !== undefined) {
            this.access = response.token;
            this.server.setLoggedIn(true, this.access);
            this.loggedIn.next(true);
            const userData = {
              access: response.access,
              refresh: response.refresh,
              userid: response.userid,
              username: response.username,
            };
            localStorage.setItem('user', JSON.stringify(userData));
            this.router.navigateByUrl('/profile');
          } else {
            console.log("got a response but undefined token");
          }
        },
        error => {
          console.log(error.error.detail);
        }
      );
    }
  }

  logout() {
    this.server.setLoggedIn(false);
    this.stopRefreshTokenTimer();
    delete this.access;

    this.loggedIn.next(false);
    localStorage.clear();
    this.router.navigate(['/login']);
  }

  private refreshToken() {
    const userData = localStorage.getItem('user');
    if (userData) {
      console.log('Logged in from memory');
      const user = JSON.parse(userData);
      this.access = user.access;
      return this.server.request('POST', 'api/token/refresh', {
        refresh: user.refresh
      }).subscribe(
        response => {
          console.log(response)
          let user = JSON.parse(userData);
          user.access = response.access;
          user.access_exp = response.access_exp;
          localStorage.setItem('user', JSON.stringify(user));
          this.startRefreshTokenTimer();
        },
        error => {
          console.log(error)
        }
      );
    } else {
      console.log('Couldn\'t log from memory');
    }
  }

  // helper methods

  private refreshTokenTimeout;

  private startRefreshTokenTimer() {
    const userData = localStorage.getItem('user');
    if (userData) {
      const user = JSON.parse(userData);

      // set a timeout to refresh the token a minute before it expires
      const expires = new Date(user.access_exp * 1000);
      const timeout = expires.getTime() - Date.now() - (60 * 1000);
      this.refreshTokenTimeout = setTimeout(() => this.refreshToken(), timeout);
    } else {
      console.log('Couldn\'t log from memory');
    }
  }

  private stopRefreshTokenTimer() {
    clearTimeout(this.refreshTokenTimeout);
  }
}
