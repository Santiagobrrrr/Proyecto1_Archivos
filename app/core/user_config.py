from dataclasses import dataclass


@dataclass
class UserConfig:
    nombre_usuario: str = "José Muñoz"
    tema_interfaz: str = "claro"
    idioma: str = "es-ES"
    tamano_fuente: int = 14
    color_barra_menu: str = "#4F46E5"
    color_letra: str = "#F8FAFC"
    foto_perfil: str = ""

    def to_dict(self) -> dict:
        return {
            "nombre_usuario": self.nombre_usuario,
            "tema_interfaz": self.tema_interfaz,
            "idioma": self.idioma,
            "tamaño_fuente": self.tamano_fuente,
            "color_barra_menu": self.color_barra_menu,
            "color_letra": self.color_letra,
            "foto_perfil": self.foto_perfil,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserConfig":
        return cls(
            nombre_usuario=data.get("nombre_usuario", "José Muñoz"),
            tema_interfaz=data.get("tema_interfaz", "claro"),
            idioma=data.get("idioma", "es-ES"),
            tamano_fuente=data.get("tamaño_fuente", 14),
            color_barra_menu=data.get(
                "color_barra_menu",
                "#4F46E5",
            ),
            color_letra=data.get(
                "color_letra",
                "#F8FAFC",
            ),
            foto_perfil=data.get("foto_perfil", ""),
        )