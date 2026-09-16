from PySide6.QtGui import QColor

from app.core.user_config import UserConfig


LIGHT = {
    "background": "#F3F5F2",
    "surface": "#FCFCFA",
    "surface_alt": "#F0F3F1",
    "text": "#202824",
    "muted": "#68736D",
    "border": "#DCE3DF",
    "border_strong": "#C8D3CE",
    "accent": "#3F7469",
    "accent_hover": "#35655C",
    "accent_pressed": "#2B554D",
    "button_text": "#F8FBF9",
    "soft_accent": "#E4EFEB",
    "soft_text": "#35655C",
    "status_bg": "#E7F2EC",
    "status_text": "#356849",
    "info_bg": "#EAF0F5",
    "info_text": "#48606F",
    "recovered_bg": "#E9F0E4",
    "recovered_text": "#4A6842",
    "warning_bg": "#F6EFD9",
    "warning_text": "#745B16",
    "danger_bg": "#F5E4E4",
    "danger_text": "#8A3F3F",
    "scroll": "#C9D4CF",
}


DARK = {
    "background": "#131816",
    "surface": "#1B221F",
    "surface_alt": "#222B27",
    "text": "#E8EEEB",
    "muted": "#A6B1AB",
    "border": "#313C37",
    "border_strong": "#45534D",
    "accent": "#6F9F94",
    "accent_hover": "#7FADA3",
    "accent_pressed": "#5E8B81",
    "button_text": "#101613",
    "soft_accent": "#243A34",
    "soft_text": "#A4D3C7",
    "status_bg": "#1F352A",
    "status_text": "#8BCDA4",
    "info_bg": "#243139",
    "info_text": "#A8C1CE",
    "recovered_bg": "#263527",
    "recovered_text": "#A8CAA0",
    "warning_bg": "#40351E",
    "warning_text": "#E4C46F",
    "danger_bg": "#402626",
    "danger_text": "#E4A0A0",
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
        "greeting": min(35, base + 12),
        "card_title": min(21, base + 3),
        "nav_bg": nav_bg,
        "nav_fg": nav_fg,
        "nav_hover": _variant(nav_bg, 108),
        "nav_pressed": _variant(nav_bg, 116),
        "nav_border": _variant(nav_bg, 112),
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
            border-radius: 20px;
        }

        QLabel#appName {
            color: %(text)s;
            font-size: %(app_name)dpx;
            font-weight: 700;
        }

        QLabel#appSubtitle {
            color: %(muted)s;
            font-size: %(tiny)dpx;
        }

        QFrame#navigationBar {
            background-color: %(nav_bg)s;
            border: 1px solid %(nav_border)s;
            border-radius: 13px;
        }

        QToolButton#menuButton {
            background-color: transparent;
            color: %(nav_fg)s;
            border: 1px solid transparent;
            border-radius: 9px;
            padding: 8px 14px;
            font-size: %(small)dpx;
            font-weight: 600;
        }

        QToolButton#menuButton:hover {
            background-color: %(nav_hover)s;
        }

        QToolButton#menuButton:pressed {
            background-color: %(nav_pressed)s;
        }

        QToolButton#menuButton:focus {
            border: 1px solid %(nav_fg)s;
        }

        QLabel#statusBadge {
            background-color: %(status_bg)s;
            color: %(status_text)s;
            border: 1px solid %(border)s;
            border-radius: 12px;
            padding: 7px 10px;
            font-size: %(tiny)dpx;
            font-weight: 600;
        }

        QLabel#statusBadge[state="info"] {
            background-color: %(info_bg)s;
            color: %(info_text)s;
        }

        QLabel#statusBadge[state="recovered"] {
            background-color: %(recovered_bg)s;
            color: %(recovered_text)s;
        }

        QLabel#statusBadge[state="warning"] {
            background-color: %(warning_bg)s;
            color: %(warning_text)s;
        }

        QLabel#statusBadge[state="error"] {
            background-color: %(danger_bg)s;
            color: %(danger_text)s;
        }

        QPushButton#settingsMenuButton,
        QPushButton#primaryButton {
            background-color: %(accent)s;
            color: %(button_text)s;
            border: 1px solid %(accent)s;
            border-radius: 11px;
            padding: 10px 16px;
            font-size: %(small)dpx;
            font-weight: 600;
        }

        QPushButton#settingsMenuButton:hover,
        QPushButton#primaryButton:hover {
            background-color: %(accent_hover)s;
            border-color: %(accent_hover)s;
        }

        QPushButton#settingsMenuButton:pressed,
        QPushButton#primaryButton:pressed {
            background-color: %(accent_pressed)s;
            border-color: %(accent_pressed)s;
        }

        QPushButton#settingsMenuButton:focus,
        QPushButton#primaryButton:focus {
            border: 1px solid %(soft_text)s;
        }

        QFrame#profileCard {
            background-color: %(surface)s;
            border: 1px solid %(border)s;
            border-radius: 26px;
        }

        QLabel#avatar {
            background-color: %(soft_accent)s;
            color: %(soft_text)s;
            border: 3px solid %(accent)s;
            border-radius: 52px;
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

        QLabel#preferenceChip {
            background-color: %(surface_alt)s;
            color: %(text)s;
            border: 1px solid %(border)s;
            border-radius: 10px;
            padding: 6px 10px;
            font-size: %(tiny)dpx;
            font-weight: 600;
        }

        QPushButton#secondaryButton {
            background-color: %(surface_alt)s;
            color: %(text)s;
            border: 1px solid %(border)s;
            border-radius: 11px;
            padding: 10px 16px;
            font-size: %(small)dpx;
            font-weight: 600;
        }

        QPushButton#secondaryButton:hover {
            background-color: %(soft_accent)s;
            border-color: %(border_strong)s;
        }

        QPushButton#secondaryButton:pressed {
            background-color: %(surface_alt)s;
        }

        QPushButton#secondaryButton:focus {
            border: 1px solid %(accent)s;
        }

        QFrame#infoCard {
            background-color: %(surface)s;
            border: 1px solid %(border)s;
            border-radius: 18px;
        }

        QFrame#infoCard:hover {
            border-color: %(border_strong)s;
        }

        QLabel#cardNumber {
            background-color: %(soft_accent)s;
            color: %(soft_text)s;
            border: 1px solid %(border)s;
            border-radius: 17px;
            font-size: %(tiny)dpx;
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
            border-radius: 10px;
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

        QToolTip {
            background-color: %(surface)s;
            color: %(text)s;
            border: 1px solid %(border)s;
            padding: 6px 8px;
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
            border-radius: 18px;
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

        QLineEdit:hover,
        QComboBox:hover,
        QSpinBox:hover {
            border-color: %(border_strong)s;
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
            border-color: %(border_strong)s;
        }

        QPushButton#compactButton:focus,
        QPushButton#secondaryButton:focus,
        QPushButton#colorButton:focus {
            border: 1px solid %(accent)s;
        }

        QPushButton#colorButton {
            text-align: left;
        }

        QPushButton#primaryButton {
            background-color: %(accent)s;
            color: %(button_text)s;
            border: 1px solid %(accent)s;
            border-radius: 10px;
            padding: 11px 18px;
            font-weight: 600;
        }

        QPushButton#primaryButton:hover {
            background-color: %(accent_hover)s;
            border-color: %(accent_hover)s;
        }

        QPushButton#primaryButton:pressed {
            background-color: %(accent_pressed)s;
            border-color: %(accent_pressed)s;
        }

        QPushButton#ghostButton {
            background-color: transparent;
            color: %(muted)s;
            border: 1px solid transparent;
            border-radius: 9px;
            padding: 10px 14px;
            font-weight: 600;
        }

        QPushButton#ghostButton:hover {
            background-color: %(surface_alt)s;
            color: %(text)s;
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

        QToolTip {
            background-color: %(surface)s;
            color: %(text)s;
            border: 1px solid %(border)s;
            padding: 6px 8px;
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
            background-color: %(warning_bg)s;
            color: %(warning_text)s;
            border-radius: 20px;
            font-size: 22px;
            font-weight: 700;
        }

        QLabel#errorIcon {
            background-color: %(danger_bg)s;
            color: %(danger_text)s;
            border-radius: 20px;
            font-size: 22px;
            font-weight: 700;
        }

        QPushButton#messageButton {
            background-color: %(accent)s;
            color: %(button_text)s;
            border: 1px solid %(accent)s;
            border-radius: 9px;
            padding: 9px 20px;
            min-width: 80px;
            font-weight: 600;
        }

        QPushButton#messageButton:hover {
            background-color: %(accent_hover)s;
            border-color: %(accent_hover)s;
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

        QColorDialog QPushButton:hover {
            background-color: %(soft_accent)s;
            border-color: %(border_strong)s;
        }

        QColorDialog QPushButton:default {
            background-color: %(accent)s;
            color: %(button_text)s;
            border: 1px solid %(accent)s;
        }
    """ % p