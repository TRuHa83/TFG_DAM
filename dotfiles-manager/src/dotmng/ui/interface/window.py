# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QListView, QMainWindow, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStackedWidget,
    QStatusBar, QVBoxLayout, QWidget)
from . import assets_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(803, 618)
        MainWindow.setMinimumSize(QSize(803, 618))
        MainWindow.setStyleSheet(u"/*QMainWindow*/\n"
"QWidget#navBar {\n"
"    background-color: #f8faff;\n"
"    border-right: 1px solid #e2e8f0;\n"
"}\n"
"\n"
"QWidget#navBar > QPushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    padding-left: 4px;\n"
"    color: #94a3b8;\n"
"}\n"
"\n"
"QWidget#navBar > QPushButton:hover {\n"
"    background-color: #eff6ff;\n"
"    border-right: 1px solid #e2e8f0;\n"
"    color: #475569;\n"
"}\n"
"\n"
"QWidget#navBar > QPushButton:checked {\n"
"    background-color: #eff6ff;\n"
"    color: #2563eb;\n"
"    border-left: 4px solid #2563eb;\n"
"    border-right: 1px solid #e2e8f0;\n"
"    padding-left: 0px;\n"
"}\n"
"\n"
"QStackedWidget {\n"
"	background-color: #eff6ff;\n"
"}\n"
"\n"
"QStatusBar {\n"
"	background-color: #f8faff;\n"
"    border-top: 1px solid #e2e8f0;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_22 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.navBar = QWidget(self.centralwidget)
        self.navBar.setObjectName(u"navBar")
        self.navBar.setMinimumSize(QSize(65, 0))
        self.navBar.setMaximumSize(QSize(65, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.navBar)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.nav_0 = QPushButton(self.navBar)
        self.nav_0.setObjectName(u"nav_0")
        self.nav_0.setMinimumSize(QSize(65, 50))
        self.nav_0.setMaximumSize(QSize(65, 50))
        font = QFont()
        font.setPointSize(20)
        font.setHintingPreference(QFont.PreferDefaultHinting)
        self.nav_0.setFont(font)
        self.nav_0.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/assets/icons/dashboard_off.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addFile(u":/assets/icons/dashboard_on.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.nav_0.setIcon(icon)
        self.nav_0.setIconSize(QSize(32, 32))
        self.nav_0.setCheckable(True)
        self.nav_0.setChecked(True)
        self.nav_0.setAutoExclusive(True)
        self.nav_0.setProperty(u"index", 0)

        self.verticalLayout_3.addWidget(self.nav_0)

        self.nav_1 = QPushButton(self.navBar)
        self.nav_1.setObjectName(u"nav_1")
        self.nav_1.setMinimumSize(QSize(65, 50))
        self.nav_1.setMaximumSize(QSize(65, 50))
        font1 = QFont()
        font1.setPointSize(24)
        self.nav_1.setFont(font1)
        icon1 = QIcon()
        icon1.addFile(u":/assets/icons/package_off.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/assets/icons/package_on.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.nav_1.setIcon(icon1)
        self.nav_1.setIconSize(QSize(32, 32))
        self.nav_1.setCheckable(True)
        self.nav_1.setAutoExclusive(True)
        self.nav_1.setProperty(u"index", 1)

        self.verticalLayout_3.addWidget(self.nav_1)

        self.nav_2 = QPushButton(self.navBar)
        self.nav_2.setObjectName(u"nav_2")
        self.nav_2.setMinimumSize(QSize(65, 50))
        self.nav_2.setMaximumSize(QSize(65, 50))
        font2 = QFont()
        font2.setPointSize(22)
        self.nav_2.setFont(font2)
        icon2 = QIcon()
        icon2.addFile(u":/assets/icons/file_on.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addFile(u":/assets/icons/file_off.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.nav_2.setIcon(icon2)
        self.nav_2.setIconSize(QSize(32, 32))
        self.nav_2.setCheckable(True)
        self.nav_2.setAutoExclusive(True)
        self.nav_2.setProperty(u"index", 2)

        self.verticalLayout_3.addWidget(self.nav_2)

        self.spacer = QSpacerItem(65, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.spacer)

        self.nav_3 = QPushButton(self.navBar)
        self.nav_3.setObjectName(u"nav_3")
        self.nav_3.setMinimumSize(QSize(65, 50))
        self.nav_3.setMaximumSize(QSize(65, 50))
        font3 = QFont()
        font3.setPointSize(18)
        self.nav_3.setFont(font3)
        icon3 = QIcon()
        icon3.addFile(u":/assets/icons/gear_off.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addFile(u":/assets/icons/gear_on.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.nav_3.setIcon(icon3)
        self.nav_3.setIconSize(QSize(32, 32))
        self.nav_3.setCheckable(True)
        self.nav_3.setAutoExclusive(True)
        self.nav_3.setProperty(u"index", 3)

        self.verticalLayout_3.addWidget(self.nav_3)

        self.nav_1.raise_()
        self.nav_2.raise_()
        self.nav_0.raise_()
        self.nav_3.raise_()

        self.horizontalLayout_22.addWidget(self.navBar)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.page_0 = QWidget()
        self.page_0.setObjectName(u"page_0")
        font4 = QFont()
        font4.setWeight(QFont.Medium)
        self.page_0.setFont(font4)
        self.page_0.setStyleSheet(u"/* ESTILOS PARA QFRAME */\n"
"QFrame#frame_1 {\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 8px;\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"}\n"
"\n"
"QFrame#frame_2 {\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 8px;\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"}\n"
"\n"
"QFrame#frame_3 {\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 8px;\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"}\n"
"\n"
"QFrame#frame_4 {\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 8px;\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"}\n"
"\n"
"QFrame#frame_5 {\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 8px;\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"}\n"
"\n"
"QFrame#label_hostname {\n"
"	border-bottom: 1px solid #e2e8f0;\n"
"    border-top-right-radius: 8px;\n"
"    border-top-left-radius: 8px;\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"}\n"
"\n"
"QFrame#label_"
                        "server {\n"
"	border-bottom: 1px solid #e2e8f0;\n"
"    border-top-right-radius: 8px;\n"
"    border-top-left-radius: 8px;\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"}\n"
"\n"
"/* ESTILOS PARA BOTON PRINCIPAL */\n"
"QPushButton#main_update {\n"
"    background-color: #2563eb;\n"
"    color: #ffffff;\n"
"    border: 1px solid #1d4ed8;\n"
"	padding-right: 3px;\n"
"	border-radius: 8px;\n"
"}\n"
"\n"
"QPushButton#main_update:hover {\n"
"    background-color: #1d4ed8;\n"
"}\n"
"\n"
"QPushButton#main_update:pressed {\n"
"    background-color: #2563eb;\n"
"}\n"
"\n"
"/* ESTILOS BOTONES BASICOS*/\n"
"QPushButton {\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"	padding-right: 3px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #f8faff;\n"
"    color: #1e293b;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f8faff;\n"
"    border: none;\n"
"	color: #2563eb;\n"
"}\n"
"\n"
"\n"
"")
        self.verticalLayout_23 = QVBoxLayout(self.page_0)
        self.verticalLayout_23.setSpacing(20)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_23.setContentsMargins(12, 12, 12, 12)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label = QLabel(self.page_0)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 25))
        self.label.setMaximumSize(QSize(100, 25))
        font5 = QFont()
        font5.setPointSize(14)
        font5.setWeight(QFont.DemiBold)
        self.label.setFont(font5)

        self.verticalLayout_11.addWidget(self.label, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.label_26 = QLabel(self.page_0)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(240, 20))
        self.label_26.setMaximumSize(QSize(240, 20))
        font6 = QFont()
        font6.setPointSize(10)
        font6.setWeight(QFont.Light)
        self.label_26.setFont(font6)

        self.verticalLayout_11.addWidget(self.label_26, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)


        self.horizontalLayout_10.addLayout(self.verticalLayout_11)

        self.main_update = QPushButton(self.page_0)
        self.main_update.setObjectName(u"main_update")
        self.main_update.setMinimumSize(QSize(120, 30))
        self.main_update.setMaximumSize(QSize(120, 30))
        icon4 = QIcon()
        icon4.addFile(u":/assets/icons/update.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.main_update.setIcon(icon4)

        self.horizontalLayout_10.addWidget(self.main_update)


        self.verticalLayout_23.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(20)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.frame_1 = QFrame(self.page_0)
        self.frame_1.setObjectName(u"frame_1")
        self.frame_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.update_dotfiles = QLabel(self.frame_1)
        self.update_dotfiles.setObjectName(u"update_dotfiles")
        font7 = QFont()
        font7.setPointSize(10)
        font7.setWeight(QFont.DemiBold)
        self.update_dotfiles.setFont(font7)

        self.horizontalLayout_3.addWidget(self.update_dotfiles, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.check_dotfiles = QPushButton(self.frame_1)
        self.check_dotfiles.setObjectName(u"check_dotfiles")
        self.check_dotfiles.setMinimumSize(QSize(18, 18))
        self.check_dotfiles.setMaximumSize(QSize(18, 18))
        icon5 = QIcon()
        icon5.addFile(u":/assets/icons/sync.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.check_dotfiles.setIcon(icon5)
        self.check_dotfiles.setIconSize(QSize(20, 20))
        self.check_dotfiles.setCheckable(True)
        self.check_dotfiles.setFlat(True)

        self.horizontalLayout_3.addWidget(self.check_dotfiles, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.setStretch(0, 1)

        self.verticalLayout_8.addLayout(self.horizontalLayout_3)

        self.count_dotfiles = QLabel(self.frame_1)
        self.count_dotfiles.setObjectName(u"count_dotfiles")
        font8 = QFont()
        font8.setPointSize(20)
        font8.setWeight(QFont.DemiBold)
        self.count_dotfiles.setFont(font8)

        self.verticalLayout_8.addWidget(self.count_dotfiles)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_5 = QLabel(self.frame_1)
        self.label_5.setObjectName(u"label_5")
        font9 = QFont()
        font9.setPointSize(8)
        font9.setWeight(QFont.Light)
        self.label_5.setFont(font9)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.hash_dotfiles = QLabel(self.frame_1)
        self.hash_dotfiles.setObjectName(u"hash_dotfiles")
        self.hash_dotfiles.setFont(font9)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.hash_dotfiles)


        self.verticalLayout_8.addLayout(self.formLayout)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_7 = QLabel(self.frame_1)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font9)

        self.horizontalLayout_29.addWidget(self.label_7, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.time_last_dotfiles = QLabel(self.frame_1)
        self.time_last_dotfiles.setObjectName(u"time_last_dotfiles")
        self.time_last_dotfiles.setFont(font9)

        self.horizontalLayout_29.addWidget(self.time_last_dotfiles, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.led_dotfiles = QLabel(self.frame_1)
        self.led_dotfiles.setObjectName(u"led_dotfiles")
        self.led_dotfiles.setEnabled(True)
        self.led_dotfiles.setPixmap(QPixmap(u":/assets/icons/led_red.svg"))

        self.horizontalLayout_29.addWidget(self.led_dotfiles, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_29.setStretch(1, 1)

        self.verticalLayout_8.addLayout(self.horizontalLayout_29)


        self.horizontalLayout_8.addWidget(self.frame_1)

        self.frame_2 = QFrame(self.page_0)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.update_apps = QLabel(self.frame_2)
        self.update_apps.setObjectName(u"update_apps")
        self.update_apps.setFont(font7)

        self.horizontalLayout_6.addWidget(self.update_apps, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.check_apps = QPushButton(self.frame_2)
        self.check_apps.setObjectName(u"check_apps")
        self.check_apps.setMinimumSize(QSize(18, 18))
        self.check_apps.setMaximumSize(QSize(18, 18))
        font10 = QFont()
        font10.setPointSize(10)
        self.check_apps.setFont(font10)
        self.check_apps.setIcon(icon5)
        self.check_apps.setIconSize(QSize(20, 20))
        self.check_apps.setCheckable(True)
        self.check_apps.setFlat(True)

        self.horizontalLayout_6.addWidget(self.check_apps, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.setStretch(0, 1)

        self.verticalLayout_9.addLayout(self.horizontalLayout_6)

        self.count_files_apps = QLabel(self.frame_2)
        self.count_files_apps.setObjectName(u"count_files_apps")
        self.count_files_apps.setFont(font8)

        self.verticalLayout_9.addWidget(self.count_files_apps)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_16 = QLabel(self.frame_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font9)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_16)

        self.hash_apps = QLabel(self.frame_2)
        self.hash_apps.setObjectName(u"hash_apps")
        self.hash_apps.setFont(font9)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.hash_apps)


        self.verticalLayout_9.addLayout(self.formLayout_3)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_19 = QLabel(self.frame_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font9)

        self.horizontalLayout_28.addWidget(self.label_19, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.time_last_apps = QLabel(self.frame_2)
        self.time_last_apps.setObjectName(u"time_last_apps")
        self.time_last_apps.setFont(font9)

        self.horizontalLayout_28.addWidget(self.time_last_apps, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.led_apps = QLabel(self.frame_2)
        self.led_apps.setObjectName(u"led_apps")
        self.led_apps.setPixmap(QPixmap(u":/assets/icons/led_red.svg"))

        self.horizontalLayout_28.addWidget(self.led_apps)

        self.horizontalLayout_28.setStretch(1, 1)

        self.verticalLayout_9.addLayout(self.horizontalLayout_28)


        self.horizontalLayout_8.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.page_0)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_3)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_20 = QLabel(self.frame_3)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font7)

        self.horizontalLayout_7.addWidget(self.label_20, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.check_unknown = QPushButton(self.frame_3)
        self.check_unknown.setObjectName(u"check_unknown")
        self.check_unknown.setMinimumSize(QSize(18, 18))
        self.check_unknown.setMaximumSize(QSize(18, 18))
        self.check_unknown.setFont(font10)
        self.check_unknown.setStyleSheet(u"")
        self.check_unknown.setIcon(icon5)
        self.check_unknown.setIconSize(QSize(20, 20))
        self.check_unknown.setCheckable(True)
        self.check_unknown.setFlat(True)

        self.horizontalLayout_7.addWidget(self.check_unknown, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_7.setStretch(0, 1)

        self.verticalLayout_10.addLayout(self.horizontalLayout_7)

        self.count_files_unknown = QLabel(self.frame_3)
        self.count_files_unknown.setObjectName(u"count_files_unknown")
        self.count_files_unknown.setFont(font8)

        self.verticalLayout_10.addWidget(self.count_files_unknown)

        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.label_22 = QLabel(self.frame_3)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font9)

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_22)

        self.hash_unknown = QLabel(self.frame_3)
        self.hash_unknown.setObjectName(u"hash_unknown")
        self.hash_unknown.setFont(font9)

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.FieldRole, self.hash_unknown)


        self.verticalLayout_10.addLayout(self.formLayout_5)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_25 = QLabel(self.frame_3)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font9)

        self.horizontalLayout_9.addWidget(self.label_25, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.time_last_unknown = QLabel(self.frame_3)
        self.time_last_unknown.setObjectName(u"time_last_unknown")
        self.time_last_unknown.setFont(font9)

        self.horizontalLayout_9.addWidget(self.time_last_unknown, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.led_unknown = QLabel(self.frame_3)
        self.led_unknown.setObjectName(u"led_unknown")
        self.led_unknown.setPixmap(QPixmap(u":/assets/icons/led_red.svg"))

        self.horizontalLayout_9.addWidget(self.led_unknown)

        self.horizontalLayout_9.setStretch(1, 1)

        self.verticalLayout_10.addLayout(self.horizontalLayout_9)


        self.horizontalLayout_8.addWidget(self.frame_3)


        self.verticalLayout_23.addLayout(self.horizontalLayout_8)

        self.frame_4 = QFrame(self.page_0)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frame_4)
        self.verticalLayout_20.setSpacing(10)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.label_hostname = QFrame(self.frame_4)
        self.label_hostname.setObjectName(u"label_hostname")
        self.label_hostname.setMinimumSize(QSize(712, 43))
        self.label_hostname.setMaximumSize(QSize(16777215, 43))
        self.verticalLayout_21 = QHBoxLayout(self.label_hostname)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.label_28 = QLabel(self.label_hostname)
        self.label_28.setObjectName(u"label_28")
        font11 = QFont()
        font11.setPointSize(14)
        self.label_28.setFont(font11)

        self.verticalLayout_21.addWidget(self.label_28, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.hostname = QLabel(self.label_hostname)
        self.hostname.setObjectName(u"hostname")
        self.hostname.setFont(font5)

        self.verticalLayout_21.addWidget(self.hostname, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_21.setStretch(1, 1)

        self.verticalLayout_20.addWidget(self.label_hostname)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(9, -1, 9, -1)
        self.label_49 = QLabel(self.frame_4)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setMinimumSize(QSize(19, 19))
        self.label_49.setMaximumSize(QSize(19, 19))

        self.horizontalLayout_19.addWidget(self.label_49, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_50 = QLabel(self.frame_4)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFont(font6)

        self.horizontalLayout_19.addWidget(self.label_50, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.os_machine = QLabel(self.frame_4)
        self.os_machine.setObjectName(u"os_machine")
        self.os_machine.setFont(font10)

        self.horizontalLayout_19.addWidget(self.os_machine, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_19.setStretch(1, 1)

        self.verticalLayout_20.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(9, -1, 9, -1)
        self.label_52 = QLabel(self.frame_4)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setMinimumSize(QSize(19, 19))
        self.label_52.setMaximumSize(QSize(19, 19))

        self.horizontalLayout_20.addWidget(self.label_52, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_53 = QLabel(self.frame_4)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setFont(font6)

        self.horizontalLayout_20.addWidget(self.label_53, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.id_machine = QLabel(self.frame_4)
        self.id_machine.setObjectName(u"id_machine")
        self.id_machine.setFont(font10)

        self.horizontalLayout_20.addWidget(self.id_machine, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_20.setStretch(1, 1)

        self.verticalLayout_20.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(9, -1, 9, -1)
        self.label_54 = QLabel(self.frame_4)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setMinimumSize(QSize(19, 19))
        self.label_54.setMaximumSize(QSize(19, 19))

        self.horizontalLayout_21.addWidget(self.label_54, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_55 = QLabel(self.frame_4)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setFont(font6)

        self.horizontalLayout_21.addWidget(self.label_55, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.version_manager = QLabel(self.frame_4)
        self.version_manager.setObjectName(u"version_manager")
        self.version_manager.setFont(font10)

        self.horizontalLayout_21.addWidget(self.version_manager, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_21.setStretch(1, 1)

        self.verticalLayout_20.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(9, -1, 9, 9)
        self.label_56 = QLabel(self.frame_4)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setMinimumSize(QSize(19, 19))

        self.horizontalLayout_23.addWidget(self.label_56, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_57 = QLabel(self.frame_4)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setFont(font6)

        self.horizontalLayout_23.addWidget(self.label_57, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.check_updates = QPushButton(self.frame_4)
        self.check_updates.setObjectName(u"check_updates")
        self.check_updates.setMinimumSize(QSize(18, 18))
        self.check_updates.setMaximumSize(QSize(18, 18))
        self.check_updates.setFont(font10)
        self.check_updates.setIcon(icon5)
        self.check_updates.setIconSize(QSize(20, 20))
        self.check_updates.setCheckable(True)
        self.check_updates.setFlat(True)

        self.horizontalLayout_23.addWidget(self.check_updates, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_23.setStretch(1, 1)

        self.verticalLayout_20.addLayout(self.horizontalLayout_23)


        self.verticalLayout_23.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.page_0)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_5)
        self.verticalLayout_22.setSpacing(6)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.label_server = QFrame(self.frame_5)
        self.label_server.setObjectName(u"label_server")
        self.label_server.setMinimumSize(QSize(712, 43))
        self.label_server.setMaximumSize(QSize(16777215, 43))
        self.horizontalLayout_24 = QHBoxLayout(self.label_server)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_60 = QLabel(self.label_server)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setFont(font11)

        self.horizontalLayout_24.addWidget(self.label_60, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_67 = QLabel(self.label_server)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setFont(font5)

        self.horizontalLayout_24.addWidget(self.label_67, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.server_status = QLabel(self.label_server)
        self.server_status.setObjectName(u"server_status")
        self.server_status.setPixmap(QPixmap(u":/assets/icons/led_red.svg"))

        self.horizontalLayout_24.addWidget(self.server_status)

        self.horizontalLayout_24.setStretch(1, 1)

        self.verticalLayout_22.addWidget(self.label_server)

        self.widgetLayout_30 = QWidget(self.frame_5)
        self.widgetLayout_30.setObjectName(u"widgetLayout_30")
        self.widgetLayout_30.setMinimumSize(QSize(712, 64))
        self.widgetLayout_30.setMaximumSize(QSize(16777215, 64))
        self.horizontalLayout_26 = QHBoxLayout(self.widgetLayout_30)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(4, 0, 4, 0)
        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setSpacing(6)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_63 = QLabel(self.widgetLayout_30)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setMinimumSize(QSize(0, 16))
        self.label_63.setMaximumSize(QSize(16777215, 16))
        self.label_63.setFont(font6)
        self.label_63.setStyleSheet(u"padding-left: 24px")

        self.verticalLayout_24.addWidget(self.label_63, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setSpacing(6)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.label_62 = QLabel(self.widgetLayout_30)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setMinimumSize(QSize(19, 19))
        self.label_62.setMaximumSize(QSize(19, 19))
        self.label_62.setStyleSheet(u"padding: 1px;")

        self.horizontalLayout_25.addWidget(self.label_62, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.endpoint_server = QLineEdit(self.widgetLayout_30)
        self.endpoint_server.setObjectName(u"endpoint_server")
        self.endpoint_server.setEnabled(False)
        self.endpoint_server.setMinimumSize(QSize(350, 26))
        self.endpoint_server.setMaximumSize(QSize(350, 26))
        font12 = QFont()
        font12.setFamilies([u"JetBrains Mono"])
        font12.setPointSize(11)
        font12.setWeight(QFont.Medium)
        self.endpoint_server.setFont(font12)
        self.endpoint_server.setStyleSheet(u"/* Estilo base para todos los LineEdit */\n"
"QLineEdit {\n"
"    background-color: #f8faff;\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 6px;\n"
"    color: #475569;\n"
"    font-family: \"JetBrains Mono\", \"Consolas\", monospace; /* Ideal para URLs/Paths */\n"
"    selection-background-color: #cbd5e1;\n"
"}\n"
"\n"
"/* Estado: Cuando se activa para editar y el usuario hace clic (Focus) */\n"
"QLineEdit:focus {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #2563eb; /* Tu azul principal */\n"
"    color: #1e293b;\n"
"}\n"
"\n"
"/* Opcional: Si lo deshabilitas por completo en lugar de ReadOnly */\n"
"QLineEdit:disabled {\n"
"    background-color: #f1f5f9;\n"
"    color: #ABABAB;\n"
"    border: 1px solid #e2e8f0;\n"
"}")

        self.horizontalLayout_25.addWidget(self.endpoint_server, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.edit_endpoint = QPushButton(self.widgetLayout_30)
        self.edit_endpoint.setObjectName(u"edit_endpoint")
        self.edit_endpoint.setMinimumSize(QSize(26, 26))
        self.edit_endpoint.setMaximumSize(QSize(26, 26))
        font13 = QFont()
        font13.setPointSize(12)
        self.edit_endpoint.setFont(font13)
        self.edit_endpoint.setFlat(True)

        self.horizontalLayout_25.addWidget(self.edit_endpoint, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_25.setStretch(1, 1)

        self.verticalLayout_24.addLayout(self.horizontalLayout_25)


        self.horizontalLayout_26.addLayout(self.verticalLayout_24)


        self.verticalLayout_22.addWidget(self.widgetLayout_30)

        self.widgetLayout_27 = QWidget(self.frame_5)
        self.widgetLayout_27.setObjectName(u"widgetLayout_27")
        self.horizontalLayout_27 = QHBoxLayout(self.widgetLayout_27)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, 0, -1, -1)
        self.label_64 = QLabel(self.widgetLayout_27)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setMinimumSize(QSize(19, 19))
        self.label_64.setMaximumSize(QSize(19, 19))

        self.horizontalLayout_27.addWidget(self.label_64, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignBottom)

        self.label_65 = QLabel(self.widgetLayout_27)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setFont(font6)

        self.horizontalLayout_27.addWidget(self.label_65, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.time_last_conection = QLabel(self.widgetLayout_27)
        self.time_last_conection.setObjectName(u"time_last_conection")
        self.time_last_conection.setFont(font10)

        self.horizontalLayout_27.addWidget(self.time_last_conection, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)

        self.horizontalLayout_27.setStretch(1, 1)

        self.verticalLayout_22.addWidget(self.widgetLayout_27)


        self.verticalLayout_23.addWidget(self.frame_5)

        self.verticalLayout_23.setStretch(2, 2)
        self.verticalLayout_23.setStretch(3, 2)
        self.stackedWidget.addWidget(self.page_0)
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setStyleSheet(u"/* --- ESTILO PARA QCOMBOBOX (Listas desplegables) --- */\n"
"QComboBox {\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 8px;\n"
"    padding: 5px 10px;\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"    min-width: 150px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #2563eb;\n"
"}\n"
"\n"
"/* El \u00e1rea donde reside la flecha */\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 30px;\n"
"    border-left: 1px solid #f1f5f9; /* L\u00ednea divisoria sutil */\n"
"    border-top-right-radius: 8px;\n"
"    border-bottom-right-radius: 8px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    /* La ruta ahora apunta al prefijo que creaste en el recurso */\n"
"    image: url(\":assets/icons/chevron.svg\");\n"
"    width: 14px;\n"
"    height: 14px;\n"
"}\n"
"\n"
"/* Estilo del men\u00fa desplegable (La lista) */\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #e2e8f0;\n"
"    background-color: #ffffff;\n"
""
                        "    selection-background-color: #eff6ff;\n"
"    selection-color: #2563eb;\n"
"    outline: none;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"/* ESTILOS PARA BOTON PRINCIPAL */\n"
"QPushButton#app_update {\n"
"    background-color: #2563eb;\n"
"    color: #ffffff;\n"
"    border: 1px solid #1d4ed8;\n"
"	padding-right: 3px;\n"
"	border-radius: 8px;\n"
"}\n"
"\n"
"QPushButton#app_update:hover {\n"
"    background-color: #1d4ed8;\n"
"}\n"
"\n"
"QPushButton#app_update:pressed {\n"
"    background-color: #2563eb;\n"
"}\n"
"\n"
"QFrame#widgetApps {\n"
"    border: 1px solid #e2e8f0;\n"
"    border-top-right-radius: 8px;\n"
"    border-top-left-radius: 8px;\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"}\n"
"\n"
"QFrame#stats_apps {\n"
"	border-bottom: 1px solid #e2e8f0;\n"
"    border-top-right-radius: 8px;\n"
"    border-top-left-radius: 8px;\n"
"    background-color: #ffffff;\n"
"	padding-right: 5px;\n"
"    color: #475569;\n"
"}\n"
"\n"
"/* ESTILOS TOGGLE APPS */\n"
"QPushButton#toggleButton:check"
                        "ed,\n"
"QPushButton#toggleButton:pressed {\n"
"	background-color: transparent;\n"
"    border: none;\n"
"}")
        self.verticalLayout_27 = QVBoxLayout(self.page_1)
        self.verticalLayout_27.setSpacing(20)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(12, 12, 12, 12)
        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setSpacing(20)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setSpacing(0)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.label_27 = QLabel(self.page_1)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(150, 25))
        self.label_27.setMaximumSize(QSize(150, 25))
        self.label_27.setFont(font5)

        self.verticalLayout_25.addWidget(self.label_27, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.label_68 = QLabel(self.page_1)
        self.label_68.setObjectName(u"label_68")
        self.label_68.setMinimumSize(QSize(240, 20))
        self.label_68.setMaximumSize(QSize(240, 20))
        self.label_68.setFont(font6)

        self.verticalLayout_25.addWidget(self.label_68, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)


        self.horizontalLayout_30.addLayout(self.verticalLayout_25)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, -1, 9, 4)
        self.filter_cat = QComboBox(self.page_1)
        self.filter_cat.addItem("")
        self.filter_cat.setObjectName(u"filter_cat")
        self.filter_cat.setMinimumSize(QSize(172, 0))
        self.filter_cat.setMaximumSize(QSize(200, 35))

        self.horizontalLayout.addWidget(self.filter_cat, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.app_update = QPushButton(self.page_1)
        self.app_update.setObjectName(u"app_update")
        self.app_update.setMinimumSize(QSize(30, 30))
        self.app_update.setMaximumSize(QSize(30, 30))
        self.app_update.setIcon(icon4)
        self.app_update.setCheckable(True)

        self.horizontalLayout.addWidget(self.app_update, 0, Qt.AlignmentFlag.AlignVCenter)


        self.horizontalLayout_30.addLayout(self.horizontalLayout)

        self.horizontalLayout_30.setStretch(0, 1)

        self.verticalLayout_27.addLayout(self.horizontalLayout_30)

        self.containerApps = QFrame(self.page_1)
        self.containerApps.setObjectName(u"containerApps")
        self.verticalLayout_4 = QVBoxLayout(self.containerApps)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.stats_apps = QFrame(self.containerApps)
        self.stats_apps.setObjectName(u"stats_apps")
        self.horizontalLayout_2 = QHBoxLayout(self.stats_apps)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_71 = QLabel(self.stats_apps)
        self.label_71.setObjectName(u"label_71")
        self.label_71.setFont(font6)

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_71)

        self.count_apps = QLabel(self.stats_apps)
        self.count_apps.setObjectName(u"count_apps")
        self.count_apps.setFont(font6)

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.FieldRole, self.count_apps)


        self.horizontalLayout_2.addLayout(self.formLayout_4)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
        self.formLayout_2.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_2.setFormAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignTrailing)
        self.label_73 = QLabel(self.stats_apps)
        self.label_73.setObjectName(u"label_73")
        self.label_73.setFont(font6)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_73)

        self.count_conflicts = QLabel(self.stats_apps)
        self.count_conflicts.setObjectName(u"count_conflicts")
        self.count_conflicts.setFont(font6)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.count_conflicts)


        self.horizontalLayout_2.addLayout(self.formLayout_2)


        self.verticalLayout_4.addWidget(self.stats_apps)

        self.appsScrollArea = QScrollArea(self.containerApps)
        self.appsScrollArea.setObjectName(u"appsScrollArea")
        self.appsScrollArea.setEnabled(True)
        self.appsScrollArea.setMinimumSize(QSize(600, 0))
        self.appsScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.appsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.appsScrollArea.setWidgetResizable(True)
        self.appsScrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 714, 463))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(8)
        self.gridLayout_2.setVerticalSpacing(9)
        self.gridLayout_2.setContentsMargins(8, 8, 8, 8)
        self.widgetApps = QWidget(self.scrollAreaWidgetContents)
        self.widgetApps.setObjectName(u"widgetApps")
        self.verticalLayout = QVBoxLayout(self.widgetApps)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_2.addWidget(self.widgetApps, 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop)

        self.appsScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.appsScrollArea)


        self.verticalLayout_27.addWidget(self.containerApps)

        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setStyleSheet(u"/* ESTILOS PARA BOTON PRINCIPAL */\n"
"QPushButton#unknown_update {\n"
"    background-color: #2563eb;\n"
"    color: #ffffff;\n"
"    border: 1px solid #1d4ed8;\n"
"	padding-right: 3px;\n"
"	border-radius: 8px;\n"
"}\n"
"\n"
"QPushButton#unknown_update:hover {\n"
"    background-color: #1d4ed8;\n"
"}\n"
"\n"
"QPushButton#unknown_update:pressed {\n"
"    background-color: #2563eb;\n"
"}\n"
"\n"
"QPushButton#discovery_apps {\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 8px;\n"
"    padding: 5px 10px;\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"    min-width: 150px;\n"
"}\n"
"\n"
"QPushButton#discovery_apps:hover {\n"
"    border: 1px solid #2563eb;\n"
"}\n"
"\n"
"QPushButton#discovery_apps:pressed {\n"
"    background-color: #f8faff;\n"
"}\n"
"\n"
"QPushButton#discovery_apps:disabled {\n"
"    background-color: #f1f5f9;\n"
"    color: #94a3b8;\n"
"    border: 1px solid #e2e8f0;\n"
"}\n"
"\n"
"QFrame#widgetUnknown {\n"
"    border: 1px solid #e2e8f0;\n"
"    border-top-right-radiu"
                        "s: 8px;\n"
"    border-top-left-radius: 8px;\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"}\n"
"\n"
"QFrame#stats_unknown {\n"
"	border-bottom: 1px solid #e2e8f0;\n"
"    border-top-right-radius: 8px;\n"
"    border-top-left-radius: 8px;\n"
"    background-color: #ffffff;\n"
"	padding-right: 5px;\n"
"    color: #475569;\n"
"}\n"
"\n"
"/* ESTILOS TOGGLE APPS */\n"
"QPushButton#switch:checked,\n"
"QPushButton#switch:pressed {\n"
"	background-color: transparent;\n"
"    border: none;\n"
"}")
        self.verticalLayout_29 = QVBoxLayout(self.page_2)
        self.verticalLayout_29.setSpacing(20)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(12, 12, 12, 12)
        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setSpacing(20)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.verticalLayout_28 = QVBoxLayout()
        self.verticalLayout_28.setSpacing(0)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.label_69 = QLabel(self.page_2)
        self.label_69.setObjectName(u"label_69")
        self.label_69.setMinimumSize(QSize(200, 25))
        self.label_69.setMaximumSize(QSize(200, 25))
        self.label_69.setFont(font5)

        self.verticalLayout_28.addWidget(self.label_69, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.label_70 = QLabel(self.page_2)
        self.label_70.setObjectName(u"label_70")
        self.label_70.setMinimumSize(QSize(240, 20))
        self.label_70.setMaximumSize(QSize(240, 20))
        self.label_70.setFont(font6)

        self.verticalLayout_28.addWidget(self.label_70, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)


        self.horizontalLayout_31.addLayout(self.verticalLayout_28)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(9, -1, 9, 4)
        self.discovery_apps = QPushButton(self.page_2)
        self.discovery_apps.setObjectName(u"discovery_apps")
        self.discovery_apps.setEnabled(False)
        self.discovery_apps.setMinimumSize(QSize(172, 30))
        self.discovery_apps.setMaximumSize(QSize(150, 30))

        self.horizontalLayout_4.addWidget(self.discovery_apps, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.unknown_update = QPushButton(self.page_2)
        self.unknown_update.setObjectName(u"unknown_update")
        self.unknown_update.setMinimumSize(QSize(30, 30))
        self.unknown_update.setMaximumSize(QSize(30, 30))
        self.unknown_update.setStyleSheet(u"")
        self.unknown_update.setIcon(icon4)
        self.unknown_update.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.unknown_update, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.horizontalLayout_31.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_31.setStretch(0, 1)

        self.verticalLayout_29.addLayout(self.horizontalLayout_31)

        self.widgetUnknown = QFrame(self.page_2)
        self.widgetUnknown.setObjectName(u"widgetUnknown")
        self.verticalLayout_7 = QVBoxLayout(self.widgetUnknown)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.stats_unknown = QFrame(self.widgetUnknown)
        self.stats_unknown.setObjectName(u"stats_unknown")
        self.horizontalLayout_32 = QHBoxLayout(self.stats_unknown)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.label_75 = QLabel(self.stats_unknown)
        self.label_75.setObjectName(u"label_75")
        self.label_75.setFont(font6)

        self.formLayout_6.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_75)

        self.count_unknown_total = QLabel(self.stats_unknown)
        self.count_unknown_total.setObjectName(u"count_unknown_total")
        self.count_unknown_total.setFont(font6)

        self.formLayout_6.setWidget(0, QFormLayout.ItemRole.FieldRole, self.count_unknown_total)


        self.horizontalLayout_32.addLayout(self.formLayout_6)

        self.formLayout_7 = QFormLayout()
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.formLayout_7.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
        self.formLayout_7.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_7.setFormAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignTrailing)
        self.label_77 = QLabel(self.stats_unknown)
        self.label_77.setObjectName(u"label_77")
        self.label_77.setFont(font6)

        self.formLayout_7.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_77)

        self.count_unknown_off = QLabel(self.stats_unknown)
        self.count_unknown_off.setObjectName(u"count_unknown_off")
        self.count_unknown_off.setFont(font6)

        self.formLayout_7.setWidget(0, QFormLayout.ItemRole.FieldRole, self.count_unknown_off)


        self.horizontalLayout_32.addLayout(self.formLayout_7)


        self.verticalLayout_7.addWidget(self.stats_unknown)

        self.listView = QListView(self.widgetUnknown)
        self.listView.setObjectName(u"listView")

        self.verticalLayout_7.addWidget(self.listView)


        self.verticalLayout_29.addWidget(self.widgetUnknown)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayoutWidget = QWidget(self.page_3)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(350, 30, 291, 531))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.listView_2 = QListView(self.verticalLayoutWidget)
        self.listView_2.setObjectName(u"listView_2")

        self.verticalLayout_2.addWidget(self.listView_2)

        self.line = QFrame(self.page_3)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(290, 30, 31, 541))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.stackedWidget.addWidget(self.page_3)

        self.horizontalLayout_22.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setMinimumSize(QSize(3, 25))
        self.statusbar.setMaximumSize(QSize(16777215, 25))
        font14 = QFont()
        font14.setPointSize(10)
        font14.setBold(False)
        self.statusbar.setFont(font14)
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Dotfiles-Manager", None))
#if QT_CONFIG(statustip)
        self.nav_0.setStatusTip(QCoreApplication.translate("MainWindow", u"Dashboard", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.nav_1.setStatusTip(QCoreApplication.translate("MainWindow", u"Aplicaciones", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.nav_2.setStatusTip(QCoreApplication.translate("MainWindow", u"Dotfiles desconocidos", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.nav_3.setStatusTip(QCoreApplication.translate("MainWindow", u"Ajustes", None))
#endif // QT_CONFIG(statustip)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Resumen de sincronizaci\u00f3n y estado local.", None))
#if QT_CONFIG(statustip)
        self.main_update.setStatusTip(QCoreApplication.translate("MainWindow", u"Comprueba cambios en todos los dotfiles", None))
#endif // QT_CONFIG(statustip)
        self.main_update.setText(QCoreApplication.translate("MainWindow", u" Actualizar", None))
        self.main_update.setProperty(u"method", QCoreApplication.translate("MainWindow", u"update_action", None))
        self.main_update.setProperty(u"action", QCoreApplication.translate("MainWindow", u"update", None))
        self.update_dotfiles.setText(QCoreApplication.translate("MainWindow", u"DOTFILES", None))
#if QT_CONFIG(statustip)
        self.check_dotfiles.setStatusTip(QCoreApplication.translate("MainWindow", u"Comprueba cambios en los dotfiles", None))
#endif // QT_CONFIG(statustip)
        self.check_dotfiles.setProperty(u"method", QCoreApplication.translate("MainWindow", u"check_action", None))
        self.check_dotfiles.setProperty(u"action", QCoreApplication.translate("MainWindow", u"RESUME_ALL", None))
        self.count_dotfiles.setText(QCoreApplication.translate("MainWindow", u"142", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"SHA:", None))
        self.hash_dotfiles.setText(QCoreApplication.translate("MainWindow", u"a7b2f91...", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Check:", None))
        self.time_last_dotfiles.setText(QCoreApplication.translate("MainWindow", u"22 / 03 / 2026", None))
#if QT_CONFIG(statustip)
        self.led_dotfiles.setStatusTip(QCoreApplication.translate("MainWindow", u"Necesita actualizar", None))
#endif // QT_CONFIG(statustip)
        self.update_apps.setText(QCoreApplication.translate("MainWindow", u"APLICACIONES", None))
#if QT_CONFIG(statustip)
        self.check_apps.setStatusTip(QCoreApplication.translate("MainWindow", u"Comprueba cambios en las aplicaciones", None))
#endif // QT_CONFIG(statustip)
        self.check_apps.setProperty(u"method", QCoreApplication.translate("MainWindow", u"check_action", None))
        self.check_apps.setProperty(u"action", QCoreApplication.translate("MainWindow", u"KNOWNS", None))
        self.count_files_apps.setText(QCoreApplication.translate("MainWindow", u"28", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"SHA:", None))
        self.hash_apps.setText(QCoreApplication.translate("MainWindow", u"f00188c...", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Check:", None))
        self.time_last_apps.setText(QCoreApplication.translate("MainWindow", u"22 / 03 / 2026", None))
#if QT_CONFIG(statustip)
        self.led_apps.setStatusTip(QCoreApplication.translate("MainWindow", u"Necesita actualizar", None))
#endif // QT_CONFIG(statustip)
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"DESCONOCIDOS", None))
#if QT_CONFIG(statustip)
        self.check_unknown.setStatusTip(QCoreApplication.translate("MainWindow", u"Comprueba cambios en los dotfiles desconocidos", None))
#endif // QT_CONFIG(statustip)
        self.check_unknown.setProperty(u"method", QCoreApplication.translate("MainWindow", u"check_action", None))
        self.check_unknown.setProperty(u"action", QCoreApplication.translate("MainWindow", u"UNKNOWNS", None))
        self.count_files_unknown.setText(QCoreApplication.translate("MainWindow", u"12", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"SHA:", None))
        self.hash_unknown.setText(QCoreApplication.translate("MainWindow", u"a7b2f91...", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Check:", None))
        self.time_last_unknown.setText(QCoreApplication.translate("MainWindow", u"22 / 03 / 2026", None))
#if QT_CONFIG(statustip)
        self.led_unknown.setStatusTip(QCoreApplication.translate("MainWindow", u"Necesita actualizar", None))
#endif // QT_CONFIG(statustip)
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\U000f01c4", None))
        self.hostname.setText(QCoreApplication.translate("MainWindow", u"Hi10Max", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"\ue77d", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Sistema Operativo", None))
        self.os_machine.setText(QCoreApplication.translate("MainWindow", u"Debian x86_64", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"\uee40", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"ID de la m\u00e1quina", None))
        self.id_machine.setText(QCoreApplication.translate("MainWindow", u"876fb2f673964d60b7d814ebfc2cbb2b", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"\uea74", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"Versi\u00f3n Manager", None))
        self.version_manager.setText(QCoreApplication.translate("MainWindow", u"0.0.1", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"\ueb29", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"Comprobar actualizaci\u00f3n", None))
#if QT_CONFIG(statustip)
        self.check_updates.setStatusTip(QCoreApplication.translate("MainWindow", u"Comprueba la \u00faltima versi\u00f3n del manager", None))
#endif // QT_CONFIG(statustip)
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"\uf233", None))
        self.label_67.setText(QCoreApplication.translate("MainWindow", u"Servidor", None))
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"Endpoint", None))
        self.label_62.setText(QCoreApplication.translate("MainWindow", u"\U000f0a60", None))
        self.endpoint_server.setText("")
#if QT_CONFIG(statustip)
        self.edit_endpoint.setStatusTip(QCoreApplication.translate("MainWindow", u"Edita el endpoint", None))
#endif // QT_CONFIG(statustip)
        self.edit_endpoint.setText(QCoreApplication.translate("MainWindow", u"\uf044", None))
        self.label_64.setText(QCoreApplication.translate("MainWindow", u"\uf274", None))
        self.label_65.setText(QCoreApplication.translate("MainWindow", u"\u00daltima conexi\u00f3n", None))
        self.time_last_conection.setText("")
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Aplicaciones", None))
        self.label_68.setText(QCoreApplication.translate("MainWindow", u"Gesti\u00f3n de aplicaciones identificadas.", None))
        self.filter_cat.setItemText(0, QCoreApplication.translate("MainWindow", u"Todas categor\u00edas", None))

        self.label_71.setText(QCoreApplication.translate("MainWindow", u"Total aplicaciones:", None))
        self.count_apps.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_73.setText(QCoreApplication.translate("MainWindow", u"Conflictos:", None))
        self.count_conflicts.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_69.setText(QCoreApplication.translate("MainWindow", u"Dotfiles Desconocidos", None))
        self.label_70.setText(QCoreApplication.translate("MainWindow", u"Archivos detectados sin vinculaci\u00f3n a aplicaciones conocidas.", None))
        self.discovery_apps.setText(QCoreApplication.translate("MainWindow", u"Descubrimiento", None))
        self.unknown_update.setText("")
        self.label_75.setText(QCoreApplication.translate("MainWindow", u"Total:", None))
        self.count_unknown_total.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.label_77.setText(QCoreApplication.translate("MainWindow", u"deshabilitados:", None))
        self.count_unknown_off.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Reglas ignorados", None))
    # retranslateUi

