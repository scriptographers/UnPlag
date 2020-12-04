import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OrgEditComponent } from './org-edit.component';

describe('OrgEditComponent', () => {
  let component: OrgEditComponent;
  let fixture: ComponentFixture<OrgEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OrgEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrgEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
