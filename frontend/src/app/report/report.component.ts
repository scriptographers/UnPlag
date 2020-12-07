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

  info: any;

  is_processing: boolean;

  buffer: any;
  content: Array<Array<string>>;
  file_names: Array<string>;
  text: Array<Array<string>>;

  plots: any;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private data: DataService
  ) {
    this.is_processing = true;
    this.content = [];
    this.file_names = [];
    this.text = [];
    this.info = {
      name: '',
      org_name: '',
      org_id: '',
      timestamp: '',
      file_type: '',
      file_count: 0
    }

    this.plots = {
      data1: [],
      data2: [],
      data3: [],
      layout1: {},
      layout2: {},
      layout3: {},
      config: {},
    };
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.id = params.get('id');
    });

    this.data.info(this.id).subscribe(
      response => {
        console.log(response);
        this.info.name = response.name;
        this.info.org_name = response.org_name;
        this.info.org_id = response.org_id;
        this.info.timestamp = response.timestamp;
        this.info.file_type = response.file_type;
        this.info.file_count = response.file_count;

        if (this.info.file_count != 0) {
          this.retrieve();
        }
      },
      error => {
        console.log(error);
        this.router.navigateByUrl('/dashboard');
      }
    );
  }

  retrieve() {
    this.data.download(this.id).subscribe(
      response => {
        this.buffer = response.body;
        this.buffer.text().then(
          (buffer: string) => {
            let arr = buffer.split('\n');
            this.file_names = arr[0].split(",");
            for (var i = 0; i < arr.length - 2; ++i) {
              this.content.push(arr[i].split(","));
            }
            this.info.file_count = this.file_names.length;
            for (var i = 0; i < this.file_names.length; i++) {
              this.text.push([]);
              for (var j = 0; j < this.file_names.length; j++) {
                this.text[i].push(`x: ${this.file_names[i]} <br>y: ${this.file_names[j]} <br>Similarity: ${this.content[i][j]}`);
              }
            }

            this.is_processing = false;

            this.plots.data1 = [{
              x: this.file_names,
              y: this.file_names,
              z: this.content,
              text: this.text,
              hoverinfo: 'text',
              hoverlabel: { bgcolor: '#41454c' },
              type: 'surface'
            }];

            this.plots.layout1 = {
              title: 'Surface Plot',
              autosize: false,
              width: 500,
              height: 500,
              hovermode: 'closest',
              scene: {
                xaxis: { showticklabels: false, zeroline: false, title: '' },
                yaxis: { showticklabels: false, zeroline: false, title: '' },
                zaxis: { showticklabels: false, title: '' },
              }
            };

            this.plots.data2 = [{
              x: this.file_names,
              y: this.file_names,
              z: this.content,
              text: this.text,
              hoverinfo: 'text',
              hoverlabel: { bgcolor: '#41454c' },
              type: 'heatmap'
            }];

            this.plots.layout2 = {
              title: 'Heat Map',
              autosize: false,
              width: 500,
              height: 500,
              hovermode: 'closest',
              xaxis: { showticklabels: false, zeroline: false, visible: false },
              yaxis: { showticklabels: false, zeroline: false, visible: false },
            };

            this.plots.data3 = [{
              x: this.file_names,
              y: this.file_names,
              z: this.content,
              text: this.text,
              hoverinfo: 'text',
              hoverlabel: { bgcolor: '#41454c' },
              type: 'contour'
            }];

            this.plots.layout3 = {
              title: 'Contour Plot',
              autosize: false,
              width: 500,
              height: 500,
              hovermode: 'closest',
              xaxis: { showticklabels: false, zeroline: false, visible: false },
              yaxis: { showticklabels: false, zeroline: false, visible: false },
            };

            this.plots.config = { displaylogo: false };
          }
        )
      },
      error => {
        console.log(error);
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
