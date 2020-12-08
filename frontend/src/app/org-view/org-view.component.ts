import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ServerService } from '../server.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-org-view',
  templateUrl: './org-view.component.html',
  styleUrls: ['./org-view.component.scss']
})
export class OrgViewComponent implements OnInit {

  org: any;
  id: string;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private server: ServerService,
    private snackBar: MatSnackBar,
  ) {
    this.route.paramMap.subscribe(params => {
      this.id = params.get('id');
    });

    this.org = {
      id: 0,
      name: '',
      description: '',
      members: [],
      passcode: '',
      date_created: '',
      history: []
    }
  }

  ngOnInit(): void {
    this.server.get(`/api/organization/get/${this.id}/`).subscribe(
      response => {
        this.org = {
          id: response.id,
          name: response.name,
          description: response.title,
          members: response.members,
          passcode: response.unique_code,
          date_created: response.date_created,
          history: response.pastchecks
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
}
