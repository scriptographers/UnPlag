import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-profile-changepwd',
  templateUrl: './profile-changepwd.component.html',
  styleUrls: ['./profile-changepwd.component.scss']
})
export class ProfileChangepwdComponent implements OnInit {
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

  ngOnInit() {
    this.form = this.fb.group({
      old_password: ['', Validators.required],
      new_password: ['', Validators.required],
      new_password2: ['', Validators.required]
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

    let user = {
      old_password: this.form.get('old_password').value,
      new_password: this.form.get('new_password').value,
      new_password2: this.form.get('new_password2').value
    };

    if (user.old_password !== '' && user.new_password !== '' && user.new_password2 !== '') {
      return this.server.put('/api/account/upassword/', user).subscribe(
        response => {
          console.log(response);
          this.router.navigateByUrl('/dashboard');
        },
        error => {
          console.log(error);
        }
      )
    }
  }
}
