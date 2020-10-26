import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Router } from '@angular/router';
import { Subject, Observable, throwError } from "rxjs";
import { catchError, switchMap, tap } from "rxjs/operators";
import { AuthService } from './auth.service';


@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  private _refreshSubject: Subject<any> = new Subject<any>();

  constructor(private router: Router, private auth: AuthService) {
    console.log('Interceptor constructed')
  }

  private _ifTokenExpired() {
    console.log('Refresh');
    this._refreshSubject.subscribe({
      complete: () => {
        this._refreshSubject = new Subject<any>();
      }
    });
    if (this._refreshSubject.observers.length === 1) {
      // Hit refresh-token API passing the refresh token stored into the request
      // to get new access token and refresh token pair
      this.auth.refresh().subscribe(this._refreshSubject);
    }
    return this._refreshSubject;
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
            return this._ifTokenExpired().pipe(
              switchMap(() => {
                return next.handle(this.addHeader(request));
              })
            );
          } else {
            return throwError(error);
          }
        }
        return caught;
      })
    );
  }

  // updateHeader(req) {
  //   const authToken = this.store.getAccessToken();
  //   req = req.clone({
  //     headers: req.headers.set("Authorization", `Bearer ${authToken}`)
  //   });
  //   return req;
  // }



  addHeader(request: HttpRequest<any>): HttpRequest<any> {
    console.log('Interceptor called')
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

  // intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

  //   return next.handle(this.addHeader(request)).pipe(catchError(
  //     error => {
  //       if (error instanceof HttpErrorResponse) {
  //         if (error.status === 401) {
  //           console.log('Authorization Failed with access token, trying refresh token');
  //           this.auth.refresh();
  //           console.log('Interceptor 401');
  //           return next.handle(this.addHeader(request)).pipe(catchError(
  //             err => {
  //               if (err instanceof HttpErrorResponse) {
  //                 if (err.status === 401) {
  //                   console.log('Authorization Failed again');
  //                   return this.auth.logout();
  //                 }
  //                 else if (err.status === 403) {
  //                   console.log('Access Denied')
  //                   this.router.navigateByUrl('dashboard');
  //                 }
  //                 return throwError(error);
  //               }
  //             }
  //           ));
  //         }
  //         else if (error.status === 403) {
  //           console.log('Access Denied')
  //           this.router.navigateByUrl('dashboard');
  //         }
  //         return;
  //       }
  //     }));
  // }
}
