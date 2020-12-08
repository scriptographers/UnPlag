import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileChangepwdComponent } from './profile-changepwd.component';

describe('ProfileChangepwdComponent', () => {
  let component: ProfileChangepwdComponent;
  let fixture: ComponentFixture<ProfileChangepwdComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProfileChangepwdComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfileChangepwdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
