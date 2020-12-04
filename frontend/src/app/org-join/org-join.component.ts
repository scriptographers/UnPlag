import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';

@Component({
  selector: 'app-org-join',
  templateUrl: './org-join.component.html',
  styleUrls: ['./org-join.component.scss']
})
export class OrgJoinComponent implements OnInit {

  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private server: ServerService,
    private router: Router,
  ) { }

  ngOnInit(): void {
    this.form = this.fb.group({
      passcode: ['', Validators.required],
    });
  }

  onSubmit() {
    console.log('Submitting');
    if (!this.form.valid) {
      console.log('Form not valid. Please check that fields are correctly filled in');
      return;
    }

    console.log('Form valid');

    let data = {
      unique_code: this.form.get('passcode').value,
    };

    return this.server.post('/api/organization/joinorg/', data).subscribe(
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
