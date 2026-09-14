import sys

from PySide6.QtWidgets import QApplication

from app.services.config_manager import ConfigManager
from app.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)

    app.setApplicationName("UserConfig")
    app.setOrganizationName("Proyecto Manejo de Archivos")

    config_manager = ConfigManager()

    config, load_status = config_manager.load_config()

    window = MainWindow(
        config=config,
        load_status=load_status,
    )

    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())