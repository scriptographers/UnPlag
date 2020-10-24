import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  form: FormGroup;
  ret: string = '';

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router,
    private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.auth.isLoggedIn.subscribe(t => {
      if (t == true) {
        this.router.navigateByUrl('/dashboard');
      }
    });
    this.form = this.fb.group({
      username: [''],
      password: ['', Validators.required]
    });
    // Get the query params
    this.route.queryParams
      .subscribe(params => {
        this.ret = params['return'] || '/dashboard';
      });
  }

  onSubmit() {
    if (this.form.valid) {
      this.auth.login(this.form.value, this.ret);
    } else {
      console.log("form invalid");
    }
  }
}
