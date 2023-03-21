# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainForm.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)
import ui.resources

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        if not MainForm.objectName():
            MainForm.setObjectName(u"MainForm")
        MainForm.resize(899, 601)
        self.actionExit = QAction(MainForm)
        self.actionExit.setObjectName(u"actionExit")
        self.actionRecalculate_ticks = QAction(MainForm)
        self.actionRecalculate_ticks.setObjectName(u"actionRecalculate_ticks")
        self.actionRecalculate_zigzag = QAction(MainForm)
        self.actionRecalculate_zigzag.setObjectName(u"actionRecalculate_zigzag")
        self.actionRecalculate_EMA = QAction(MainForm)
        self.actionRecalculate_EMA.setObjectName(u"actionRecalculate_EMA")
        self.actionRecalculate_ticks_percents = QAction(MainForm)
        self.actionRecalculate_ticks_percents.setObjectName(u"actionRecalculate_ticks_percents")
        self.actionRecalculate_ticks_points = QAction(MainForm)
        self.actionRecalculate_ticks_points.setObjectName(u"actionRecalculate_ticks_points")
        self.centralwidget = QWidget(MainForm)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName(u"main_layout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.tab)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(64, 32))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.PageDnButton = QPushButton(self.frame)
        self.PageDnButton.setObjectName(u"PageDnButton")
        self.PageDnButton.setMaximumSize(QSize(32, 32))
        icon = QIcon()
        icon.addFile(u":/icons/icons/skip_previous_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.PageDnButton.setIcon(icon)
        self.PageDnButton.setIconSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.PageDnButton)

        self.PageUpButton = QPushButton(self.frame)
        self.PageUpButton.setObjectName(u"PageUpButton")
        self.PageUpButton.setMaximumSize(QSize(32, 32))
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/skip_next_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.PageUpButton.setIcon(icon1)
        self.PageUpButton.setIconSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.PageUpButton)


        self.verticalLayout_2.addWidget(self.frame)

        self.ticks_frame_chart_layout = QVBoxLayout()
        self.ticks_frame_chart_layout.setObjectName(u"ticks_frame_chart_layout")

        self.verticalLayout_2.addLayout(self.ticks_frame_chart_layout)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_3.addWidget(self.tabWidget)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.main_layout.addLayout(self.verticalLayout)


        self.horizontalLayout.addLayout(self.main_layout)

        MainForm.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainForm)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 899, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuCommands = QMenu(self.menubar)
        self.menuCommands.setObjectName(u"menuCommands")
        MainForm.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainForm)
        self.statusbar.setObjectName(u"statusbar")
        MainForm.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCommands.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuCommands.addAction(self.actionRecalculate_ticks)
        self.menuCommands.addAction(self.actionRecalculate_ticks_percents)
        self.menuCommands.addAction(self.actionRecalculate_ticks_points)
        self.menuCommands.addAction(self.actionRecalculate_zigzag)
        self.menuCommands.addAction(self.actionRecalculate_EMA)

        self.retranslateUi(MainForm)

        QMetaObject.connectSlotsByName(MainForm)
    # setupUi

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(QCoreApplication.translate("MainForm", u"RLTrader", None))
        self.actionExit.setText(QCoreApplication.translate("MainForm", u"E&xit", None))
        self.actionRecalculate_ticks.setText(QCoreApplication.translate("MainForm", u"Recalculate &ticks", None))
        self.actionRecalculate_zigzag.setText(QCoreApplication.translate("MainForm", u"Recalculate &zigzag", None))
        self.actionRecalculate_EMA.setText(QCoreApplication.translate("MainForm", u"Recalculate &EMA", None))
        self.actionRecalculate_ticks_percents.setText(QCoreApplication.translate("MainForm", u"Recalculate ticks &percents", None))
        self.actionRecalculate_ticks_points.setText(QCoreApplication.translate("MainForm", u"Recalculate ticks p&oints", None))
        self.PageDnButton.setText("")
        self.PageUpButton.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainForm", u"Main", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainForm", u"Tab 2", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainForm", u"&File", None))
        self.menuCommands.setTitle(QCoreApplication.translate("MainForm", u"Commands", None))
    # retranslateUi

