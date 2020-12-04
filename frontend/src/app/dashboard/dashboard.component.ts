import { Component, OnInit } from '@angular/core';
import { ServerService } from '../server.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  history: Array<any>;

  constructor(
    private server: ServerService
  ) {
    this.history = [];
  }

  ngOnInit(): void {
    this.server.get('/api/account/pastchecks/').subscribe(
      response => {
        console.log(response);
        this.history = response.pastchecks;
      },
      error => {
        console.log(error);
      }
    )
  }
}
