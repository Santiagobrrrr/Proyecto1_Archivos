from pathlib import Path
from uuid import uuid4


class ProfileManager:
    """
    Gestiona la copia y localización de fotografías
    de perfil utilizando archivos binarios.
    """

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    PROFILES_DIR = PROJECT_ROOT / "data" / "profiles"

    ALLOWED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".webp",
    }

    def __init__(self):
        self.PROFILES_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save_profile_image(
        self,
        source_path: str,
    ) -> str:
        """
        Copia una fotografía al directorio interno del
        proyecto usando lectura y escritura binaria.

        Devuelve una ruta relativa para almacenarla
        dentro de config.json.
        """

        if not source_path:
            return ""

        source = Path(source_path)

        # Si ya se trata de una ruta interna del proyecto,
        # no necesitamos volver a copiarla.
        resolved_existing = self.resolve_profile_path(
            source_path
        )

        if (
            resolved_existing is not None
            and resolved_existing.exists()
            and self._is_inside_profiles(
                resolved_existing
            )
        ):
            return self._to_relative_path(
                resolved_existing
            )

        if not source.exists():
            raise FileNotFoundError(
                "La fotografía seleccionada no existe."
            )

        extension = source.suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(
                "El formato de imagen no es compatible."
            )

        filename = (
            f"profile_{uuid4().hex[:10]}"
            f"{extension}"
        )

        destination = (
            self.PROFILES_DIR / filename
        )

        # Lectura binaria del archivo original.
        with open(source, "rb") as original:
            # Escritura binaria de la copia interna.
            with open(destination, "wb") as copy:
                while True:
                    block = original.read(8192)

                    if not block:
                        break

                    copy.write(block)

        return self._to_relative_path(
            destination
        )

    def resolve_profile_path(
        self,
        stored_path: str,
    ) -> Path | None:
        """
        Convierte la ruta almacenada en config.json
        en una ruta absoluta utilizable por la aplicación.
        """

        if not stored_path:
            return None

        path = Path(stored_path)

        if path.is_absolute():
            return path

        return self.PROJECT_ROOT / path

    def _to_relative_path(
        self,
        path: Path,
    ) -> str:
        """
        Convierte una ruta absoluta en una ruta relativa
        al proyecto para hacer la configuración portable.
        """

        try:
            relative = path.resolve().relative_to(
                self.PROJECT_ROOT.resolve()
            )

            return relative.as_posix()

        except ValueError:
            return str(path)

    def _is_inside_profiles(
        self,
        path: Path,
    ) -> bool:
        try:
            path.resolve().relative_to(
                self.PROFILES_DIR.resolve()
            )

            return True

        except ValueError:
            return False