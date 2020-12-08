import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-profile-view',
  templateUrl: './profile-view.component.html',
  styleUrls: ['./profile-view.component.scss']
})
export class ProfileViewComponent implements OnInit {

  profile: any;

  constructor(
    private router: Router,
    private server: ServerService,
    private snackBar: MatSnackBar,
  ) {
    this.profile = {
      userid: 0,
      username: '',
      profileid: 0,
      nickname: '',
      orgs: []
    }
  }

  ngOnInit(): void {
    this.server.get('/api/account/profile/').subscribe(
      response => {
        this.profile = {
          userid: response.user,
          username: response.username,
          profileid: response.id,
          nickname: response.nick,
          orgs: response.orgs
        }
        this.profile.orgs.forEach(org => {
          if (org.org_name == this.profile.username) {
            org.is_personal = true;
          }
        });
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
}
