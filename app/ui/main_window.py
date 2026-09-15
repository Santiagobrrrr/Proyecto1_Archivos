from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtGui import (
    QPainter,
    QPainterPath,
    QPixmap,
)

from app.services.profile_manager import ProfileManager
from app.core.i18n import text
from app.core.user_config import UserConfig
from app.services.config_manager import ConfigManager
from app.ui.settings_window import SettingsWindow
from app.ui.theme_manager import build_main_stylesheet


class MainWindow(QMainWindow):
    def __init__(
        self,
        config: UserConfig,
        config_manager: ConfigManager,
        load_status: str = "Sistema listo",
    ):
        super().__init__()

        self.config = config
        self.config_manager = config_manager
        self.profile_manager = ProfileManager()
        self.load_status = load_status

        self.setWindowTitle("UserConfig")
        self.resize(1120, 700)
        self.setMinimumSize(960, 600)

        self._render_ui()

    def _txt(self, key: str) -> str:
        return text(
            self.config.idioma,
            key,
        )

    def _render_ui(self):
        old_widget = self.takeCentralWidget()

        if old_widget is not None:
            old_widget.deleteLater()

        self._build_ui()
        self._apply_current_theme()

    def _build_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName(
            "centralWidget"
        )

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            32,
            28,
            32,
            28,
        )
        main_layout.setSpacing(22)

        self._build_header(
            main_layout
        )

        self._build_profile_card(
            main_layout
        )

        self._build_info_cards(
            main_layout
        )

        main_layout.addStretch()

    # =========================================================
    # HEADER
    # =========================================================

    def _build_header(
        self,
        parent_layout,
    ):
        header = QFrame()
        header.setObjectName("headerCard")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(
            24,
            14,
            20,
            14,
        )
        layout.setSpacing(16)

        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(1)

        app_name = QLabel("UserConfig")
        app_name.setObjectName("appName")

        subtitle = QLabel(
            self._txt("app_subtitle")
        )
        subtitle.setObjectName(
            "appSubtitle"
        )

        brand_layout.addWidget(
            app_name
        )
        brand_layout.addWidget(
            subtitle
        )

        layout.addLayout(
            brand_layout
        )

        layout.addStretch()

        navigation = QFrame()
        navigation.setObjectName(
            "navigationBar"
        )

        nav_layout = QHBoxLayout(
            navigation
        )
        nav_layout.setContentsMargins(
            5,
            5,
            5,
            5,
        )
        nav_layout.setSpacing(2)

        # Archivo / File
        file_button = (
            self._create_menu_button(
                self._txt("menu_file")
            )
        )

        file_menu = QMenu(
            file_button
        )

        action_new = file_menu.addAction(
            self._txt("new")
        )

        action_open = file_menu.addAction(
            self._txt("open")
        )

        file_menu.addSeparator()

        action_exit = file_menu.addAction(
            self._txt("exit")
        )

        action_new.triggered.connect(
            lambda: self._show_simulated_action(
                self._txt("new")
            )
        )

        action_open.triggered.connect(
            lambda: self._show_simulated_action(
                self._txt("open")
            )
        )

        action_exit.triggered.connect(
            self.close
        )

        file_button.setMenu(
            file_menu
        )

        # Edición / Edit
        edit_button = (
            self._create_menu_button(
                self._txt("menu_edit")
            )
        )

        edit_menu = QMenu(
            edit_button
        )

        action_undo = edit_menu.addAction(
            self._txt("undo")
        )

        action_copy = edit_menu.addAction(
            self._txt("copy")
        )

        action_paste = edit_menu.addAction(
            self._txt("paste")
        )

        action_undo.triggered.connect(
            lambda: self._show_simulated_action(
                self._txt("undo")
            )
        )

        action_copy.triggered.connect(
            lambda: self._show_simulated_action(
                self._txt("copy")
            )
        )

        action_paste.triggered.connect(
            lambda: self._show_simulated_action(
                self._txt("paste")
            )
        )

        edit_button.setMenu(
            edit_menu
        )

        # Ver / View
        view_button = (
            self._create_menu_button(
                self._txt("menu_view")
            )
        )

        view_menu = QMenu(
            view_button
        )

        action_refresh = (
            view_menu.addAction(
                self._txt("refresh")
            )
        )

        action_info = (
            view_menu.addAction(
                self._txt(
                    "interface_info"
                )
            )
        )

        action_refresh.triggered.connect(
            lambda: self._show_simulated_action(
                self._txt("refresh")
            )
        )

        action_info.triggered.connect(
            lambda: self._show_simulated_action(
                self._txt(
                    "interface_info"
                )
            )
        )

        view_button.setMenu(
            view_menu
        )

        nav_layout.addWidget(
            file_button
        )
        nav_layout.addWidget(
            edit_button
        )
        nav_layout.addWidget(
            view_button
        )

        layout.addWidget(
            navigation
        )

        status = QLabel(
            f"●  {self._status_text()}"
        )
        status.setObjectName(
            "statusBadge"
        )
        status.setAlignment(
            Qt.AlignCenter
        )
        status.setToolTip(
            self.load_status
        )

        layout.addWidget(
            status
        )

        settings_button = QPushButton(
            self._txt("settings")
        )
        settings_button.setObjectName(
            "settingsMenuButton"
        )
        settings_button.setCursor(
            Qt.PointingHandCursor
        )

        settings_button.clicked.connect(
            self._open_settings
        )

        layout.addWidget(
            settings_button
        )

        parent_layout.addWidget(
            header
        )

    def _create_menu_button(
        self,
        label: str,
    ) -> QToolButton:
        button = QToolButton()

        button.setText(label)
        button.setObjectName(
            "menuButton"
        )

        button.setPopupMode(
            QToolButton.InstantPopup
        )

        button.setToolButtonStyle(
            Qt.ToolButtonTextOnly
        )

        button.setCursor(
            Qt.PointingHandCursor
        )

        return button

    def _status_text(self) -> str:
        status_map = {
            "Configuración cargada":
                "status_ready",

            "Valores predeterminados":
                "status_default",

            "Configuración inválida":
                "status_invalid",

            "Sin permiso de lectura":
                "status_no_access",

            "Formato no válido":
                "status_format",

            "Error al leer configuración":
                "status_error",
            
            "Configuración recuperada": "status_recovered",
        }

        key = status_map.get(
            self.load_status,
            "status_ready",
        )

        return self._txt(key)

    # =========================================================
    # SETTINGS
    # =========================================================

    def _open_settings(self):
        dialog = SettingsWindow(
            config=self.config,
            config_manager=self.config_manager,
            parent=self,
        )

        if (
            dialog.exec()
            == QDialog.Accepted
        ):
            self.config = (
                dialog.updated_config
            )

            # Reconstruye toda la interfaz para
            # aplicar tema, idioma, fuente y colores.
            self._render_ui()

    # =========================================================
    # PERFIL
    # =========================================================

    def _build_profile_card(
        self,
        parent_layout,
    ):
        card = QFrame()
        card.setObjectName(
            "profileCard"
        )

        layout = QHBoxLayout(card)
        layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )
        layout.setSpacing(24)

        avatar = QLabel()
        avatar.setObjectName("avatar")
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFixedSize(92, 92)

        self._load_avatar(avatar)

        information = QVBoxLayout()
        information.setSpacing(8)

        eyebrow = QLabel(
            self._txt("profile")
        )
        eyebrow.setObjectName(
            "eyebrow"
        )

        greeting = QLabel(
            self._txt("welcome").format(
                name=self.config.nombre_usuario
            )
        )
        greeting.setObjectName(
            "greeting"
        )

        description = QLabel(
            self._txt(
                "profile_description"
            )
        )
        description.setObjectName(
            "description"
        )
        description.setWordWrap(True)

        preferences = QLabel(
            f"{self._theme_name()}   ·   "
            f"{self.config.idioma}   ·   "
            f"{self.config.tamano_fuente} px"
        )
        preferences.setObjectName(
            "preferences"
        )

        buttons = QHBoxLayout()
        buttons.setSpacing(10)

        settings_button = QPushButton(
            self._txt("configure")
        )
        settings_button.setObjectName(
            "primaryButton"
        )
        settings_button.setCursor(
            Qt.PointingHandCursor
        )

        settings_button.clicked.connect(
            self._open_settings
        )

        preview_button = QPushButton(
            self._txt("preview")
        )
        preview_button.setObjectName(
            "secondaryButton"
        )
        preview_button.setCursor(
            Qt.PointingHandCursor
        )

        buttons.addWidget(
            settings_button
        )
        buttons.addWidget(
            preview_button
        )
        buttons.addStretch()

        information.addWidget(
            eyebrow
        )
        information.addWidget(
            greeting
        )
        information.addWidget(
            description
        )
        information.addWidget(
            preferences
        )
        information.addSpacing(8)
        information.addLayout(
            buttons
        )

        layout.addWidget(
            avatar
        )
        layout.addLayout(
            information,
            1,
        )

        parent_layout.addWidget(
            card
        )

    # =========================================================
    # TARJETAS INFERIORES
    # =========================================================

    def _build_info_cards(
        self,
        parent_layout,
    ):
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        cards_layout.addWidget(
            self._create_info_card(
                "01",
                self._txt("persistence"),
                self._txt(
                    "persistence_description"
                ),
            )
        )

        cards_layout.addWidget(
            self._create_info_card(
                "02",
                self._txt(
                    "personalization"
                ),
                self._txt(
                    "personalization_description"
                ),
            )
        )

        cards_layout.addWidget(
            self._create_info_card(
                "03",
                self._txt("protection"),
                self._txt(
                    "protection_description"
                ),
            )
        )

        parent_layout.addLayout(
            cards_layout
        )

    def _create_info_card(
        self,
        number: str,
        title: str,
        description: str,
    ) -> QFrame:
        card = QFrame()
        card.setObjectName(
            "infoCard"
        )

        card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred,
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            22,
            20,
            22,
            22,
        )
        layout.setSpacing(8)

        number_label = QLabel(
            number
        )
        number_label.setObjectName(
            "cardNumber"
        )

        title_label = QLabel(
            title
        )
        title_label.setObjectName(
            "cardTitle"
        )

        description_label = QLabel(
            description
        )
        description_label.setObjectName(
            "cardDescription"
        )
        description_label.setWordWrap(
            True
        )

        layout.addWidget(
            number_label
        )
        layout.addSpacing(8)
        layout.addWidget(
            title_label
        )
        layout.addWidget(
            description_label
        )
        layout.addStretch()

        return card

    # =========================================================
    # UTILIDADES
    # =========================================================

    def _get_initials(
        self,
        name: str,
    ) -> str:
        parts = name.strip().split()

        if not parts:
            return "U"

        if len(parts) == 1:
            return parts[0][0].upper()

        return (
            parts[0][0]
            + parts[-1][0]
        ).upper()

    def _theme_name(self) -> str:
        if (
            self.config.tema_interfaz
            == "oscuro"
        ):
            return self._txt(
                "theme_dark"
            )

        return self._txt(
            "theme_light"
        )

    def _show_simulated_action(
        self,
        action_name: str,
    ):
        QMessageBox.information(
            self,
            self._txt(
                "simulated_title"
            ),
            self._txt(
                "simulated_message"
            ).format(
                action=action_name
            ),
        )
        
    # otro
    def _load_avatar(
        self,
        avatar: QLabel,
    ):
        """
        Muestra la fotografía del usuario si existe.
        En caso contrario, muestra sus iniciales.
        """

        profile_path = (
            self.profile_manager.resolve_profile_path(
                self.config.foto_perfil
            )
        )

        if (
            profile_path is not None
            and profile_path.exists()
        ):
            pixmap = QPixmap(
                str(profile_path)
            )

            if not pixmap.isNull():
                avatar.setText("")
                avatar.setPixmap(
                    self._circular_pixmap(
                        pixmap,
                        92,
                    )
                )

                return

        # Fallback: iniciales
        avatar.setPixmap(QPixmap())
        avatar.setText(
            self._get_initials(
                self.config.nombre_usuario
            )
        )


    def _circular_pixmap(
        self,
        source: QPixmap,
        size: int,
    ) -> QPixmap:
        """
        Recorta una imagen cuadrada y la dibuja
        dentro de un círculo.
        """

        scaled = source.scaled(
            size,
            size,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )

        x = max(
            0,
            (scaled.width() - size) // 2,
        )

        y = max(
            0,
            (scaled.height() - size) // 2,
        )

        cropped = scaled.copy(
            x,
            y,
            size,
            size,
        )

        result = QPixmap(
            size,
            size,
        )

        result.fill(
            Qt.transparent
        )

        painter = QPainter(result)

        painter.setRenderHint(
            QPainter.Antialiasing,
            True,
        )

        path = QPainterPath()
        path.addEllipse(
            0,
            0,
            size,
            size,
        )

        painter.setClipPath(path)

        painter.drawPixmap(
            0,
            0,
            cropped,
        )

        painter.end()

        return result

    # =========================================================
    # TEMA
    # =========================================================

    def _apply_current_theme(self):
        self.setStyleSheet(
            build_main_stylesheet(
                self.config
            )
        )