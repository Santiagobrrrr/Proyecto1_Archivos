import json
from pathlib import Path

from app.core.user_config import UserConfig


class ConfigManager:
    """
    Se encarga de leer la configuración de usuario
    almacenada en un archivo JSON.
    """

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    DEFAULT_CONFIG_PATH = PROJECT_ROOT / "data" / "config.json"

    def __init__(self, config_path=None):
        if config_path is None:
            self.config_path = self.DEFAULT_CONFIG_PATH
        else:
            self.config_path = Path(config_path)

    def load_config(self) -> tuple[UserConfig, str]:
        """
        Lee la configuración desde config.json.

        Si el archivo no existe, está corrupto o no puede
        leerse por falta de permisos, se utilizan valores
        predeterminados para evitar que la aplicación falle.
        """

        try:
            with open(
                self.config_path,
                "r",
                encoding="utf-8",
            ) as archivo:
                data = json.load(archivo)

            if not isinstance(data, dict):
                raise ValueError(
                    "La raíz del archivo JSON debe ser un objeto."
                )

            config = UserConfig.from_dict(data)

            return config, "Configuración cargada"

        except FileNotFoundError:
            return (
                UserConfig(),
                "Valores predeterminados",
            )

        except json.JSONDecodeError:
            return (
                UserConfig(),
                "Configuración inválida",
            )

        except PermissionError:
            return (
                UserConfig(),
                "Sin permiso de lectura",
            )

        except ValueError:
            return (
                UserConfig(),
                "Formato no válido",
            )

        except OSError:
            return (
                UserConfig(),
                "Error al leer configuración",
            )