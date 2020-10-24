import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

const baseUrl = 'http://127.0.0.1:8000';

@Injectable({
  providedIn: 'root'
})
export class ServerService {

  constructor(private http: HttpClient) { }


  request(method: string, route: string, data?: any) {
    if (method === 'GET') {
      return this.get(route, data);
    }

    else if (method === 'POST') {
      return this.post(route, data);
    }

    else if (method === 'PUT') {
      return this.put(route, data);
    }


    return this.http.request(method, baseUrl + route, {
      body: data,
      responseType: 'json',
      observe: 'body',
    });
  }

  get(route: string, data?: any): Observable<any> {
    let params = new HttpParams();
    if (data !== undefined) {
      Object.getOwnPropertyNames(data).forEach(key => {
        params = params.set(key, data[key]);
      });
    }

    return this.http.get(baseUrl + route, {
      responseType: 'json',
      params
    });
    // var obj = JSON.parse(txt);
  }

  post(route: string, data?: any, skip: boolean = false, file: boolean = false): Observable<any> {
    let head = {};
    if (skip) {
      head["skip"] = "true";
    }
    if (file) {
      head["file"] = "true";
    }
    console.log(head);
    return this.http.post(baseUrl + route, data, {headers: head});
  }

  put(route: string, data?: any): Observable<any> {
    return this.http.put(baseUrl + route, data);
  }
}
