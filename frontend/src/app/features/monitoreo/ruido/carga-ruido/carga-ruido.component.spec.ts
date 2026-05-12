import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CargaRuidoComponent } from './carga-ruido.component';

describe('CargaRuidoComponent', () => {
  let component: CargaRuidoComponent;
  let fixture: ComponentFixture<CargaRuidoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CargaRuidoComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CargaRuidoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
