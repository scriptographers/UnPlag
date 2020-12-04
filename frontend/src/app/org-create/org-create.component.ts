import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';

@Component({
  selector: 'app-org-create',
  templateUrl: './org-create.component.html',
  styleUrls: ['./org-create.component.scss']
})
export class OrgCreateComponent implements OnInit {

  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private server: ServerService,
    private router: Router,
  ) { }

  ngOnInit(): void {
    this.form = this.fb.group({
      name: ['', Validators.required],
      description: [''],
    });
  }

  onSubmit() {
    console.log('Submitting');
    if (!this.form.valid) {
      console.log('Form not valid. Please check that fields are correctly filled in');
      return;
    }

    console.log('Form valid');

    let org = {
      name: this.form.get('name').value,
      title: this.form.get('description').value
    };

    if (org.name !== '') {
      return this.server.post('/api/organization/makeorg/', org).subscribe(
        response => {
          console.log(response);
          this.router.navigateByUrl(`/org/view/${response.id}`);
        },
        error => {
          console.log(error);
        }
      )
    }
  }
}
