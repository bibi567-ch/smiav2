import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MapaLeafletComponent } from './mapa-leaflet.component';

describe('MapaLeafletComponent', () => {
  let component: MapaLeafletComponent;
  let fixture: ComponentFixture<MapaLeafletComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MapaLeafletComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MapaLeafletComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
