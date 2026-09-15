TEXTS = {
    "es": {
        "app_subtitle": "Configuración de usuario",
        "menu_file": "Archivo",
        "menu_edit": "Edición",
        "menu_view": "Ver",
        "settings": "Settings",

        "new": "Nuevo",
        "open": "Abrir",
        "exit": "Salir",
        "undo": "Deshacer",
        "copy": "Copiar",
        "paste": "Pegar",
        "refresh": "Actualizar vista",
        "interface_info": "Información de interfaz",

        "status_ready": "Listo",
        "status_default": "Predeterminado",
        "status_invalid": "Configuración inválida",
        "status_no_access": "Sin acceso",
        "status_format": "Formato inválido",
        "status_error": "Error de configuración",

        "profile": "PERFIL DE USUARIO",
        "welcome": "Bienvenido, {name}",
        "profile_description": (
            "Personaliza la aplicación y conserva tus "
            "preferencias de forma segura entre sesiones."
        ),

        "theme_light": "Tema claro",
        "theme_dark": "Tema oscuro",

        "configure": "Configurar preferencias",
        "preview": "Vista previa",

        "persistence": "Persistencia",
        "persistence_description": (
            "Tus preferencias permanecerán disponibles "
            "cuando vuelvas a iniciar la aplicación."
        ),

        "personalization": "Personalización",
        "personalization_description": (
            "Tema, idioma, tipografía, colores y perfil "
            "en un único espacio de configuración."
        ),

        "protection": "Protección",
        "protection_description": (
            "La configuración contará con escritura segura, "
            "respaldo y manejo controlado de errores."
        ),

        "simulated_title": "Función simulada",
        "simulated_message": (
            "La opción «{action}» forma parte del menú "
            "simulado solicitado por el proyecto."
        ),
        
        "status_recovered": "Configuración recuperada",
    },

    "en": {
        "app_subtitle": "User configuration",
        "menu_file": "File",
        "menu_edit": "Edit",
        "menu_view": "View",
        "settings": "Settings",

        "new": "New",
        "open": "Open",
        "exit": "Exit",
        "undo": "Undo",
        "copy": "Copy",
        "paste": "Paste",
        "refresh": "Refresh view",
        "interface_info": "Interface information",

        "status_ready": "Ready",
        "status_default": "Default",
        "status_invalid": "Invalid configuration",
        "status_no_access": "No access",
        "status_format": "Invalid format",
        "status_error": "Configuration error",

        "profile": "USER PROFILE",
        "welcome": "Welcome, {name}",
        "profile_description": (
            "Customize the application and keep your "
            "preferences safely between sessions."
        ),

        "theme_light": "Light theme",
        "theme_dark": "Dark theme",

        "configure": "Configure preferences",
        "preview": "Preview",

        "persistence": "Persistence",
        "persistence_description": (
            "Your preferences will remain available "
            "when you start the application again."
        ),

        "personalization": "Personalization",
        "personalization_description": (
            "Theme, language, typography, colors and profile "
            "in a single configuration space."
        ),

        "protection": "Protection",
        "protection_description": (
            "The configuration uses safe writing, backups "
            "and controlled error handling."
        ),

        "simulated_title": "Simulated function",
        "simulated_message": (
            "The «{action}» option is part of the simulated "
            "menu requested by the project."
        ),
        
        "status_recovered": "Configuration recovered",
    },
}


def normalize_language(language: str) -> str:
    if str(language).lower().startswith("en"):
        return "en"

    return "es"


def text(language: str, key: str) -> str:
    lang = normalize_language(language)

    return TEXTS.get(
        lang,
        TEXTS["es"],
    ).get(
        key,
        TEXTS["es"].get(key, key),
    )