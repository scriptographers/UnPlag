import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { ServerService } from './server.service';

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

  login(user: { username: string, password: string }) {
    if (user.username !== '' && user.password !== '') {
      return this.server.post('/api/token/', {
        username: user.username,
        password: user.password
      }, true).subscribe(
        response => {
          console.log(response);
          localStorage.setItem('access', response.access);
          localStorage.setItem('refresh', response.refresh);
          this.loggedIn.next(true);
          this.router.navigateByUrl('/profile');
        },
        error => {
          console.log(error.error.detail);
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
    }, true).subscribe(
      response => {
        console.log(response);
        localStorage.setItem('access', response.access);
      },
      error => {
        console.log(error.error.detail);
        this.logout();
      }
    );
  }
}
