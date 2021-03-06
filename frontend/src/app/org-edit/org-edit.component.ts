import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { ServerService } from '../server.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-org-edit',
  templateUrl: './org-edit.component.html',
  styleUrls: ['./org-edit.component.scss']
})
export class OrgEditComponent implements OnInit {

  org: any;
  id: string;
  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private server: ServerService,
    private snackBar: MatSnackBar,
  ) {
    this.route.paramMap.subscribe(params => {
      this.id = params.get('id');
    });

    this.org = {
      id: 0,
      name: '',
      description: '',
      members: []
    }
  }

  ngOnInit(): void {
    this.form = this.fb.group({
      description: ['', Validators.required],
    });

    this.server.get(`/api/organization/get/${this.id}/`).subscribe(
      response => {
        this.org = {
          id: response.id,
          name: response.name,
          description: response.title,
          members: response.members
        }
        this.form.setValue({ description: this.org.description });
      },
      error => {
        if (error.status === 403) {
          this.snackBar.open("Forbidden", "Try Again", {
            duration: 5000, // 5 sec timeout
          });
        } else {
          this.snackBar.open("Something went wrong!", "Try Again", {
            duration: 5000, // 5 sec timeout
          });
        }
        this.router.navigateByUrl('/dashboard');
      }
    );
  }

  onSubmit() {
    console.log('Submitting');
    if (!this.form.valid) {
      console.log('Form not valid. Please check that fields are correctly filled in');
      return;
    }

    console.log('Form valid');

    let data = {
      title: this.form.get('description').value,
    };

    if (data.title !== '') {
      return this.server.put(`/api/organization/update/${this.id}/`, data).subscribe(
        response => {
          this.snackBar.open("Successfully Updated", "Done", {
            duration: 5000, // 5 sec timeout
          });
          this.router.navigateByUrl(`/org/view/${this.id}`);
        },
        error => {
          let error_message = '';
          if (error.error.detail != null) {
            error_message += error.error.detail;
          }
          if (error_message == '') {
            error_message = 'Something went wrong!';
          }
          this.snackBar.open(error_message, "Try Again", {
            duration: 5000, // 5 sec timeout
          });
          this.router.navigateByUrl(`/org/view/${this.id}`);
        }
      )
    }
  }
}
