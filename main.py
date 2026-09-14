import sys

from PySide6.QtWidgets import QApplication

from app.core.user_config import UserConfig
from app.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)

    app.setApplicationName("UserConfig")
    app.setOrganizationName("Proyecto Manejo de Archivos")

    config = UserConfig()

    window = MainWindow(config)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())