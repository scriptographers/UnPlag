import { Component, ViewChild, OnInit, ElementRef } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { DataService } from '../data.service';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.scss']
})
export class ReportComponent implements OnInit {

  id: string;
  content: Array<Array<string>>;
  file_names: Array<string>;
  buffer: any;
  text: Array<Array<string>>;

  public data1: any;
  public data2: any;
  public data3: any;
  public layout1: any;
  public layout2: any;
  public layout3: any;

  is_processing: boolean;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private data: DataService
  ) {
    this.is_processing = true;
    this.content = [];
    this.file_names = [];
    this.text = [];
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
              this.file_names.push(`File ${i}`);
            }
            for (var i = 0; i < this.file_names.length; i++) {
              this.text.push([]);
              for (var j = 0; j < this.file_names.length; j++) {
                this.text[i].push(`x: ${this.file_names[i]} <br>y: ${this.file_names[j]} <br>Similarity: ${this.content[i][j]}`);
              }
            }
            console.log(this.content);
            console.log(Array.isArray(this.content));
            console.log(this.file_names);
            console.log(this.text);

            this.is_processing = false;

            this.data1 = [{
              x: this.file_names,
              y: this.file_names,
              z: this.content,
              text: this.text,
              hoverinfo: 'text',
              hoverlabel: { bgcolor: '#41454c' },
              type: 'surface'
            }];

            this.layout1 = {
              title: 'Surface Plot',
              autosize: false,
              width: 500,
              height: 500,
              hovermode: 'closest',
            };

            this.data2 = [{
              x: this.file_names,
              y: this.file_names,
              z: this.content,
              text: this.text,
              hoverinfo: 'text',
              hoverlabel: { bgcolor: '#41454c' },
              type: 'heatmap'
            }];

            this.layout2 = {
              title: 'Heat Map',
              autosize: false,
              width: 500,
              height: 500,
              hovermode: 'closest',
            };

            this.data3 = [{
              x: this.file_names,
              y: this.file_names,
              z: this.content,
              text: this.text,
              hoverinfo: 'text',
              hoverlabel: { bgcolor: '#41454c' },
              type: 'contour'
            }];

            this.layout3 = {
              title: 'Contour Plot',
              autosize: false,
              width: 500,
              height: 500,
              hovermode: 'closest',
            };
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

  // onhover(data) {
  //   console.log(data.points[0].x);
  //   console.log(data.points[0].y);
  // };

  // onunhover(data) {
  //   console.log(data.points[0].x);
  //   console.log(data.points[0].y);
  // };
}
