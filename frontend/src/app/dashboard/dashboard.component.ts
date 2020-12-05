import { Component, OnInit } from '@angular/core';
import { ServerService } from '../server.service';

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
    private server: ServerService
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
        console.log(response);
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
        console.log(this.profile);
        this.update_history();
      },
      error => {
        console.log(error);
      }
    );
  }

  update_history(): void {
    this.server.get('/api/account/pastchecks/').subscribe(
      response => {
        console.log(response);
        let pastchecks = response.pastchecks;
        console.log(pastchecks)
        pastchecks.forEach(sample => {
          if (sample.org_name == this.profile.username) {
            this.personal_history.push(sample);
          } else {
            this.orgs_history.get(sample.org_name).push(sample);
          }
        });
        console.log(this.orgs_history);
      },
      error => {
        console.log(error);
      }
    );
  }
}
