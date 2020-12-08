import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-org-join',
  templateUrl: './org-join.component.html',
  styleUrls: ['./org-join.component.scss']
})
export class OrgJoinComponent implements OnInit {

  profile: any;
  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private server: ServerService,
    private snackBar: MatSnackBar,
  ) {
    this.profile = {
      userid: 0,
      username: '',
      profileid: 0,
      nickname: ''
    }
  }

  ngOnInit(): void {
    this.form = this.fb.group({
      passcode: ['', Validators.required],
    });
    this.server.get('/api/account/profile/').subscribe(
      response => {
        this.profile = {
          userid: response.user,
          username: response.username,
          profileid: response.id,
          nickname: response.nick
        }
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
      unique_code: this.form.get('passcode').value,
    };

    return this.server.post('/api/organization/joinorg/', data).subscribe(
      response => {
        this.snackBar.open("Successfully Joined org", "Done", {
          duration: 5000, // 5 sec timeout
        });
        this.router.navigateByUrl(`/org/view/${response.id}`);
      },
      error => {
        if (error.status === 404 || error.status === 403) {
          this.snackBar.open("No org found with given passcode", "Try Again", {
            duration: 5000, // 5 sec timeout
          });
        } else {
          this.snackBar.open("Something went wrong!", "Try Again", {
            duration: 5000, // 5 sec timeout
          });
          this.router.navigateByUrl('/dashboard');
        }
      }
    )
  }
}
