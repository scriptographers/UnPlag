import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { DataService } from '../data.service';

@Component({
  selector: 'app-display',
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.scss']
})
export class DisplayComponent implements OnInit {
  id: string;
  content: Array<any>;
  buffer: any;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private data: DataService
  ) {
    this.content = new Array();
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.id = params.get('id');
    });
    this.data.download(this.id).subscribe(
      response => {
        console.log(response);
        console.log(response.body);
        this.buffer = response.body;
        response.body.text().then(
          (buffer: string) => {
            console.log(buffer);
            console.log(typeof buffer);
            let arr = buffer.split('\n');
            console.log(arr)
            for (var i = 0; i < arr.length - 1; i++) {
              this.content.push(arr[i].split(","));
            }
            console.log(this.content);
            console.log(Array.isArray(this.content));
          }
        )
        console.log(response.headers);
      },
      error => {
        console.log(error);
        this.router.navigateByUrl('/dashboard');
      }
    );
  }

  download() {
    this.data.downloadCSV(this.buffer, "demo.csv");
  }
}
