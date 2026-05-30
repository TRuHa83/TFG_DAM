from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QFrame, QSizePolicy, QPushButton
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, Signal, QSize

from . import assets_rc


class CustomModel(QWidget):
    # Señal que emitiremos cuando el usuario cambie el switch
    # Enviaremos el ID del archivo y su nuevo estado
    toggled = Signal(int, bool)

    def __init__(self, file_id, file_path, file_type, enabled=True, parent=None):
        super().__init__(parent)
        self.file_id = file_id
        self.file_path = file_path
        self.file_type = file_type
        self.is_enabled = enabled

        self._setup_ui()
        self._update_style()

    def _setup_ui(self):
        # Aseguramos que el widget sea visible y tenga un tamaño mínimo razonable
        self.setMinimumHeight(55)
        
        # Contenedor principal (para darle bordes redondeados y fondo)
        self.container = QFrame(self)
        self.container.setObjectName("rowContainer")

        # Layout principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)  # Margen externo
        layout.addWidget(self.container)

        # Importante: para que el widget se vea dentro de un QListView/setIndexWidget
        # a veces es necesario asegurar que el widget se expanda
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Layout interno del contenedor
        inner_layout = QHBoxLayout(self.container)
        inner_layout.setContentsMargins(15, 10, 15, 10)
        inner_layout.setSpacing(10)

        # 1. ID
        self.lbl_id = QLabel(str(self.file_id))
        self.lbl_id.setFixedWidth(25)
        self.lbl_id.setAlignment(Qt.AlignCenter)
        font_mono = QFont("monospace")
        font_mono.setPointSize(10)
        self.lbl_id.setFont(font_mono)

        # 2. Símbolo del árbol
        self.lbl_tree = QLabel("├─")
        self.lbl_tree.setFont(font_mono)

        # 3. Icono
        self.lbl_icon = QLabel()
        icon_name = "folder" if self.file_type == "folder" else "text-x-generic"
        # Carga el icono nativo del sistema Linux
        pixmap = QIcon.fromTheme(icon_name).pixmap(20, 20)
        self.lbl_icon.setPixmap(pixmap)

        # 4. Nombre del archivo (Path)
        self.lbl_name = QLabel(self.file_path)
        font_name = QFont()
        font_name.setPointSize(12)
        self.lbl_name.setFont(font_name)
        self.lbl_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # LINEA
        self.line = QFrame()
        self.line.setMinimumSize(QSize(0, 30))
        self.line.setMaximumSize(QSize(16777215, 30))
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QFrame.Shape.VLine)

        # 6. Button (Toggle)
        self.switch = QPushButton()
        self.switch.setObjectName("switch")
        self.switch.setMinimumSize(QSize(30, 15))
        self.switch.setMaximumSize(QSize(30, 15))
        icon = QIcon()
        icon.addFile(u":/icons/icons/toggle_off.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addFile(u":/icons/icons/toggle_on.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.switch.setIcon(icon)
        self.switch.setIconSize(QSize(24, 24))
        self.switch.setCheckable(True)
        self.switch.setChecked(self.is_enabled)
        self.switch.setFlat(True)
        self.switch.clicked.connect(self._on_switch_toggled)

        # Ensamblar
        inner_layout.addWidget(self.lbl_id)
        inner_layout.addWidget(self.lbl_tree)
        inner_layout.addWidget(self.lbl_icon)
        inner_layout.addWidget(self.lbl_name)
        inner_layout.addStretch()
        inner_layout.addWidget(self.line)
        inner_layout.addWidget(self.switch)

    def _on_switch_toggled(self, checked):
        self.is_enabled = checked
        self._update_style()
        self.toggled.emit(self.file_id, checked)

    def _update_style(self):
        """Actualiza los colores dependiendo de si está encendido o apagado"""
        if self.is_enabled:
            # Estilo Activo (Azul/Claro)
            self.container.setStyleSheet("""
                QFrame#rowContainer {
                    background-color: #ffffff;
                    border: 1px solid #e2e8f0;
                    border-radius: 10px;
                }
                QFrame#rowContainer:hover {
                    background-color: #eff6ff;
                    border: 1px solid #2563eb;
                }
            """)
            self.lbl_id.setStyleSheet("color: #94a3b8;")
            self.lbl_tree.setStyleSheet("color: #cbd5e1;")
            self.lbl_name.setStyleSheet("color: #1e293b;")

        else:
            # Estilo Inactivo (Grisado)
            self.container.setStyleSheet("""
                QFrame#rowContainer {
                    background-color: #f8fafc;
                    border: 1px dashed #cbd5e1;
                    border-radius: 10px;
                }
            """)
            self.lbl_id.setStyleSheet("color: #cbd5e1;")
            self.lbl_tree.setStyleSheet("color: #e2e8f0;")
            self.lbl_name.setStyleSheet("color: #94a3b8;")
