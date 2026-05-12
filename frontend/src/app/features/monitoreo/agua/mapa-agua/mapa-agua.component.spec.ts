import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MapaAguaComponent } from './mapa-agua.component';

describe('MapaAguaComponent', () => {
  let component: MapaAguaComponent;
  let fixture: ComponentFixture<MapaAguaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MapaAguaComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MapaAguaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
