import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { ServerService } from './server.service';
import { saveAs } from 'file-saver';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(
    private router: Router,
    private server: ServerService
  ) { }

  upload(data: File) {
    let formData: FormData = new FormData();
    formData.append('plagzip', data, data.name);
    console.log(formData)
    return this.server.post('/api/plagsample/upload/', formData).subscribe(
      response => {
        console.log(response.id);
        this.router.navigateByUrl('display/' + response.id)
      },
      error => {
        console.log(error.error);
      }
    );
  }

  download(id: string) {
    return this.server.get(`/api/plagsample/download/${id}/`, undefined, true);
  }

  downloadCSV(data: any, name: string) {
    const blobData = new Blob([data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blobData);
    console.log(blobData)
    saveAs(blobData, name);
  }
}
