from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPixmap,
)
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from app.core.i18n import text
from app.core.user_config import UserConfig
from app.services.config_manager import ConfigManager
from app.services.profile_manager import ProfileManager
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

    # =========================================================
    # TRADUCCIONES
    # =========================================================

    def _txt(self, key: str) -> str:
        return text(
            self.config.idioma,
            key,
        )

    # =========================================================
    # CONSTRUIR INTERFAZ
    # =========================================================

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
            30,
            26,
            30,
            28,
        )

        main_layout.setSpacing(18)

        self._build_header(
            main_layout
        )

        self._build_profile_card(
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
        header.setObjectName(
            "headerCard"
        )

        layout = QHBoxLayout(
            header
        )

        layout.setContentsMargins(
            22,
            15,
            18,
            15,
        )

        layout.setSpacing(14)

        # -----------------------------------------------------
        # Título
        # -----------------------------------------------------

        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(1)

        app_name = QLabel(
            self._txt("app_subtitle")
        )

        app_name.setObjectName(
            "appName"
        )

        brand_layout.addWidget(
            app_name
        )

        layout.addLayout(
            brand_layout
        )

        layout.addSpacing(8)
        layout.addStretch()

        # -----------------------------------------------------
        # Navegación
        # -----------------------------------------------------

        navigation = QFrame()

        navigation.setObjectName(
            "navigationBar"
        )

        nav_layout = QHBoxLayout(
            navigation
        )

        nav_layout.setContentsMargins(
            4,
            4,
            4,
            4,
        )

        nav_layout.setSpacing(2)

        # =====================================================
        # ARCHIVO
        # =====================================================

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
                "new"
            )
        )

        action_open.triggered.connect(
            lambda: self._show_simulated_action(
                "open"
            )
        )

        # Salir sí tiene funcionalidad real.
        action_exit.triggered.connect(
            self.close
        )

        file_button.setMenu(
            file_menu
        )

        # =====================================================
        # EDICIÓN
        # =====================================================

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
                "undo"
            )
        )

        action_copy.triggered.connect(
            lambda: self._show_simulated_action(
                "copy"
            )
        )

        action_paste.triggered.connect(
            lambda: self._show_simulated_action(
                "paste"
            )
        )

        edit_button.setMenu(
            edit_menu
        )

        # =====================================================
        # VER
        # =====================================================

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
                "refresh"
            )
        )

        action_info.triggered.connect(
            lambda: self._show_simulated_action(
                "interface_info"
            )
        )

        view_button.setMenu(
            view_menu
        )

        # -----------------------------------------------------
        # Agregar menús
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Estado
        # -----------------------------------------------------

        status = QLabel(
            f"●  {self._status_text()}"
        )

        status.setObjectName(
            "statusBadge"
        )

        status.setProperty(
            "state",
            self._status_state(),
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

        # -----------------------------------------------------
        # Settings
        # -----------------------------------------------------

        settings_button = QPushButton(
            self._txt("settings")
        )

        settings_button.setObjectName(
            "settingsMenuButton"
        )

        settings_button.setCursor(
            Qt.PointingHandCursor
        )

        settings_button.setToolTip(
            self._txt("settings")
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

        self._apply_shadow(
            header,
            blur=26,
            y_offset=5,
        )

    def _create_menu_button(
        self,
        label: str,
    ) -> QToolButton:
        button = QToolButton()

        button.setText(
            label
        )

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

    # =========================================================
    # ESTADO
    # =========================================================

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

            "Configuración recuperada":
                "status_recovered",
        }

        key = status_map.get(
            self.load_status,
            "status_ready",
        )

        return self._txt(
            key
        )

    def _status_state(self) -> str:
        states = {
            "Configuración cargada":
                "ok",

            "Valores predeterminados":
                "info",

            "Configuración recuperada":
                "recovered",

            "Configuración inválida":
                "warning",

            "Formato no válido":
                "warning",

            "Sin permiso de lectura":
                "error",

            "Error al leer configuración":
                "error",
        }

        return states.get(
            self.load_status,
            "ok",
        )

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

            # Reconstruye la interfaz para aplicar
            # tema, idioma, fuente y colores.
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

        layout = QHBoxLayout(
            card
        )

        layout.setContentsMargins(
            32,
            30,
            32,
            30,
        )

        layout.setSpacing(28)

        # -----------------------------------------------------
        # Avatar
        # -----------------------------------------------------

        avatar = QLabel()

        avatar.setObjectName(
            "avatar"
        )

        avatar.setAlignment(
            Qt.AlignCenter
        )

        avatar.setFixedSize(
            104,
            104,
        )

        self._load_avatar(
            avatar,
            104,
        )

        # -----------------------------------------------------
        # Información
        # -----------------------------------------------------

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
                name=(
                    self.config
                    .nombre_usuario
                )
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

        description.setWordWrap(
            True
        )

        # -----------------------------------------------------
        # Chips de preferencias
        # -----------------------------------------------------

        chips = QHBoxLayout()
        chips.setSpacing(8)

        chip_values = (
            self._theme_name(),
            self.config.idioma,
            (
                f"{self.config.tamano_fuente} "
                "px"
            ),
        )

        for value in chip_values:
            chip = QLabel(
                value
            )

            chip.setObjectName(
                "preferenceChip"
            )

            chip.setAlignment(
                Qt.AlignCenter
            )

            chips.addWidget(
                chip
            )

        chips.addStretch()

        # -----------------------------------------------------
        # Botón real de configuración
        # -----------------------------------------------------

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

        buttons.addWidget(
            settings_button
        )

        buttons.addStretch()

        # -----------------------------------------------------
        # Composición
        # -----------------------------------------------------

        information.addWidget(
            eyebrow
        )

        information.addWidget(
            greeting
        )

        information.addWidget(
            description
        )

        information.addSpacing(2)

        information.addLayout(
            chips
        )

        information.addSpacing(8)

        information.addLayout(
            buttons
        )

        layout.addWidget(
            avatar,
            0,
            Qt.AlignVCenter,
        )

        layout.addLayout(
            information,
            1,
        )

        parent_layout.addWidget(
            card
        )

        self._apply_shadow(
            card,
            blur=34,
            y_offset=8,
        )

    # =========================================================
    # ACCIONES SIMULADAS
    # =========================================================

    def _show_simulated_action(
        self,
        action_key: str,
    ):
        messages = {
            "new": (
                "new",
                "msg_new",
            ),

            "open": (
                "open",
                "msg_open",
            ),

            "undo": (
                "undo",
                "msg_undo",
            ),

            "copy": (
                "copy",
                "msg_copy",
            ),

            "paste": (
                "paste",
                "msg_paste",
            ),

            "refresh": (
                "refresh",
                "msg_refresh",
            ),

            "interface_info": (
                "interface_info",
                "msg_interface_info",
            ),
        }

        action_data = messages.get(
            action_key
        )

        if action_data is None:
            return

        title_key, message_key = (
            action_data
        )

        QMessageBox.information(
            self,
            self._txt(title_key),
            self._txt(message_key),
        )

    # =========================================================
    # AVATAR
    # =========================================================

    def _get_initials(
        self,
        name: str,
    ) -> str:
        parts = (
            name.strip().split()
        )

        if not parts:
            return "U"

        if len(parts) == 1:
            return (
                parts[0][0].upper()
            )

        return (
            parts[0][0]
            + parts[-1][0]
        ).upper()

    def _load_avatar(
        self,
        avatar: QLabel,
        size: int = 104,
    ):
        profile_path = (
            self.profile_manager
            .resolve_profile_path(
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
                        size,
                    )
                )

                return

        # Si no hay fotografía válida,
        # muestra las iniciales.
        avatar.setPixmap(
            QPixmap()
        )

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
        scaled = source.scaled(
            size,
            size,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )

        x = max(
            0,
            (
                scaled.width()
                - size
            ) // 2,
        )

        y = max(
            0,
            (
                scaled.height()
                - size
            ) // 2,
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

        painter = QPainter(
            result
        )

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

        painter.setClipPath(
            path
        )

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

    def _apply_shadow(
        self,
        widget: QWidget,
        blur: int = 28,
        y_offset: int = 6,
    ):
        shadow = (
            QGraphicsDropShadowEffect(
                widget
            )
        )

        shadow.setBlurRadius(
            blur
        )

        shadow.setOffset(
            0,
            y_offset,
        )

        if (
            self.config.tema_interfaz
            == "oscuro"
        ):
            shadow.setColor(
                QColor(
                    0,
                    0,
                    0,
                    92,
                )
            )

        else:
            shadow.setColor(
                QColor(
                    31,
                    45,
                    39,
                    34,
                )
            )

        widget.setGraphicsEffect(
            shadow
        )

    def _apply_current_theme(self):
        self.setStyleSheet(
            build_main_stylesheet(
                self.config
            )
        )