import { Component, OnInit } from '@angular/core';
import { ServerService } from '../server.service';
import { User } from '../user';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  user: User;

  constructor(private server: ServerService) { }

  ngOnInit() {
  }
}
