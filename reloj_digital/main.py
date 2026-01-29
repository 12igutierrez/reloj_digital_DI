import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from widgets.digital_clock import DigitalClock, ClockMode

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout(window)

clock = DigitalClock()
clock.mode = ClockMode.STOPWATCH  # PROGRESIVO
clock.showSeconds = True

layout.addWidget(clock)

window.setWindowTitle("Demo Reloj Digital")
window.resize(300, 150)
window.show()

sys.exit(app.exec())