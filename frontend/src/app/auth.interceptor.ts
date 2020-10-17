import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { AuthService } from './auth.service';
import { tap } from 'rxjs/operators';


@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private router: Router, private auth: AuthService) {
    console.log('Interceptor constructed')
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    if (request.headers.has("skip")) {
      request = request.clone({
        headers: request.headers.delete('skip')
      });
      return next.handle(request);
    }
    console.log('Interceptor called')
    const access = localStorage.getItem('access');
    if (access) {
      request = request.clone({
        setHeaders: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${access}`
        }
      });
    }

    return next.handle(request).pipe(tap(
      () => { },
      (error: any) => {
        if (error instanceof HttpErrorResponse) {
          if (error.status !== 401) {
            if (error.error.detail === 'Given token not valid for any token type') {
              console.log('Authorization Failed with access token, trying refresh token');
              this.auth.refresh();
            } else {
              this.auth.logout();
            }
            return;
          }
          this.router.navigateByUrl('login');
        }
      }));
  }
}
