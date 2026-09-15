from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.core.user_config import UserConfig
from app.services.config_manager import ConfigManager
from app.ui.theme_manager import (
    build_color_dialog_stylesheet,
    build_message_stylesheet,
    build_settings_stylesheet,
)


class SettingsWindow(QDialog):
    def __init__(
        self,
        config: UserConfig,
        config_manager: ConfigManager,
        parent=None,
    ):
        super().__init__(parent)

        self.config_manager = config_manager
        self.current_config = config
        self.updated_config = config

        self.menu_color = config.color_barra_menu
        self.text_color = config.color_letra
        self.profile_path = config.foto_perfil

        self.setWindowTitle("Configuración")
        self.resize(900, 720)
        self.setMinimumSize(820, 640)
        self.setModal(True)

        self._build_ui()
        self._load_config(config)
        self._apply_style()

    # =========================================================
    # INTERFAZ PRINCIPAL
    # =========================================================

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._build_header(root)
        self._build_scroll_content(root)
        self._build_footer(root)

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def _build_header(self, parent_layout):
        header = QFrame()
        header.setObjectName("settingsHeader")

        layout = QVBoxLayout(header)
        layout.setContentsMargins(30, 26, 30, 18)
        layout.setSpacing(6)

        title = QLabel("Configuración")
        title.setObjectName("settingsTitle")

        subtitle = QLabel(
            "Personaliza tu perfil, apariencia y preferencias "
            "de la aplicación."
        )
        subtitle.setObjectName("settingsSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        parent_layout.addWidget(header)

    # =========================================================
    # ÁREA DESPLAZABLE
    # =========================================================

    def _build_scroll_content(self, parent_layout):
        scroll = QScrollArea()
        scroll.setObjectName("settingsScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        content.setObjectName("settingsContent")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 10, 30, 24)
        content_layout.setSpacing(16)

        content_layout.addWidget(
            self._build_profile_card()
        )

        content_layout.addWidget(
            self._build_appearance_card()
        )

        content_layout.addWidget(
            self._build_language_card()
        )

        content_layout.addStretch()

        scroll.setWidget(content)

        parent_layout.addWidget(scroll, 1)

    # =========================================================
    # PERFIL
    # =========================================================

    def _build_profile_card(self):
        card = self._create_card()

        layout = QGridLayout(card)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setHorizontalSpacing(18)
        layout.setVerticalSpacing(9)

        title = QLabel("Perfil")
        title.setObjectName("sectionTitle")

        description = QLabel(
            "Información que identifica al usuario dentro "
            "de la aplicación."
        )
        description.setObjectName("sectionDescription")

        # Nombre
        name_label = QLabel("Nombre de usuario")
        name_label.setObjectName("fieldLabel")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "Ingresa tu nombre"
        )
        self.name_input.setClearButtonEnabled(True)

        # Foto
        photo_label = QLabel("Fotografía de perfil")
        photo_label.setObjectName("fieldLabel")

        photo_container = QFrame()
        photo_container.setObjectName("photoField")

        photo_layout = QHBoxLayout(photo_container)
        photo_layout.setContentsMargins(10, 5, 5, 5)
        photo_layout.setSpacing(10)

        self.photo_path_label = QLabel(
            "Sin fotografía seleccionada"
        )
        self.photo_path_label.setObjectName("pathLabel")

        self.photo_button = QPushButton(
            "Elegir imagen"
        )
        self.photo_button.setObjectName(
            "compactButton"
        )
        self.photo_button.setCursor(
            Qt.PointingHandCursor
        )
        self.photo_button.clicked.connect(
            self._select_photo
        )

        photo_layout.addWidget(
            self.photo_path_label,
            1,
        )

        photo_layout.addWidget(
            self.photo_button
        )

        # Grid
        layout.addWidget(
            title,
            0,
            0,
            1,
            2,
        )

        layout.addWidget(
            description,
            1,
            0,
            1,
            2,
        )

        layout.addWidget(
            name_label,
            2,
            0,
        )

        layout.addWidget(
            photo_label,
            2,
            1,
        )

        layout.addWidget(
            self.name_input,
            3,
            0,
        )

        layout.addWidget(
            photo_container,
            3,
            1,
        )

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        return card

    # =========================================================
    # APARIENCIA
    # =========================================================

    def _build_appearance_card(self):
        card = self._create_card()

        layout = QGridLayout(card)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setHorizontalSpacing(18)
        layout.setVerticalSpacing(9)

        title = QLabel("Apariencia")
        title.setObjectName("sectionTitle")

        description = QLabel(
            "Ajusta cómo quieres visualizar la interfaz."
        )
        description.setObjectName("sectionDescription")

        # Tema
        theme_label = QLabel("Tema de interfaz")
        theme_label.setObjectName("fieldLabel")

        self.theme_combo = QComboBox()

        self.theme_combo.addItem(
            "Claro",
            "claro",
        )

        self.theme_combo.addItem(
            "Oscuro",
            "oscuro",
        )

        # Tamaño fuente
        font_label = QLabel("Tamaño de fuente")
        font_label.setObjectName("fieldLabel")

        self.font_size = QSpinBox()
        self.font_size.setRange(10, 20)
        self.font_size.setSuffix(" px")

        # Colores
        menu_color_label = QLabel(
            "Color de barra de menú"
        )
        menu_color_label.setObjectName("fieldLabel")

        text_color_label = QLabel(
            "Color de letra"
        )
        text_color_label.setObjectName("fieldLabel")

        self.menu_color_button = QPushButton()
        self.menu_color_button.setObjectName(
            "colorButton"
        )
        self.menu_color_button.setCursor(
            Qt.PointingHandCursor
        )
        self.menu_color_button.clicked.connect(
            self._select_menu_color
        )

        self.text_color_button = QPushButton()
        self.text_color_button.setObjectName(
            "colorButton"
        )
        self.text_color_button.setCursor(
            Qt.PointingHandCursor
        )
        self.text_color_button.clicked.connect(
            self._select_text_color
        )

        # Grid
        layout.addWidget(
            title,
            0,
            0,
            1,
            2,
        )

        layout.addWidget(
            description,
            1,
            0,
            1,
            2,
        )

        layout.addWidget(
            theme_label,
            2,
            0,
        )

        layout.addWidget(
            font_label,
            2,
            1,
        )

        layout.addWidget(
            self.theme_combo,
            3,
            0,
        )

        layout.addWidget(
            self.font_size,
            3,
            1,
        )

        layout.addWidget(
            menu_color_label,
            4,
            0,
        )

        layout.addWidget(
            text_color_label,
            4,
            1,
        )

        layout.addWidget(
            self.menu_color_button,
            5,
            0,
        )

        layout.addWidget(
            self.text_color_button,
            5,
            1,
        )

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        return card

    # =========================================================
    # IDIOMA
    # =========================================================

    def _build_language_card(self):
        card = self._create_card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(9)

        title = QLabel("Idioma")
        title.setObjectName("sectionTitle")

        description = QLabel(
            "Selecciona el idioma que utilizará "
            "la aplicación."
        )
        description.setObjectName(
            "sectionDescription"
        )

        label = QLabel(
            "Idioma de la aplicación"
        )
        label.setObjectName("fieldLabel")

        self.language_combo = QComboBox()

        self.language_combo.addItem(
            "Español",
            "es",
        )

        self.language_combo.addItem(
            "Español (España)",
            "es-ES",
        )

        self.language_combo.addItem(
            "English",
            "en",
        )

        self.language_combo.addItem(
            "English (United States)",
            "en-US",
        )

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(label)
        layout.addWidget(
            self.language_combo
        )

        return card

    # =========================================================
    # PIE DE VENTANA
    # =========================================================

    def _build_footer(self, parent_layout):
        footer = QFrame()
        footer.setObjectName("settingsFooter")

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(
            30,
            14,
            30,
            18,
        )
        layout.setSpacing(10)

        reset_button = QPushButton(
            "Restablecer"
        )
        reset_button.setObjectName(
            "ghostButton"
        )
        reset_button.setCursor(
            Qt.PointingHandCursor
        )
        reset_button.clicked.connect(
            self._reset_defaults
        )

        cancel_button = QPushButton(
            "Cancelar"
        )
        cancel_button.setObjectName(
            "secondaryButton"
        )
        cancel_button.setCursor(
            Qt.PointingHandCursor
        )
        cancel_button.clicked.connect(
            self.reject
        )

        save_button = QPushButton(
            "Guardar cambios"
        )
        save_button.setObjectName(
            "primaryButton"
        )
        save_button.setCursor(
            Qt.PointingHandCursor
        )
        save_button.clicked.connect(
            self._save
        )

        layout.addWidget(reset_button)
        layout.addStretch()
        layout.addWidget(cancel_button)
        layout.addWidget(save_button)

        parent_layout.addWidget(footer)

    # =========================================================
    # CREAR TARJETAS
    # =========================================================

    def _create_card(self):
        card = QFrame()
        card.setObjectName("settingsCard")

        return card

    # =========================================================
    # CARGAR CONFIGURACIÓN
    # =========================================================

    def _load_config(
        self,
        config: UserConfig,
    ):
        self.name_input.setText(
            config.nombre_usuario
        )

        theme_index = (
            self.theme_combo.findData(
                config.tema_interfaz
            )
        )

        if theme_index >= 0:
            self.theme_combo.setCurrentIndex(
                theme_index
            )

        language_index = (
            self.language_combo.findData(
                config.idioma
            )
        )

        if language_index >= 0:
            self.language_combo.setCurrentIndex(
                language_index
            )

        self.font_size.setValue(
            config.tamano_fuente
        )

        self.profile_path = (
            config.foto_perfil
        )

        self._refresh_photo_text()
        self._refresh_color_buttons()

    # =========================================================
    # FOTO
    # =========================================================

    def _select_photo(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar fotografía",
            "",
            (
                "Imágenes "
                "(*.png *.jpg *.jpeg *.bmp *.webp)"
            ),
        )

        if path:
            self.profile_path = path
            self._refresh_photo_text()

    def _refresh_photo_text(self):
        if not self.profile_path:
            self.photo_path_label.setText(
                "Sin fotografía seleccionada"
            )
            self.photo_path_label.setToolTip("")
            return

        filename = Path(
            self.profile_path
        ).name

        self.photo_path_label.setText(
            filename
        )

        self.photo_path_label.setToolTip(
            self.profile_path
        )

    # =========================================================
    # SELECTOR DE COLORES
    # =========================================================

    def _open_color_dialog(
        self,
        current_color: str,
        title: str,
    ):
        dialog = QColorDialog(
            QColor(current_color),
            self,
        )

        dialog.setWindowTitle(title)

        # Evita utilizar el diálogo nativo de Windows
        # para poder controlar mejor sus colores.
        dialog.setOption(
            QColorDialog.DontUseNativeDialog,
            True,
        )
        
        dialog.setStyleSheet(
            build_color_dialog_stylesheet(
                self.current_config
            )
        )

        if dialog.exec() == QDialog.Accepted:
            return dialog.selectedColor()

        return None

    def _select_menu_color(self):
        color = self._open_color_dialog(
            self.menu_color,
            "Color de la barra de menú",
        )

        if (
            color is not None
            and color.isValid()
        ):
            self.menu_color = color.name()
            self._refresh_color_buttons()

    def _select_text_color(self):
        color = self._open_color_dialog(
            self.text_color,
            "Color de letra",
        )

        if (
            color is not None
            and color.isValid()
        ):
            self.text_color = color.name()
            self._refresh_color_buttons()

    def _refresh_color_buttons(self):
        self.menu_color_button.setText(
            f"●   {self.menu_color.upper()}"
        )

        self.text_color_button.setText(
            f"●   {self.text_color.upper()}"
        )

    # =========================================================
    # RESTABLECER VALORES
    # =========================================================

    def _reset_defaults(self):
        defaults = UserConfig()

        self.name_input.setText(
            defaults.nombre_usuario
        )

        theme_index = (
            self.theme_combo.findData(
                defaults.tema_interfaz
            )
        )

        if theme_index >= 0:
            self.theme_combo.setCurrentIndex(
                theme_index
            )

        language_index = (
            self.language_combo.findData(
                defaults.idioma
            )
        )

        if language_index >= 0:
            self.language_combo.setCurrentIndex(
                language_index
            )

        self.font_size.setValue(
            defaults.tamano_fuente
        )

        self.menu_color = (
            defaults.color_barra_menu
        )

        self.text_color = (
            defaults.color_letra
        )

        self.profile_path = ""

        self._refresh_photo_text()
        self._refresh_color_buttons()

    def _show_message(
        self,
        icon,
        title: str,
        message: str,
    ):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setModal(True)
        dialog.setFixedWidth(430)

        root = QVBoxLayout(dialog)
        root.setContentsMargins(24, 22, 24, 18)
        root.setSpacing(18)

        # Contenido principal
        content = QHBoxLayout()
        content.setSpacing(16)

        icon_label = QLabel()

        if icon == QMessageBox.Information:
            icon_label.setText("i")
            icon_label.setObjectName("infoIcon")

        elif icon == QMessageBox.Warning:
            icon_label.setText("!")
            icon_label.setObjectName("warningIcon")

        elif icon == QMessageBox.Critical:
            icon_label.setText("×")
            icon_label.setObjectName("errorIcon")

        else:
            icon_label.setText("i")
            icon_label.setObjectName("infoIcon")

        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedSize(40, 40)

        message_label = QLabel(message)
        message_label.setObjectName("messageText")
        message_label.setWordWrap(True)
        message_label.setAlignment(
            Qt.AlignVCenter | Qt.AlignLeft
        )

        content.addWidget(
            icon_label,
            0,
            Qt.AlignTop,
        )
        content.addWidget(
            message_label,
            1,
        )

        root.addLayout(content)

        # Botón
        buttons = QHBoxLayout()
        buttons.addStretch()

        accept_button = QPushButton("Aceptar")
        accept_button.setObjectName("messageButton")
        accept_button.setCursor(
            Qt.PointingHandCursor
        )
        accept_button.clicked.connect(
            dialog.accept
        )

        buttons.addWidget(accept_button)

        root.addLayout(buttons)

        dialog.setStyleSheet(
            build_message_stylesheet(
                self.updated_config
            )
        )

        dialog.adjustSize()
        dialog.exec()
    
    # =========================================================
    # GUARDAR
    # =========================================================

    def _save(self):
        nombre = (
            self.name_input.text().strip()
        )

        if not nombre:
            self._show_message(
                QMessageBox.Warning,
                "Datos incompletos",
                "El nombre de usuario no puede estar vacío.",
            )
            return

        new_config = UserConfig(
            nombre_usuario=nombre,
            tema_interfaz=(
                self.theme_combo.currentData()
            ),
            idioma=(
                self.language_combo.currentData()
            ),
            tamano_fuente=(
                self.font_size.value()
            ),
            color_barra_menu=(
                self.menu_color
            ),
            color_letra=(
                self.text_color
            ),
            foto_perfil=(
                self.profile_path
            ),
        )

        success, message = (
            self.config_manager.save_config(
                new_config
            )
        )

        if not success:
            self._show_message(
                QMessageBox.Critical,
                "No se pudo guardar",
                message,
            )
            return

        self.updated_config = new_config

        self._show_message(
            QMessageBox.Information,
            "Configuración",
            message,
        )

        self.accept()

    # =========================================================
    # ESTILOS
    # =========================================================

    def _apply_style(self):
        self.setStyleSheet(
            build_settings_stylesheet(
                self.current_config
            )
        )