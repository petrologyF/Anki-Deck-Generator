import flet as ft
from app.main import main

if __name__ == "__main__":
    # Switching back to ft.run as ft.app is deprecated in Flet 0.84.0+
    ft.run(main, assets_dir="assets")
