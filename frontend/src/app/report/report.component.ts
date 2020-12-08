import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { DataService } from '../data.service';
import { MatSnackBar } from '@angular/material/snack-bar';

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
  data_matrix: Array<Array<string>>;
  data_vector: Array<string>;
  file_names: Array<string>;
  text: Array<Array<string>>;

  plots: any;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private data: DataService,
    private snackBar: MatSnackBar,
  ) {
    this.is_processing = true;
    this.data_matrix = [];
    this.data_vector = [];
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
      data4: [],
      layout1: {},
      layout2: {},
      layout3: {},
      layout4: {},
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

  retrieve() {
    this.data.download(this.id).subscribe(
      response => {
        this.buffer = response.body;
        this.buffer.text().then(
          (buffer: string) => {
            let arr = buffer.split('\n');
            this.file_names = arr[0].split(",");
            for (var i = 1; i < arr.length - 1; ++i) {
              this.data_matrix.push(arr[i].split(","));
            }
            this.info.file_count = this.file_names.length;
            for (var i = 0; i < this.file_names.length; ++i) {
              this.text.push([]);
              for (var j = 0; j < this.file_names.length; ++j) {
                this.text[i].push(`x: ${this.file_names[i]} <br>y: ${this.file_names[j]} <br>Similarity: ${this.data_matrix[i][j]}`);
              }
            }
            for (var i = 0; i < this.file_names.length; ++i) {
              for (var j = i + 1; j < this.file_names.length; ++j) {
                this.data_vector.push(this.data_matrix[i][j]);
              }
            }
            this.data_vector.sort();
            console.log(this.data_vector);

            this.is_processing = false;

            this.plots.data1 = [{
              x: this.file_names,
              y: this.file_names,
              z: this.data_matrix,
              text: this.text,
              hoverinfo: 'text',
              hoverlabel: { bgcolor: '#41454c' },
              type: 'surface'
            }];

            this.plots.layout1 = {
              title: 'Surface Plot',
              autosize: false,
              width: 750,
              height: 750,
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
              z: this.data_matrix,
              text: this.text,
              hoverinfo: 'text',
              hoverlabel: { bgcolor: '#41454c' },
              type: 'heatmap'
            }];

            this.plots.layout2 = {
              title: 'Heat Map',
              autosize: false,
              width: 750,
              height: 750,
              hovermode: 'closest',
              xaxis: { showticklabels: false, zeroline: false, visible: false },
              yaxis: { showticklabels: false, zeroline: false, visible: false },
            };

            this.plots.data3 = [{
              x: this.file_names,
              y: this.file_names,
              z: this.data_matrix,
              text: this.text,
              hoverinfo: 'text',
              hoverlabel: { bgcolor: '#41454c' },
              type: 'contour'
            }];

            this.plots.layout3 = {
              title: 'Contour Plot',
              autosize: false,
              width: 750,
              height: 750,
              hovermode: 'closest',
              xaxis: { showticklabels: false, zeroline: false, visible: false },
              yaxis: { showticklabels: false, zeroline: false, visible: false },
            };

            this.plots.data4 = [{
              x: this.data_vector,
              autobinx: false,
              histnorm: "count",
              xbins: {
                size: 0.05,
              },
              type: 'histogram'
            }];

            this.plots.layout4 = {
              title: 'Histogram',
              autosize: false,
              width: 750,
              height: 750,
              hovermode: 'x',
            };

            this.plots.data5 = [{
              y: this.data_vector,
              type: 'box'
            }];

            this.plots.layout5 = {
              title: 'Box Plot',
              autosize: false,
              width: 750,
              height: 750,
              xaxis: { showticklabels: false, zeroline: false, visible: false },
            };

            this.plots.config = { displaylogo: false };
          }
        )
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

  download() {
    this.data.downloadCSV(this.buffer, `${this.info.org_name}-${this.info.name}.csv`);
  }
}
