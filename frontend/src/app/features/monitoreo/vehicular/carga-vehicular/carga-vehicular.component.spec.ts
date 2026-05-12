import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CargaVehicularComponent } from './carga-vehicular.component';

describe('CargaVehicularComponent', () => {
  let component: CargaVehicularComponent;
  let fixture: ComponentFixture<CargaVehicularComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CargaVehicularComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CargaVehicularComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
