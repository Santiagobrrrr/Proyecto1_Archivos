from PySide6.QtGui import QColor

from app.core.user_config import UserConfig


LIGHT = {
    "background": "#F3F5F2",
    "surface": "#FCFCFA",
    "surface_alt": "#F0F3F1",
    "text": "#202824",
    "muted": "#68736D",
    "border": "#DCE3DF",
    "accent": "#3F7469",
    "accent_hover": "#35655C",
    "accent_pressed": "#2B554D",
    "button_text": "#F8FBF9",
    "soft_accent": "#E4EFEB",
    "soft_text": "#35655C",
    "status": "#356849",
    "scroll": "#C9D4CF",
}


DARK = {
    "background": "#131816",
    "surface": "#1B221F",
    "surface_alt": "#222B27",
    "text": "#E8EEEB",
    "muted": "#A6B1AB",
    "border": "#313C37",
    "accent": "#6F9F94",
    "accent_hover": "#7FADA3",
    "accent_pressed": "#5E8B81",
    "button_text": "#101613",
    "soft_accent": "#243A34",
    "soft_text": "#A4D3C7",
    "status": "#8BCDA4",
    "scroll": "#53615B",
}


def _palette(config: UserConfig) -> dict:
    if config.tema_interfaz == "oscuro":
        return DARK

    return LIGHT


def _safe_color(value: str, fallback: str) -> str:
    color = QColor(value)

    if not color.isValid():
        return fallback

    return color.name().upper()


def _variant(value: str, amount: int) -> str:
    color = QColor(value)

    if not color.isValid():
        return value

    brightness = (
        color.red() * 299
        + color.green() * 587
        + color.blue() * 114
    ) / 1000

    if brightness >= 145:
        return color.darker(amount).name()

    return color.lighter(amount).name()


def effective_font_size(value: int) -> int:
    """
    Evita tamaños que destruyan la composición visual,
    manteniendo un rango accesible y perceptible.
    """
    return max(10, min(int(value), 20))


def build_main_stylesheet(config: UserConfig) -> str:
    p = _palette(config)

    base = effective_font_size(
        config.tamano_fuente
    )

    nav_bg = _safe_color(
        config.color_barra_menu,
        p["accent"],
    )

    nav_fg = _safe_color(
        config.color_letra,
        p["button_text"],
    )

    values = {
        **p,
        "base": base,
        "small": max(10, base - 2),
        "tiny": max(9, base - 3),
        "app_name": min(28, base + 7),
        "greeting": min(36, base + 13),
        "card_title": min(22, base + 3),
        "nav_bg": nav_bg,
        "nav_fg": nav_fg,
        "nav_hover": _variant(nav_bg, 108),
        "nav_pressed": _variant(nav_bg, 116),
    }

    return """
        QWidget#centralWidget {
            background-color: %(background)s;
            color: %(text)s;
            font-size: %(base)dpx;
        }

        QFrame#headerCard {
            background-color: %(surface)s;
            border: 1px solid %(border)s;
            border-radius: 18px;
        }

        QLabel#appName {
            color: %(text)s;
            font-size: %(app_name)dpx;
            font-weight: 700;
        }

        QLabel#appSubtitle {
            color: %(muted)s;
            font-size: %(small)dpx;
        }

        QFrame#navigationBar {
            background-color: %(nav_bg)s;
            border: 1px solid %(nav_bg)s;
            border-radius: 12px;
        }

        QToolButton#menuButton {
            background-color: transparent;
            color: %(nav_fg)s;
            border: none;
            border-radius: 8px;
            padding: 8px 13px;
            font-size: %(small)dpx;
            font-weight: 600;
        }

        QToolButton#menuButton:hover {
            background-color: %(nav_hover)s;
        }

        QToolButton#menuButton:pressed {
            background-color: %(nav_pressed)s;
        }

        QLabel#statusBadge {
            background-color: transparent;
            color: %(status)s;
            border: none;
            padding: 7px 5px;
            font-size: %(tiny)dpx;
            font-weight: 600;
        }

        QPushButton#settingsMenuButton,
        QPushButton#primaryButton {
            background-color: %(accent)s;
            color: %(button_text)s;
            border: none;
            border-radius: 10px;
            padding: 10px 16px;
            font-size: %(small)dpx;
            font-weight: 600;
        }

        QPushButton#settingsMenuButton:hover,
        QPushButton#primaryButton:hover {
            background-color: %(accent_hover)s;
        }

        QPushButton#settingsMenuButton:pressed,
        QPushButton#primaryButton:pressed {
            background-color: %(accent_pressed)s;
        }

        QFrame#profileCard {
            background-color: %(surface)s;
            border: 1px solid %(border)s;
            border-radius: 24px;
        }

        QLabel#avatar {
            background-color: %(soft_accent)s;
            color: %(soft_text)s;
            border: 1px solid %(border)s;
            border-radius: 46px;
            font-size: %(card_title)dpx;
            font-weight: 700;
        }

        QLabel#eyebrow {
            color: %(accent)s;
            font-size: %(tiny)dpx;
            font-weight: 700;
        }

        QLabel#greeting {
            color: %(text)s;
            font-size: %(greeting)dpx;
            font-weight: 700;
        }

        QLabel#description {
            color: %(muted)s;
            font-size: %(small)dpx;
        }

        QLabel#preferences {
            color: %(accent)s;
            font-size: %(small)dpx;
            font-weight: 600;
        }

        QPushButton#secondaryButton {
            background-color: %(surface_alt)s;
            color: %(text)s;
            border: 1px solid %(border)s;
            border-radius: 10px;
            padding: 10px 16px;
            font-size: %(small)dpx;
            font-weight: 600;
        }

        QPushButton#secondaryButton:hover {
            background-color: %(soft_accent)s;
        }

        QFrame#infoCard {
            background-color: %(surface)s;
            border: 1px solid %(border)s;
            border-radius: 18px;
        }

        QLabel#cardNumber {
            color: %(accent)s;
            font-size: %(small)dpx;
            font-weight: 700;
        }

        QLabel#cardTitle {
            color: %(text)s;
            font-size: %(card_title)dpx;
            font-weight: 700;
        }

        QLabel#cardDescription {
            color: %(muted)s;
            font-size: %(small)dpx;
        }

        QMenu {
            background-color: %(surface)s;
            color: %(text)s;
            border: 1px solid %(border)s;
            padding: 5px;
            font-size: %(small)dpx;
        }

        QMenu::item {
            background-color: transparent;
            padding: 9px 26px 9px 12px;
            border-radius: 7px;
            margin: 1px;
        }

        QMenu::item:selected {
            background-color: %(soft_accent)s;
            color: %(soft_text)s;
        }

        QMenu::separator {
            height: 1px;
            background-color: %(border)s;
            margin: 5px 7px;
        }
    """ % values


def build_settings_stylesheet(
    config: UserConfig,
) -> str:
    p = _palette(config)

    base = effective_font_size(
        config.tamano_fuente
    )

    values = {
        **p,
        "base": base,
        "small": max(10, base - 2),
        "title": min(32, base + 10),
        "section": min(23, base + 4),
    }

    return """
        QDialog {
            background-color: %(background)s;
            color: %(text)s;
            font-size: %(base)dpx;
        }

        QFrame#settingsHeader,
        QWidget#settingsContent,
        QScrollArea#settingsScroll,
        QFrame#settingsFooter {
            background-color: %(background)s;
            border: none;
        }

        QFrame#settingsFooter {
            border-top: 1px solid %(border)s;
        }

        QLabel#settingsTitle {
            color: %(text)s;
            font-size: %(title)dpx;
            font-weight: 700;
        }

        QLabel#settingsSubtitle,
        QLabel#sectionDescription,
        QLabel#pathLabel {
            color: %(muted)s;
            font-size: %(small)dpx;
        }

        QFrame#settingsCard {
            background-color: %(surface)s;
            border: 1px solid %(border)s;
            border-radius: 16px;
        }

        QLabel#sectionTitle {
            color: %(text)s;
            font-size: %(section)dpx;
            font-weight: 700;
        }

        QLabel#fieldLabel {
            color: %(text)s;
            font-size: %(small)dpx;
            font-weight: 600;
        }

        QLineEdit,
        QComboBox,
        QSpinBox {
            background-color: %(surface_alt)s;
            color: %(text)s;
            border: 1px solid %(border)s;
            border-radius: 10px;
            padding: 9px 11px;
            min-height: 22px;
            font-size: %(small)dpx;
        }

        QLineEdit:focus,
        QComboBox:focus,
        QSpinBox:focus {
            border: 1px solid %(accent)s;
        }

        QComboBox QAbstractItemView {
            background-color: %(surface)s;
            color: %(text)s;
            border: 1px solid %(border)s;
            selection-background-color: %(soft_accent)s;
            selection-color: %(soft_text)s;
            outline: 0;
            padding: 5px;
        }

        QFrame#photoField {
            background-color: %(surface_alt)s;
            border: 1px solid %(border)s;
            border-radius: 10px;
            min-height: 40px;
        }

        QPushButton#compactButton,
        QPushButton#secondaryButton,
        QPushButton#colorButton {
            background-color: %(surface_alt)s;
            color: %(text)s;
            border: 1px solid %(border)s;
            border-radius: 9px;
            padding: 9px 14px;
            font-weight: 600;
        }

        QPushButton#compactButton:hover,
        QPushButton#secondaryButton:hover,
        QPushButton#colorButton:hover {
            background-color: %(soft_accent)s;
        }

        QPushButton#colorButton {
            text-align: left;
        }

        QPushButton#primaryButton {
            background-color: %(accent)s;
            color: %(button_text)s;
            border: none;
            border-radius: 10px;
            padding: 11px 18px;
            font-weight: 600;
        }

        QPushButton#primaryButton:hover {
            background-color: %(accent_hover)s;
        }

        QPushButton#ghostButton {
            background-color: transparent;
            color: %(muted)s;
            border: none;
            border-radius: 9px;
            padding: 10px 14px;
            font-weight: 600;
        }

        QPushButton#ghostButton:hover {
            background-color: %(surface_alt)s;
        }

        QScrollBar:vertical {
            background: transparent;
            width: 8px;
        }

        QScrollBar::handle:vertical {
            background: %(scroll)s;
            border-radius: 4px;
            min-height: 35px;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0;
        }
    """ % values


def build_message_stylesheet(
    config: UserConfig,
) -> str:
    p = _palette(config)

    return """
        QDialog {
            background-color: %(background)s;
        }

        QLabel#messageText {
            color: %(text)s;
            font-size: 13px;
        }

        QLabel#infoIcon {
            background-color: %(soft_accent)s;
            color: %(soft_text)s;
            border-radius: 20px;
            font-size: 20px;
            font-weight: 700;
        }

        QLabel#warningIcon {
            background-color: #5A4720;
            color: #F4D488;
            border-radius: 20px;
            font-size: 22px;
            font-weight: 700;
        }

        QLabel#errorIcon {
            background-color: #512A2A;
            color: #F0A0A0;
            border-radius: 20px;
            font-size: 22px;
            font-weight: 700;
        }

        QPushButton#messageButton {
            background-color: %(accent)s;
            color: %(button_text)s;
            border: none;
            border-radius: 9px;
            padding: 9px 20px;
            min-width: 80px;
            font-weight: 600;
        }
    """ % p


def build_color_dialog_stylesheet(
    config: UserConfig,
) -> str:
    p = _palette(config)

    return """
        QColorDialog {
            background-color: %(background)s;
            color: %(text)s;
        }

        QColorDialog QLabel {
            color: %(text)s;
        }

        QColorDialog QLineEdit,
        QColorDialog QSpinBox {
            background-color: %(surface)s;
            color: %(text)s;
            border: 1px solid %(border)s;
            border-radius: 8px;
            padding: 6px;
        }

        QColorDialog QPushButton {
            background-color: %(surface_alt)s;
            color: %(text)s;
            border: 1px solid %(border)s;
            border-radius: 8px;
            padding: 8px 14px;
        }

        QColorDialog QPushButton:default {
            background-color: %(accent)s;
            color: %(button_text)s;
            border: none;
        }
    """ % p