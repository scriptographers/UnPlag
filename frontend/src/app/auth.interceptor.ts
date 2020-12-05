import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Router } from '@angular/router';
import { Subject, Observable, throwError, EMPTY } from "rxjs";
import { catchError, switchMap } from "rxjs/operators";
import { AuthService } from './auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  private _refreshSubject: Subject<any> = new Subject<any>();

  constructor(
    private router: Router,
    private auth: AuthService) {
    console.log('Interceptor constructed')
  }

  private refresh() {
    console.log('Refresh');
    this._refreshSubject.subscribe({
      complete: () => {
        this._refreshSubject = new Subject<any>();
      }
    });
    if (this._refreshSubject.observers.length === 1) {
      // Hit refresh-token API passing the refresh token stored
      // into the request to get new access token
      this.auth.refresh().subscribe(this._refreshSubject);
    }
    return this._refreshSubject;
  }

  private addHeader(request: HttpRequest<any>): HttpRequest<any> {
    console.log('Header updated')
    const access = localStorage.getItem('access');
    if (access) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${access}`
        }
      });
    }
    return request;
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    if (request.headers.has("skip")) {
      request = request.clone({
        headers: request.headers.delete('skip')
      });
      return next.handle(request);
    }

    return next.handle(this.addHeader(request)).pipe(
      catchError((error, caught) => {
        if (error instanceof HttpErrorResponse) {
          if (error.status === 401) {
            return this.refresh().pipe(
              switchMap(() => {
                return next.handle(this.addHeader(request));
              })
            );
          }
          else {
            return throwError(error);
          }
        }
        return caught;
      })
    );
  }
}
