import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { ServerService } from './server.service';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private router: Router, private server: ServerService) {
  }

  upload(data: File) {
    const formData: FormData = new FormData();
    formData.append('plagzip', data, data.name);
    console.log(data)
    return this.server.post('/api/plagsample/upload/', formData, false, true).subscribe(
      response => {
        console.log(response);
      },
      error => {
        console.log(error.error);
      }
    );
  }
}
