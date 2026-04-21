import flet as ft
from app.main import main

if __name__ == "__main__":
    # Launch the application
    # The assets_dir is relative to this entry point script
    ft.run(main, assets_dir="assets")
