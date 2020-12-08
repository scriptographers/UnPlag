import { Component, OnInit } from '@angular/core';
import { ServerService } from '../server.service';
import { AuthService } from '../auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  orgs_history: Map<String, Array<any>>;
  personal_history: Array<any>;
  profile: any;

  constructor(
    private server: ServerService,
    private auth: AuthService,
    private snackBar: MatSnackBar,
  ) {
    this.profile = {
      userid: 0,
      username: '',
      profileid: 0,
      nickname: '',
      orgs: []
    }
    this.personal_history = [];
    this.orgs_history = new Map();
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
        response.orgs.forEach(org => {
          this.orgs_history.set(org.org_name, []);
        });
        this.orgs_history.delete(this.profile.username);
        this.update_history();
      },
      error => {
        this.snackBar.open('Something went wrong! Logging out.', "Try Again", {
          duration: 5000, // 5 sec timeout
        });
        this.auth.logout();
      }
    );
  }

  update_history(): void {
    this.server.get('/api/account/pastchecks/').subscribe(
      response => {
        let pastchecks = response.pastchecks;
        pastchecks.forEach(sample => {
          if (sample.org_name == this.profile.username) {
            this.personal_history.push(sample);
          } else {
            this.orgs_history.get(sample.org_name).push(sample);
          }
        });
      },
      error => {
        this.snackBar.open('Something went wrong! Logging out.', "Try Again", {
          duration: 5000, // 5 sec timeout
        });
        this.auth.logout();
      }
    );
  }
}
