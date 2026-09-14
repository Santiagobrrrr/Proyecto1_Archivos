from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.core.user_config import UserConfig


class MainWindow(QMainWindow):
    def __init__(self, config: UserConfig):
        super().__init__()

        self.config = config

        self.setWindowTitle("UserConfig")
        self.resize(1120, 700)
        self.setMinimumSize(960, 600)

        self._build_ui()
        self._apply_base_style()

    def _build_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")

        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(32, 28, 32, 28)
        main_layout.setSpacing(22)

        self._build_header(main_layout)
        self._build_profile_card(main_layout)
        self._build_info_cards(main_layout)

        main_layout.addStretch()

    def _build_header(self, parent_layout):
        header = QFrame()
        header.setObjectName("headerCard")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(16)

        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(3)

        app_name = QLabel("UserConfig")
        app_name.setObjectName("appName")

        subtitle = QLabel(
            "Preferencias y configuración local"
        )
        subtitle.setObjectName("appSubtitle")

        brand_layout.addWidget(app_name)
        brand_layout.addWidget(subtitle)

        status = QLabel("●  Sistema listo")
        status.setObjectName("statusBadge")
        status.setAlignment(Qt.AlignCenter)

        layout.addLayout(brand_layout)
        layout.addStretch()
        layout.addWidget(status)

        parent_layout.addWidget(header)

    def _build_profile_card(self, parent_layout):
        card = QFrame()
        card.setObjectName("profileCard")

        layout = QHBoxLayout(card)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)

        avatar = QLabel(
            self._get_initials(self.config.nombre_usuario)
        )
        avatar.setObjectName("avatar")
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFixedSize(92, 92)

        information = QVBoxLayout()
        information.setSpacing(8)

        eyebrow = QLabel("PERFIL DE USUARIO")
        eyebrow.setObjectName("eyebrow")

        greeting = QLabel(
            f"Bienvenido, {self.config.nombre_usuario}"
        )
        greeting.setObjectName("greeting")

        description = QLabel(
            "Personaliza la aplicación y conserva tus "
            "preferencias de forma segura entre sesiones."
        )
        description.setObjectName("description")
        description.setWordWrap(True)

        preferences = QLabel(
            f"{self._theme_name()}   ·   "
            f"{self.config.idioma}   ·   "
            f"{self.config.tamano_fuente} px"
        )
        preferences.setObjectName("preferences")

        buttons = QHBoxLayout()
        buttons.setSpacing(10)

        self.settings_button = QPushButton(
            "Configurar preferencias"
        )
        self.settings_button.setObjectName("primaryButton")
        self.settings_button.setCursor(
            Qt.PointingHandCursor
        )

        self.preview_button = QPushButton("Vista previa")
        self.preview_button.setObjectName("secondaryButton")
        self.preview_button.setCursor(
            Qt.PointingHandCursor
        )

        buttons.addWidget(self.settings_button)
        buttons.addWidget(self.preview_button)
        buttons.addStretch()

        information.addWidget(eyebrow)
        information.addWidget(greeting)
        information.addWidget(description)
        information.addWidget(preferences)
        information.addSpacing(8)
        information.addLayout(buttons)

        layout.addWidget(avatar)
        layout.addLayout(information, 1)

        parent_layout.addWidget(card)

    def _build_info_cards(self, parent_layout):
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        persistence_card = self._create_info_card(
            "01",
            "Persistencia",
            "Tus preferencias permanecerán disponibles "
            "cuando vuelvas a iniciar la aplicación.",
        )

        personalization_card = self._create_info_card(
            "02",
            "Personalización",
            "Tema, idioma, tipografía, colores y perfil "
            "en un único espacio de configuración.",
        )

        security_card = self._create_info_card(
            "03",
            "Protección",
            "La configuración contará con escritura segura, "
            "respaldo y manejo controlado de errores.",
        )

        cards_layout.addWidget(persistence_card)
        cards_layout.addWidget(personalization_card)
        cards_layout.addWidget(security_card)

        parent_layout.addLayout(cards_layout)

    def _create_info_card(
        self,
        number: str,
        title: str,
        description: str,
    ) -> QFrame:
        card = QFrame()
        card.setObjectName("infoCard")
        card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred,
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(8)

        number_label = QLabel(number)
        number_label.setObjectName("cardNumber")

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        description_label = QLabel(description)
        description_label.setObjectName("cardDescription")
        description_label.setWordWrap(True)

        layout.addWidget(number_label)
        layout.addSpacing(8)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch()

        return card

    def _get_initials(self, name: str) -> str:
        parts = name.strip().split()

        if not parts:
            return "U"

        if len(parts) == 1:
            return parts[0][0].upper()

        return (
            parts[0][0] + parts[-1][0]
        ).upper()

    def _theme_name(self) -> str:
        if self.config.tema_interfaz == "oscuro":
            return "Tema oscuro"

        return "Tema claro"

    def _apply_base_style(self):
        self.setStyleSheet(
            """
            QWidget#centralWidget {
                background-color: #F3F5F2;
            }

            QFrame#headerCard {
                background-color: #FAFBF8;
                border: 1px solid #DCE3DF;
                border-radius: 18px;
            }

            QLabel#appName {
                color: #202824;
                font-size: 23px;
                font-weight: 700;
            }

            QLabel#appSubtitle {
                color: #7A8680;
                font-size: 12px;
            }

            QLabel#statusBadge {
                background-color: #E7F3EA;
                color: #356849;
                border: 1px solid #C9E2D0;
                border-radius: 14px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QFrame#profileCard {
                background-color: #FAFBF8;
                border: 1px solid #DCE3DF;
                border-radius: 24px;
            }

            QLabel#avatar {
                background-color: #E4EFEB;
                color: #35655C;
                border: 1px solid #C9DDD6;
                border-radius: 46px;
                font-size: 27px;
                font-weight: 700;
            }

            QLabel#eyebrow {
                color: #4B786F;
                font-size: 10px;
                font-weight: 700;
            }

            QLabel#greeting {
                color: #202824;
                font-size: 27px;
                font-weight: 700;
            }

            QLabel#description {
                color: #66716C;
                font-size: 13px;
            }

            QLabel#preferences {
                color: #3F7469;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton#primaryButton {
                background-color: #3F7469;
                color: #F8FBF9;
                border: none;
                border-radius: 11px;
                padding: 11px 18px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton#primaryButton:hover {
                background-color: #35655C;
            }

            QPushButton#primaryButton:pressed {
                background-color: #2B554D;
            }

            QPushButton#secondaryButton {
                background-color: #F2F4F1;
                color: #34413B;
                border: 1px solid #D6DEDA;
                border-radius: 11px;
                padding: 10px 18px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton#secondaryButton:hover {
                background-color: #E8ECE9;
                border-color: #C8D2CD;
            }

            QFrame#infoCard {
                background-color: #FAFBF8;
                border: 1px solid #DCE3DF;
                border-radius: 18px;
            }

            QLabel#cardNumber {
                color: #78A399;
                font-size: 12px;
                font-weight: 700;
            }

            QLabel#cardTitle {
                color: #27312D;
                font-size: 16px;
                font-weight: 700;
            }

            QLabel#cardDescription {
                color: #66716C;
                font-size: 12px;
            }
            """
        )