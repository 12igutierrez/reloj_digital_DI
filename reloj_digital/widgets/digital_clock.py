from PySide6.QtWidgets import QWidget, QInputDialog, QMessageBox
from PySide6.QtCore import QTimer
from PySide6.QtUiTools import QUiLoader
from pathlib import Path
from datetime import datetime
from enum import IntEnum
from utils.time_utils import seconds_to_hms
from utils.utils import resource_path



# =========================
# MODOS
class ClockMode(IntEnum):
    CLOCK = 0
    TIMER = 1
    STOPWATCH = 2


class DigitalClock(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # UI
        loader = QUiLoader()
        ui_path = resource_path("widgets/digital_clock.ui")
        self.ui = loader.load(ui_path, self)

        if self.ui is None:
            raise RuntimeError(f"No se pudo cargar el UI: {ui_path}")

        self.setLayout(self.ui.layout())

        # Conexiones
        self.ui.btn_mode.clicked.connect(self._next_mode)
        self.ui.btn_format.clicked.connect(self._toggle_format)
        self.ui.btn_alarm.clicked.connect(self._configure_alarm)

        for btn in (
            self.ui.btn_start,
            self.ui.btn_timer_start
        ):
            btn.clicked.connect(self.start)

        for btn in (
            self.ui.btn_pause,
            self.ui.btn_timer_pause
        ):
            btn.clicked.connect(self.pause)

        for btn in (
            self.ui.btn_reset,
            self.ui.btn_timer_reset
        ):
            btn.clicked.connect(self.reset)

        self.ui.spin_timer_minutes.valueChanged.connect(self._update_timer_duration)

        # Estado
        self._mode = ClockMode.STOPWATCH
        self._running = False
        self._seconds = 0
        self._target_seconds = 0
        self._format_24h = True

        # Alarma
        self._alarm_enabled = False
        self._alarm_time = (0, 0, 0)
        self._alarm_message = ""
        self._alarm_triggered = False

        # Timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_time)
        self._timer.start(1000)

        self._apply_style()
        self._update_panels()
        self._update_mode_label()
        self._set_display_time()


    # =========================
    # TIEMPO
    def _update_time(self):

        if self._mode == ClockMode.CLOCK:
            now = datetime.now()
            fmt = "%H:%M:%S" if self._format_24h else "%I:%M:%S %p"
            text = now.strftime(fmt)
            self.ui.lbl_time.setText(text)

            if self._alarm_enabled and not self._alarm_triggered:
                if (now.hour, now.minute, now.second) == self._alarm_time:
                    self._alarm_triggered = True
                    self._show_alarm_popup()
            return

        if not self._running:
            return

        if self._mode == ClockMode.STOPWATCH:
            self._seconds += 1

        elif self._mode == ClockMode.TIMER:
            self._seconds -= 1
            if self._seconds <= 0:
                self._running = False
                self._seconds = 0

        self._set_display_time()

    def _set_display_time(self):
        self.ui.lbl_time.setText(seconds_to_hms(self._seconds))


    # =========================
    # CONTROLES
    def start(self):
        if self._mode == ClockMode.TIMER and self._seconds <= 0:
            self._seconds = self._target_seconds
        self._running = True

    def pause(self):
        self._running = False

    def reset(self):
        self._running = False
        self._seconds = self._target_seconds if self._mode == ClockMode.TIMER else 0
        self._set_display_time()


    # =========================
    # UI
    def _next_mode(self):
        modes = list(ClockMode)
        self._mode = modes[(modes.index(self._mode) + 1) % len(modes)]
        self._running = False

        if self._mode == ClockMode.TIMER:
            self._target_seconds = self.ui.spin_timer_minutes.value() * 60
            self._seconds = self._target_seconds
        else:
            self._seconds = 0

        self._update_panels()
        self._update_mode_label()
        self._set_display_time()

    def _update_panels(self):
        self.ui.panel_clock.setVisible(self._mode == ClockMode.CLOCK)
        self.ui.panel_stopwatch.setVisible(self._mode == ClockMode.STOPWATCH)
        self.ui.panel_timer.setVisible(self._mode == ClockMode.TIMER)

    def _update_mode_label(self):
        self.ui.lbl_mode.setText({
            ClockMode.CLOCK: "Reloj",
            ClockMode.STOPWATCH: "Cronómetro",
            ClockMode.TIMER: "Temporizador"
        }[self._mode])

    def _toggle_format(self):
        self._format_24h = not self._format_24h

    def _update_timer_duration(self, minutes):
        self._target_seconds = minutes * 60
        if self._mode == ClockMode.TIMER and not self._running:
            self._seconds = self._target_seconds
            self._set_display_time()


    # =========================
    # ALARMA
    def _configure_alarm(self):
        text, ok = QInputDialog.getText(
            self,
            "Configurar alarma",
            "Introduce (HH:MM:SS) y el mensaje\nEjemplo: 08:30:00 Despertar"
        )

        if not ok or not text.strip():
            return

        try:
            time_part, *msg = text.split()
            h, m, s = map(int, time_part.split(":"))
            if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Formato inválido")
            return

        self._alarm_time = (h, m, s)
        self._alarm_message = " ".join(msg) or "¡Alarma!"
        self._alarm_enabled = True
        self._alarm_triggered = False

    def _show_alarm_popup(self):
        QMessageBox.information(self, "Alarma", self._alarm_message)


    # =========================
    # ESTILO
    def _apply_style(self):
        qss_path = resource_path("resources/qss/clock.qss")
        if qss_path and Path(qss_path).exists():
            self.setStyleSheet(Path(qss_path).read_text(encoding="utf-8"))
