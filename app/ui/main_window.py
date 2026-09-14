from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UserConfig")
        self.resize(1050, 650)
        self.setMinimumSize(900, 550)

        self._build_ui()
        self._apply_base_style()

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(45, 40, 45, 40)
        main_layout.setSpacing(20)

        title = QLabel("Configuración de Usuario")
        title.setObjectName("titleLabel")

        subtitle = QLabel(
            "Administra las preferencias y configuración local "
            "de la aplicación."
        )
        subtitle.setObjectName("subtitleLabel")

        card = QFrame()
        card.setObjectName("welcomeCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(8)

        welcome_label = QLabel("Bienvenido")
        welcome_label.setObjectName("cardTitle")

        description_label = QLabel(
            "La configuración de la aplicación se cargará "
            "automáticamente desde el archivo local."
        )
        description_label.setObjectName("cardDescription")
        description_label.setWordWrap(True)

        status_label = QLabel("● Sistema listo")
        status_label.setObjectName("statusLabel")

        card_layout.addWidget(welcome_label)
        card_layout.addWidget(description_label)
        card_layout.addSpacing(14)
        card_layout.addWidget(status_label)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(10)
        main_layout.addWidget(card)
        main_layout.addStretch()

    def _apply_base_style(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #F4F6F8;
            }

            QLabel#titleLabel {
                color: #111827;
                font-size: 30px;
                font-weight: 700;
            }

            QLabel#subtitleLabel {
                color: #6B7280;
                font-size: 14px;
            }

            QFrame#welcomeCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 14px;
            }

            QLabel#cardTitle {
                color: #111827;
                font-size: 20px;
                font-weight: 600;
            }

            QLabel#cardDescription {
                color: #6B7280;
                font-size: 13px;
            }

            QLabel#statusLabel {
                color: #15803D;
                font-size: 13px;
                font-weight: 600;
            }
            """
        )