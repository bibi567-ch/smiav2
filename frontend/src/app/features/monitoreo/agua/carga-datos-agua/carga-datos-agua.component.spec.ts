import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CargaDatosAguaComponent } from './carga-datos-agua.component';

describe('CargaDatosAguaComponent', () => {
  let component: CargaDatosAguaComponent;
  let fixture: ComponentFixture<CargaDatosAguaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CargaDatosAguaComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CargaDatosAguaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
