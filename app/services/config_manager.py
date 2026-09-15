import json
import os
import re
from pathlib import Path

from app.core.user_config import UserConfig


class ConfigManager:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    DEFAULT_CONFIG_PATH = (
        PROJECT_ROOT
        / "data"
        / "config.json"
    )

    def __init__(self, config_path=None):
        if config_path is None:
            self.config_path = (
                self.DEFAULT_CONFIG_PATH
            )
        else:
            self.config_path = Path(
                config_path
            )

        self.temp_path = (
            self.config_path.with_suffix(
                ".tmp"
            )
        )

        self.backup_path = (
            self.config_path.with_suffix(
                ".bak"
            )
        )

    # =========================================================
    # CARGAR CONFIGURACIÓN
    # =========================================================

    def load_config(
        self,
    ) -> tuple[UserConfig, str]:
        """
        Carga config.json.

        Si el archivo está corrupto o tiene un formato
        inválido, intenta recuperar config.bak.
        """

        # Si quedó un temporal de una ejecución
        # interrumpida, lo eliminamos.
        self._remove_temp_file()

        try:
            config = self._read_config_file(
                self.config_path
            )

            return (
                config,
                "Configuración cargada",
            )

        except FileNotFoundError:
            return (
                UserConfig(),
                "Valores predeterminados",
            )

        except PermissionError:
            return (
                UserConfig(),
                "Sin permiso de lectura",
            )

        except (
            json.JSONDecodeError,
            ValueError,
            TypeError,
        ):
            recovered = (
                self._recover_from_backup()
            )

            if recovered is not None:
                return (
                    recovered,
                    "Configuración recuperada",
                )

            return (
                UserConfig(),
                "Configuración inválida",
            )

        except OSError:
            return (
                UserConfig(),
                "Error al leer configuración",
            )

    # =========================================================
    # GUARDAR CONFIGURACIÓN
    # =========================================================

    def save_config(
        self,
        config: UserConfig,
    ) -> tuple[bool, str]:
        """
        Guarda primero en config.tmp.

        Si config.json actual es válido, crea antes
        config.bak.

        Finalmente reemplaza config.json usando
        os.replace().
        """

        try:
            self.config_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            # Primero escribimos el temporal.
            self._write_temp_file(config)

            # Si existe un archivo anterior válido,
            # hacemos una copia de respaldo.
            if self.config_path.exists():
                self._backup_current_if_valid()

            # Reemplazo seguro.
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
                (
                    "No hay permisos para guardar "
                    "la configuración"
                ),
            )

        except (
            TypeError,
            ValueError,
        ):
            self._remove_temp_file()

            return (
                False,
                (
                    "Los datos de configuración "
                    "no son válidos"
                ),
            )

        except OSError:
            self._remove_temp_file()

            return (
                False,
                (
                    "Ocurrió un error al guardar "
                    "la configuración"
                ),
            )

    # =========================================================
    # LEER ARCHIVO JSON
    # =========================================================

    def _read_config_file(
        self,
        path: Path,
    ) -> UserConfig:
        with open(
            path,
            "r",
            encoding="utf-8",
        ) as archivo:
            data = json.load(archivo)

        self._validate_data(data)

        return UserConfig.from_dict(data)

    # =========================================================
    # VALIDAR FORMATO
    # =========================================================

    def _validate_data(
        self,
        data: dict,
    ):
        if not isinstance(data, dict):
            raise ValueError(
                "La raíz del JSON debe ser un objeto."
            )

        if (
            "nombre_usuario" in data
            and not isinstance(
                data["nombre_usuario"],
                str,
            )
        ):
            raise ValueError(
                "nombre_usuario no es válido."
            )

        if "tema_interfaz" in data:
            if data["tema_interfaz"] not in (
                "claro",
                "oscuro",
            ):
                raise ValueError(
                    "tema_interfaz no es válido."
                )

        if "idioma" in data:
            if data["idioma"] not in (
                "es",
                "es-ES",
                "en",
                "en-US",
            ):
                raise ValueError(
                    "idioma no es válido."
                )

        if "tamaño_fuente" in data:
            if not isinstance(
                data["tamaño_fuente"],
                int,
            ):
                raise ValueError(
                    "tamaño_fuente no es válido."
                )

        if "foto_perfil" in data:
            if not isinstance(
                data["foto_perfil"],
                str,
            ):
                raise ValueError(
                    "foto_perfil no es válido."
                )

        for field in (
            "color_barra_menu",
            "color_letra",
        ):
            if field in data:
                value = data[field]

                if not isinstance(
                    value,
                    str,
                ):
                    raise ValueError(
                        f"{field} no es válido."
                    )

                if not re.fullmatch(
                    r"#[0-9A-Fa-f]{6}",
                    value,
                ):
                    raise ValueError(
                        f"{field} no es válido."
                    )

    # =========================================================
    # ARCHIVO TEMPORAL
    # =========================================================

    def _write_temp_file(
        self,
        config: UserConfig,
    ):
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
            os.fsync(
                archivo.fileno()
            )

    # =========================================================
    # RESPALDO
    # =========================================================

    def _backup_current_if_valid(self):
        """
        Solo sobrescribe config.bak cuando el
        config.json actual es válido.

        De esta manera un JSON corrupto no destruye
        un respaldo bueno.
        """

        try:
            self._read_config_file(
                self.config_path
            )

        except FileNotFoundError:
            return

        except (
            json.JSONDecodeError,
            ValueError,
            TypeError,
        ):
            # El archivo actual está corrupto.
            # Conservamos el backup existente.
            return

        # PermissionError y otros OSError no se
        # ignoran: subirán hasta save_config().
        self._create_backup()

    def _create_backup(self):
        """
        Copia config.json a config.bak utilizando
        lectura y escritura binaria.
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
                    bloque = (
                        archivo_original.read(
                            8192
                        )
                    )

                    if not bloque:
                        break

                    archivo_backup.write(
                        bloque
                    )

                archivo_backup.flush()
                os.fsync(
                    archivo_backup.fileno()
                )

    # =========================================================
    # RECUPERACIÓN
    # =========================================================

    def _recover_from_backup(
        self,
    ) -> UserConfig | None:
        """
        Intenta leer config.bak.

        Si es válido, también reconstruye config.json
        mediante el archivo temporal.
        """

        try:
            recovered_config = (
                self._read_config_file(
                    self.backup_path
                )
            )

        except (
            FileNotFoundError,
            PermissionError,
            json.JSONDecodeError,
            ValueError,
            TypeError,
            OSError,
        ):
            return None

        try:
            # Reconstruimos config.json de forma
            # segura sin modificar el backup.
            self._write_temp_file(
                recovered_config
            )

            os.replace(
                self.temp_path,
                self.config_path,
            )

        except (
            PermissionError,
            OSError,
        ):
            # Aunque no podamos reconstruir el archivo,
            # todavía podemos usar el backup en memoria.
            self._remove_temp_file()

        return recovered_config

    # =========================================================
    # LIMPIAR TEMPORAL
    # =========================================================

    def _remove_temp_file(self):
        try:
            if self.temp_path.exists():
                self.temp_path.unlink()

        except OSError:
            pass