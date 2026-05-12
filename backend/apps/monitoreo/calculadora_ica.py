# apps/monitoreo/calculadora_ica.py
"""
Calculadora del Índice de Calidad del Aire (ICA).
Metodología EPA (Environmental Protection Agency).
Resultado con 4 decimales de precisión.
Cumple: HU-05.1, HU-05.6, RF-05
"""
from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass
from typing import Optional


@dataclass
class ResultadoICA:
    valor: Decimal
    nivel: str
    contaminante_critico: str
    color: str
    recomendacion: str


# Puntos de corte EPA para cada contaminante
# Formato: (C_low, C_high, ICA_low, ICA_high)
BREAKPOINTS = {
    'pm25': [
        (Decimal('0.0'),    Decimal('12.0'),   0,   50),
        (Decimal('12.1'),   Decimal('35.4'),  51,  100),
        (Decimal('35.5'),   Decimal('55.4'), 101,  150),
        (Decimal('55.5'),   Decimal('150.4'),151,  200),
        (Decimal('150.5'),  Decimal('250.4'),201,  300),
        (Decimal('250.5'),  Decimal('500.4'),301,  500),
    ],
    'pm10': [
        (Decimal('0'),   Decimal('54'),    0,   50),
        (Decimal('55'),  Decimal('154'),  51,  100),
        (Decimal('155'), Decimal('254'), 101,  150),
        (Decimal('255'), Decimal('354'), 151,  200),
        (Decimal('355'), Decimal('424'), 201,  300),
        (Decimal('425'), Decimal('604'), 301,  500),
    ],
    'no2': [
        (Decimal('0'),    Decimal('53'),    0,   50),
        (Decimal('54'),   Decimal('100'),  51,  100),
        (Decimal('101'),  Decimal('360'), 101,  150),
        (Decimal('361'),  Decimal('649'), 151,  200),
        (Decimal('650'),  Decimal('1249'),201,  300),
        (Decimal('1250'), Decimal('2049'),301,  500),
    ],
    'so2': [
        (Decimal('0'),   Decimal('35'),    0,   50),
        (Decimal('36'),  Decimal('75'),   51,  100),
        (Decimal('76'),  Decimal('185'), 101,  150),
        (Decimal('186'), Decimal('304'), 151,  200),
        (Decimal('305'), Decimal('604'), 201,  300),
        (Decimal('605'), Decimal('1004'),301,  500),
    ],
    'co': [
        (Decimal('0.0'),  Decimal('4.4'),   0,   50),
        (Decimal('4.5'),  Decimal('9.4'),  51,  100),
        (Decimal('9.5'),  Decimal('12.4'),101,  150),
        (Decimal('12.5'), Decimal('15.4'),151,  200),
        (Decimal('15.5'), Decimal('30.4'),201,  300),
        (Decimal('30.5'), Decimal('50.4'),301,  500),
    ],
    'o3': [
        (Decimal('0'),   Decimal('54'),    0,   50),
        (Decimal('55'),  Decimal('70'),   51,  100),
        (Decimal('71'),  Decimal('85'),  101,  150),
        (Decimal('86'),  Decimal('105'), 151,  200),
        (Decimal('106'), Decimal('200'), 201,  300),
    ],
}

NIVELES = [
    (50,  'BUENO',    '#00e400', 'La calidad del aire es satisfactoria.'),
    (100, 'MODERADO', '#ffff00', 'Grupos sensibles pueden verse afectados.'),
    (150, 'SENSIBLE', '#ff7e00', 'Grupos sensibles deben reducir actividad al aire libre.'),
    (200, 'DANINO',   '#ff0000', 'Todos pueden experimentar efectos a la salud.'),
    (300, 'MUY_DAN',  '#8f3f97', 'Alerta sanitaria. Evitar actividad al aire libre.'),
    (500, 'PELIGROSO','#7e0023', 'Emergencia sanitaria.'),
]


def _calcular_ica_contaminante(
    concentracion: Decimal,
    contaminante: str
) -> Optional[Decimal]:
    """
    Aplica la fórmula lineal EPA para un contaminante específico.
    ICA = ((ICA_high - ICA_low) / (C_high - C_low)) * (C - C_low) + ICA_low
    """
    breakpoints = BREAKPOINTS.get(contaminante, [])

    for c_low, c_high, ica_low, ica_high in breakpoints:
        if c_low <= concentracion <= c_high:
            ica = (
                (Decimal(ica_high) - Decimal(ica_low)) /
                (c_high - c_low) *
                (concentracion - c_low) +
                Decimal(ica_low)
            )
            return ica.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)

    return None


def calcular_ica(
    pm25: float = None,
    pm10: float = None,
    no2:  float = None,
    so2:  float = None,
    co:   float = None,
    o3:   float = None,
) -> ResultadoICA:
    """
    Calcula el ICA general como el máximo entre todos los contaminantes.
    El contaminante con el ICA más alto determina el nivel final.
    Cumple: HU-05.1 (4 decimales), HU-05.6 (cálculo automático)
    """
    contaminantes = {
        'PM2.5': (pm25, 'pm25'),
        'PM10':  (pm10, 'pm10'),
        'NO₂':   (no2,  'no2'),
        'SO₂':   (so2,  'so2'),
        'CO':    (co,   'co'),
        'O₃':    (o3,   'o3'),
    }

    ica_maximo     = Decimal('0.0000')
    contaminante_critico = 'N/D'

    for nombre, (valor, clave) in contaminantes.items():
        if valor is None:
            continue

        ica = _calcular_ica_contaminante(Decimal(str(valor)), clave)
        if ica and ica > ica_maximo:
            ica_maximo           = ica
            contaminante_critico = nombre

    # Determinar nivel y color
    nivel        = 'PELIGROSO'
    color        = '#7e0023'
    recomendacion = 'Emergencia sanitaria.'

    for limite, nivel_str, color_str, recom in NIVELES:
        if ica_maximo <= limite:
            nivel         = nivel_str
            color         = color_str
            recomendacion = recom
            break

    return ResultadoICA(
        valor                = ica_maximo,
        nivel                = nivel,
        contaminante_critico = contaminante_critico,
        color                = color,
        recomendacion        = recomendacion,
    )


def verificar_cumplimiento_agua(muestra_data: dict) -> tuple[bool, list]:
    """
    Verifica si una muestra de agua cumple los límites de la Ley N°1333.
    Retorna (cumple: bool, parametros_excedidos: list)
    Cumple: HU-05.2
    """
    # Límites Ley N°1333 Bolivia — Clase C (uso recreativo)
    LIMITES_LEY_1333 = {
        'ph':         (6.5, 8.5),    # rango: min, max
        'dbo':        (None, 6.0),   # mg/L máximo
        'dqo':        (None, 40.0),  # mg/L máximo
        'coliformes': (None, 1000.0),# UFC/100ml máximo
        'turbidez':   (None, 100.0), # NTU máximo
    }

    excedidos = []

    for parametro, limites in LIMITES_LEY_1333.items():
        valor = muestra_data.get(parametro)
        if valor is None:
            continue

        valor = float(valor)
        min_val, max_val = limites

        if min_val is not None and valor < min_val:
            excedidos.append({
                'parametro': parametro.upper(),
                'valor': valor,
                'limite': f'mínimo {min_val}',
            })
        elif max_val is not None and valor > max_val:
            excedidos.append({
                'parametro': parametro.upper(),
                'valor': valor,
                'limite': f'máximo {max_val}',
            })

    return len(excedidos) == 0, excedidos