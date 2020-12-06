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

  upload(data: File, name: string, org_id: string, file_type: string) {
    let formData: FormData = new FormData();
    formData.append('plagzip', data, data.name);
    formData.append('name', name);
    formData.append('org_id', org_id);
    formData.append('file_type', file_type);
    console.log(formData);
    return this.server.post('/api/plagsample/upload/', formData).subscribe(
      response => {
        console.log(response.id);
        this.router.navigateByUrl('report/' + response.id)
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
