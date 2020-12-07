import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ServerService } from '../server.service';
import { DataService } from '../data.service';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnInit {

  file: File = null;
  form: FormGroup;
  file_name: string;

  languages: Array<any>;
  orgs: Array<any>

  constructor(
    private fb: FormBuilder,
    private server: ServerService,
    private data: DataService
  ) {
    this.languages = ['txt', 'cpp', 'py'];
    this.orgs = [];
  }

  ngOnInit(): void {
    this.form = this.fb.group({
      file_source: ['', [Validators.required]],
      sample_name: ['', [Validators.required]],
      org_id: ['', [Validators.required]],
      file_type: ['', [Validators.required]]
    });

    this.server.get('/api/account/profile/').subscribe(
      response => {
        console.log(response);
        this.orgs = response.orgs
        console.log(this.orgs.find((org) => {
          return org.org_name == response.username;
        }).org_id);
        this.form.patchValue({
          org_id: this.orgs.find((org) => {
            return org.org_name == response.username;
          }).org_id
        })
        console.log(this.orgs);
      },
      error => {
        console.log(error);
      }
    );

  }

  onFileChange(event) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.form.patchValue({
        file_source: file
      });
      this.file_name = file.name;
      console.log(this.file_name);
    }
  }

  onSubmit() {
    console.log('Submitting');
    if (!this.form.valid) {
      console.log('Form not valid. Please check that fields are correctly filled in');
      return;
    }

    console.log('Form valid');

    this.data.upload(this.form.get('file_source').value, this.form.get('sample_name').value, this.form.get('org_id').value, this.form.get('file_type').value);
  }
}
