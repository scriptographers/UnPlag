import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';

@Component({
  selector: 'app-profile-edit',
  templateUrl: './profile-edit.component.html',
  styleUrls: ['./profile-edit.component.scss']
})
export class ProfileEditComponent implements OnInit {
  profile: any;

  constructor(
    private fb: FormBuilder,
    private server: ServerService,
    private router: Router,
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
        console.log(response);
        this.profile = {
          userid: response.user,
          username: response.username,
          profileid: response.id,
          nickname: response.nick
        }
        this.form.setValue({ nickname: this.profile.nickname });
        console.log(this.profile);
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
