import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { DataService } from '../data.service';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnInit {
  file: File = null;
  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private data: DataService
  ) { }

  ngOnInit(): void {
    this.form = this.fb.group({
      file_source: ['', [Validators.required]],
      sample_name: ['', [Validators.required]],
      org_id: ['0', [Validators.required]]
    });

  }

  onFileChange(event) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.form.patchValue({
        file_source: file
      });
    }
  }

  onSubmit() {
    console.log('Submitting');
    if (!this.form.valid) {
      console.log('Form not valid. Please check that fields are correctly filled in');
      return;
    }

    console.log('Form valid');

    this.data.upload(this.form.get('file_source').value, this.form.get('sample_name').value, this.form.get('org_id').value);
  }
}
