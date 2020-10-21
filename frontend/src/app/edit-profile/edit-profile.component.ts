import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';

@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.scss']
})
export class EditProfileComponent implements OnInit {
  user: any;

  constructor(
    private fb: FormBuilder,
    private server: ServerService,
    private router: Router,
  ) {
    this.user = {
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
        console.log(response);
        this.user = {
          userid: response.user,
          username: response.username,
          profileid: response.id,
          nickname: response.nick
        }
        this.form.setValue({nickname: this.user.nickname});
        console.log(this.user);
      },
      error => {
        console.log(error);
      }
    );
  }
  form: FormGroup;

  onSubmit() {
    console.log('Submitting');
    if (!this.form.valid) {
      console.log('Form not valid. Please check that fields are correctly filled in');
      return;
    }

    console.log('Form valid');

    let profile = {
      nick: this.form.get('nickname').value,
    };

    if (profile.nick !== '') {
      return this.server.put('/api/account/update/', profile).subscribe(
        response => {
          console.log(response);
          this.router.navigateByUrl('/profile');
        },
        error => {
          console.log(error);
        }
      )
    }
  }
}
