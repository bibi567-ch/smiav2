import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CargaDatosAireComponent } from './carga-datos-aire.component';

describe('CargaDatosAireComponent', () => {
  let component: CargaDatosAireComponent;
  let fixture: ComponentFixture<CargaDatosAireComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CargaDatosAireComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CargaDatosAireComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
