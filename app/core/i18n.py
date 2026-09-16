TEXTS = {
    "es": {
        # =====================================================
        # APLICACIÓN
        # =====================================================

        "app_subtitle": "Configuración de usuario",

        # =====================================================
        # MENÚ PRINCIPAL
        # =====================================================

        "menu_file": "Archivo",
        "menu_edit": "Edición",
        "menu_view": "Ver",
        "settings": "Settings",

        # Archivo
        "new": "Nuevo",
        "open": "Abrir",
        "exit": "Salir",

        # Edición
        "undo": "Deshacer",
        "copy": "Copiar",
        "paste": "Pegar",

        # Ver
        "refresh": "Actualizar vista",
        "interface_info": "Información de interfaz",

        # =====================================================
        # ESTADO
        # =====================================================

        "status_ready": "Listo",
        "status_default": "Predeterminado",
        "status_invalid": "Configuración inválida",
        "status_no_access": "Sin acceso",
        "status_format": "Formato inválido",
        "status_error": "Error de configuración",
        "status_recovered": "Configuración recuperada",

        # =====================================================
        # PERFIL
        # =====================================================

        "profile": "PERFIL DE USUARIO",

        "welcome": "Bienvenido, {name}",

        "profile_description": (
            "Personaliza la aplicación y conserva tus "
            "preferencias de forma segura entre sesiones."
        ),

        "theme_light": "Tema claro",
        "theme_dark": "Tema oscuro",

        "configure": "Configurar preferencias",

        # =====================================================
        # MENSAJES DE MENÚ
        # =====================================================

        "msg_new": (
            "Puedes comenzar modificando las "
            "preferencias desde Settings."
        ),

        "msg_open": (
            "La configuración actual ya está cargada."
        ),

        "msg_undo": (
            "No hay cambios disponibles para deshacer."
        ),

        "msg_copy": (
            "No hay contenido seleccionado para copiar."
        ),

        "msg_paste": (
            "No hay contenido disponible para pegar."
        ),

        "msg_refresh": (
            "La interfaz ya se encuentra actualizada."
        ),

        "msg_interface_info": (
            "Aplicación de configuración de usuario "
            "desarrollada con Python y PySide6."
        ),
    },

    "en": {
        # =====================================================
        # APPLICATION
        # =====================================================

        "app_subtitle": "User configuration",

        # =====================================================
        # MAIN MENU
        # =====================================================

        "menu_file": "File",
        "menu_edit": "Edit",
        "menu_view": "View",
        "settings": "Settings",

        # File
        "new": "New",
        "open": "Open",
        "exit": "Exit",

        # Edit
        "undo": "Undo",
        "copy": "Copy",
        "paste": "Paste",

        # View
        "refresh": "Refresh view",
        "interface_info": "Interface information",

        # =====================================================
        # STATUS
        # =====================================================

        "status_ready": "Ready",
        "status_default": "Default",
        "status_invalid": "Invalid configuration",
        "status_no_access": "No access",
        "status_format": "Invalid format",
        "status_error": "Configuration error",
        "status_recovered": "Configuration recovered",

        # =====================================================
        # PROFILE
        # =====================================================

        "profile": "USER PROFILE",

        "welcome": "Welcome, {name}",

        "profile_description": (
            "Customize the application and keep your "
            "preferences safely between sessions."
        ),

        "theme_light": "Light theme",
        "theme_dark": "Dark theme",

        "configure": "Configure preferences",

        # =====================================================
        # MENU MESSAGES
        # =====================================================

        "msg_new": (
            "You can start by changing your "
            "preferences in Settings."
        ),

        "msg_open": (
            "The current configuration is already loaded."
        ),

        "msg_undo": (
            "There are no changes available to undo."
        ),

        "msg_copy": (
            "There is no selected content to copy."
        ),

        "msg_paste": (
            "There is no content available to paste."
        ),

        "msg_refresh": (
            "The interface is already up to date."
        ),

        "msg_interface_info": (
            "User configuration application developed "
            "with Python and PySide6."
        ),
    },
}


def normalize_language(
    language: str,
) -> str:
    if (
        str(language)
        .lower()
        .startswith("en")
    ):
        return "en"

    return "es"


def text(
    language: str,
    key: str,
) -> str:
    lang = normalize_language(
        language
    )

    return TEXTS.get(
        lang,
        TEXTS["es"],
    ).get(
        key,
        TEXTS["es"].get(
            key,
            key,
        ),
    )