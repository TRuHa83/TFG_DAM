from PySide6.QtGui     import QPixmap, QFont, QIcon
from PySide6.QtCore    import QSize, Qt

from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel,
    QWidget, QVBoxLayout, QPushButton
)

from . import icon_resolver as resolver
from . import assets_rc


def _set_font(name, size:int=11, bold=False, italic=False) -> QFont:
    font = QFont()
    font.setFamilies([name])
    font.setPointSize(size)
    font.setBold(bold)
    font.setItalic(italic)

    return font

def _add_label(text, font=None,) -> QLabel:
    label = QLabel(str(text))
    label.setFont(font)
    return label

def _set_icon(resolver, app) -> QLabel:
    icon = QLabel()
    icon.setMinimumSize(QSize(60, 60))
    icon.setMaximumSize(QSize(60, 60))
    icon.setStyleSheet(u"padding: 0px;")
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Buscamos el icono usando el resolver
    icon_path = resolver.resolve(app)
    
    if icon_path:
        icon.setPixmap(QPixmap(icon_path))
    else:
        # icon default
        icon.setPixmap(QPixmap(u":/icons/icons/default-app.svg"))

    return icon


def _style_basic():
    return (
        """
        QFrame#container {
            border-radius: 10px;
            border: 1px solid;
            border-color: silver;
        }
        
        QFrame#container:hover {
            border-color: #1C71D8;
            background-color: #E8F1FC
        }

        QLabel#name_app {
            color: #1C71D8;
        }
        """
    )

def _style_conflict():
    return (
        """
        QFrame#container {
            border-radius: 10px;
            border: 1px solid;
            border-color: silver;
        }
        
        QFrame#container:hover {
            border-color: #F54927;
            background-color: #FEEBE7;
        }
        
        QLabel#name_app {
            color: #F54927;
        }
        """
    )


def _style_disable():
    return (
        """
        QFrame#container {
            border-radius: 10px;
            border: 1px solid;
            border-color: silver;
        }

        QFrame#container:hover {
            border-color: #808080;
            background-color: #DBDBDB;
        }

        QLabel#name_app {
            color: #808080;
        }
        """
    )


class CustomItem(QWidget):
    def __init__(self, path_cache, config):
        super().__init__()

        self.layoutCat    = None
        self.layoutApp    = None
        self.layoutIcon   = None
        self.layoutAction = None

        self.app_id, self.config = list(config.items())[0]
        self.name     = self.config.get("name", None)
        self.files    = self.config.get("files", None)
        self.main_cat = self.config.get("main_cat", None)
        self.cat      = self.config.get("cat", None)
        self.cfts     = self.config.get("conflict", False)
        self.disable  = self.config.get("disable", True)

        self.setProperty("app_id", self.app_id)
        self.setProperty("name", self.name)
        self.setProperty("files", self.files)
        self.setProperty("cat", self.cat)
        self.setProperty("conflict", self.cfts)
        self.setProperty("disable", self.disable)

        if not self.disable:
            self.setStyleSheet(_style_disable())

        elif self.cfts:
            self.setStyleSheet(_style_conflict())

        else:
            self.setStyleSheet(_style_basic())

        self.resolver = resolver.Icon(path_cache)

        self.init_ui()

    def init_ui(self):
        # CONTENEDOR PRINCIPAL
        container = QFrame(self)
        container.setObjectName(u"container")
        container.setMinimumSize(QSize(0, 100))
        container.setMaximumSize(QSize(16777215, 100))
        container.setFrameShape(QFrame.Shape.StyledPanel)

        # ELEMENTOS
        self.layout_icon()    # AGREGA EL ICONO
        self.layout_name()    # AGREGA NOMBRE Y FILES
        self.layout_cat()     # AGREGA CATEGORIA
        self.layout_control() # AGREGA EL CONTROL

        # LAYOUT CONTENEDOR PRINCIPAL
        containerLayout = QHBoxLayout(container)
        containerLayout.setSpacing(10)
        containerLayout.setContentsMargins(15, 10, 10, 10)
        containerLayout.addLayout(self.layoutIcon, 0)
        containerLayout.addLayout(self.layoutApp, 0)
        containerLayout.addLayout(self.layoutCat, 0)
        containerLayout.addLayout(self.layoutAction, 0)

        # CREAMOS EL MAIN_LAYOUT
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)


    def layout_icon(self):
        # LAYOUT ICONO
        self.layoutIcon = QVBoxLayout()
        self.layoutIcon.setContentsMargins(15, 0, 15, 0)

        # ICONO DE LA APLICACION
        icon_app = _set_icon(self.resolver, self.name)

        self.layoutIcon.addWidget(icon_app)

    def layout_name(self):
        # LAYOUT APP
        self.layoutApp = QVBoxLayout()
        self.layoutApp.setSpacing(8)

        # TITULO DE LA APLICACIÓN
        font = _set_font(u"Monospace", 14, True)
        name_app = _add_label(self.name, font)
        name_app.setObjectName(u"name_app")

        # DOTFILES DE LA APLICACION
        font = _set_font(u"Adwaita Mono", 11, False, True)
        dotfiles_app = _add_label(self.files, font)

        self.layoutApp.addWidget(name_app, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)
        self.layoutApp.addWidget(dotfiles_app, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

    def layout_cat(self):
        # LAYOUT TIPO
        self.layoutCat = QVBoxLayout()
        self.layoutCat.setSpacing(8)
        self.layoutCat.setContentsMargins(0, -1, 10, -1)

        # LABEL TIPO
        font = _set_font(u"Monospace", 10)
        label_tipo = _add_label("Tipo", font)

        # LABEL CATEGORIA
        font = _set_font(u"Adwaita Mono", 11, True)
        label_cat = _add_label(self.cat, font)

        self.layoutCat.addWidget(label_tipo, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)
        self.layoutCat.addWidget(label_cat, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

    def layout_control(self):
        # LAYOUT ACTION
        self.layoutAction = QHBoxLayout()
        self.layoutAction.setSpacing(8)
        self.layoutAction.setContentsMargins(-1, -1, 12, -1)

        # LINEA
        line = QFrame()
        line.setMinimumSize(QSize(0, 50))
        line.setMaximumSize(QSize(16777215, 50))
        line.setFrameShadow(QFrame.Shadow.Plain)
        line.setLineWidth(1)
        line.setMidLineWidth(0)
        line.setFrameShape(QFrame.Shape.VLine)

        # CONTROL HABILITADOR
        self.toggleButton = QPushButton()
        self.toggleButton.setObjectName(u"toggleButton")
        self.toggleButton.setMinimumSize(QSize(30, 15))
        self.toggleButton.setMaximumSize(QSize(30, 15))
        icon = QIcon()
        icon.addFile(u":/icons/icons/toggle_off.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addFile(u":/icons/icons/toggle_on.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.toggleButton.setIcon(icon)
        self.toggleButton.setIconSize(QSize(24, 24))
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(self.disable)
        self.toggleButton.setFlat(True)

        self.layoutAction.addWidget(line)
        self.layoutAction.addWidget(self.toggleButton)
