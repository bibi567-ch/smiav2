import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MapaAireComponent } from './mapa-aire.component';

describe('MapaAireComponent', () => {
  let component: MapaAireComponent;
  let fixture: ComponentFixture<MapaAireComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MapaAireComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MapaAireComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
