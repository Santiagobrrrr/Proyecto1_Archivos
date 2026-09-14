import json
import os
from pathlib import Path

from app.core.user_config import UserConfig


class ConfigManager:
    """
    Gestiona la lectura y escritura segura de la
    configuración de usuario.
    """

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    DEFAULT_CONFIG_PATH = (
        PROJECT_ROOT / "data" / "config.json"
    )

    def __init__(self, config_path=None):
        if config_path is None:
            self.config_path = self.DEFAULT_CONFIG_PATH
        else:
            self.config_path = Path(config_path)

        self.temp_path = self.config_path.with_suffix(".tmp")
        self.backup_path = self.config_path.with_suffix(".bak")

    def load_config(self) -> tuple[UserConfig, str]:
        """
        Lee la configuración desde config.json.

        Si el archivo no existe, está corrupto o no puede
        leerse, la aplicación utiliza valores predeterminados.
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

    def save_config(
        self,
        config: UserConfig,
    ) -> tuple[bool, str]:
        """
        Guarda la configuración de forma segura.

        1. Escribe primero en config.tmp.
        2. Conserva config.json anterior como config.bak.
        3. Reemplaza config.json utilizando os.replace().
        """

        try:
            self.config_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._write_temp_file(config)

            if self.config_path.exists():
                self._create_backup()

            os.replace(
                self.temp_path,
                self.config_path,
            )

            return (
                True,
                "Configuración guardada correctamente",
            )

        except PermissionError:
            self._remove_temp_file()

            return (
                False,
                "No hay permisos para guardar la configuración",
            )

        except (TypeError, ValueError):
            self._remove_temp_file()

            return (
                False,
                "Los datos de configuración no son válidos",
            )

        except OSError:
            self._remove_temp_file()

            return (
                False,
                "Ocurrió un error al guardar la configuración",
            )

    def _write_temp_file(
        self,
        config: UserConfig,
    ) -> None:
        """
        Escribe la nueva configuración en un archivo temporal.
        """

        with open(
            self.temp_path,
            "w",
            encoding="utf-8",
        ) as archivo:
            json.dump(
                config.to_dict(),
                archivo,
                indent=4,
                ensure_ascii=False,
            )

            archivo.flush()
            os.fsync(archivo.fileno())

    def _create_backup(self) -> None:
        """
        Copia la configuración actual a config.bak.

        Se utilizan modos binarios para conservar exactamente
        el contenido del archivo original.
        """

        with open(
            self.config_path,
            "rb",
        ) as archivo_original:
            with open(
                self.backup_path,
                "wb",
            ) as archivo_backup:

                while True:
                    bloque = archivo_original.read(8192)

                    if not bloque:
                        break

                    archivo_backup.write(bloque)

                archivo_backup.flush()
                os.fsync(archivo_backup.fileno())

    def _remove_temp_file(self) -> None:
        """
        Elimina config.tmp si quedó creado después de un error.
        """

        try:
            if self.temp_path.exists():
                self.temp_path.unlink()

        except OSError:
            pass