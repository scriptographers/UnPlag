import { Component, OnInit } from '@angular/core';
import { ServerService } from '../server.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user: any;

  constructor(private server: ServerService) {
    this.user = {
      userid: 0,
      username: '',
      profileid: 0,
      nickname: ''
    }
  }

  ngOnInit(): void {
    this.server.get('/api/account/profile/').subscribe(
      response => {
        console.log(response);
        this.user = {
          userid: response.user,
          username: response.username,
          profileid: response.id,
          nickname: response.nick
        }
        console.log(this.user);
      },
      error => {
        console.log(error);
      }
    );
  }
}
