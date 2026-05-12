import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CargaResiduosComponent } from './carga-residuos.component';

describe('CargaResiduosComponent', () => {
  let component: CargaResiduosComponent;
  let fixture: ComponentFixture<CargaResiduosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CargaResiduosComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CargaResiduosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
