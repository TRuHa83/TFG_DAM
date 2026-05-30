from PySide6.QtCore    import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Quitar barra de título y bordes
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        # Opcional: Hacer el fondo translúcido si usas QSS (hojas de estilo)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.task = QLabel()
        self.task.setAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignBottom)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        layout.addWidget(self.task)
        layout.addWidget(self.progress)

        self.setLayout(layout)

        # Ajustar tamaño y centrar
        self.setFixedSize(300, 70)
        self.center_on_screen()

    def center_on_screen(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())