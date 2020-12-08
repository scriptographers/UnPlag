import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-profile-edit',
  templateUrl: './profile-edit.component.html',
  styleUrls: ['./profile-edit.component.scss']
})
export class ProfileEditComponent implements OnInit {

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
      nickname: ['', Validators.required],
    });

    this.server.get('/api/account/profile/').subscribe(
      response => {
        this.profile = {
          userid: response.user,
          username: response.username,
          profileid: response.id,
          nickname: response.nick
        }
        this.form.setValue({ nickname: this.profile.nickname });
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
      nick: this.form.get('nickname').value,
    };

    if (data.nick !== '') {
      return this.server.put('/api/account/update/', data).subscribe(
        response => {
          this.snackBar.open("Successfully Updated", "Done", {
            duration: 5000, // 5 sec timeout
          });
          this.router.navigateByUrl('/profile/view');
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
          this.router.navigateByUrl('/profile/view');
        }
      )
    }
  }
}
