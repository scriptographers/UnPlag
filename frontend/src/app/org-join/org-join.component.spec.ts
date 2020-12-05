import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OrgJoinComponent } from './org-join.component';

describe('OrgJoinComponent', () => {
  let component: OrgJoinComponent;
  let fixture: ComponentFixture<OrgJoinComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OrgJoinComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrgJoinComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
