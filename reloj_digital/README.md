# Digital Clock – PySide6

Aplicación de reloj digital desarrollada en **Python + PySide6** que incluye:

- Reloj en tiempo real
- Cronómetro
- Temporizador
- Alarma configurable

---

## Funcionalidades

### Modos disponibles
- **Reloj**
  - Formato 12h / 24h
  - Alarma con mensaje emergente
- **Cronómetro**
  - Iniciar / Pausar / Reiniciar
- **Temporizador**
  - Configurable por minutos
  - Cuenta atrás

---

## Tecnologías usadas

- Python 3
- PySide6 (Qt for Python)
- Qt Designer
- QTimer

---

## Estructura del proyecto
RELOG_DIGITAL/
│
├── docs/
│ └── Tarea4v2.pdf
│
├── utils/
│ └── time_utils.py
│
├── widgets/
│ ├── digital_clock.ui
│ └── digital_clock.py
│
├── resources/
│ └── qss/
│   └── clock.qss
│
├── main.py
└── README.md
