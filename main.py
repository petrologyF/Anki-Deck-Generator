import flet as ft
import os
from core import AnkiGenerator
import time
import ctypes

def main(page: ft.Page):
    # Windows Taskbar Icon Fix
    try:
        myappid = "anki.deck.generator"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    # 1. Page Initial Setup
    # ==========================================
    page.title = "Anki Deck Generator"
    page.window_width = 1400
    page.window_height = 950
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.DARK
    page.window_icon = os.path.abspath("assets/icon.png")
    page.icon = "icon.png"
    
    # Remove all default margins and gaps!
    page.padding = 0
    page.spacing = 0

    page.fonts = {
        "Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"
    }
    page.theme = ft.Theme(font_family="Outfit")

    generator = AnkiGenerator()
    ICON_PATH = os.path.abspath(r"assets/icon.png")

    VS_COLORS = {
        ft.ThemeMode.DARK: {
            "activity_bg": "#333333",
            "sidebar_bg": "#252526",
            "editor_bg": "#1e1e1e",
            "status_bg": "#007acc",
            "text_main": "#cccccc",
            "text_dim": "#858585",
            "border": "#454545",
            "tab_bg": "#2d2d2d",
            "panel_bg": "#1e1e1e"
        },
        ft.ThemeMode.LIGHT: {
            "activity_bg": "#2c2c2c",
            "sidebar_bg": "#f3f3f3",
            "editor_bg": "#ffffff",
            "status_bg": "#007acc",
            "text_main": "#3b3b3b",
            "text_dim": "#717171",
            "border": "#cccccc",
            "tab_bg": "#ececec",
            "panel_bg": "#ffffff"
        }
    }

    # 2. Components & State
    # ==========================================

    gen_status = ft.Text("⚠️ Ungenerated", size=11, color="white", weight=ft.FontWeight.BOLD)
    save_status = ft.Text("✔️ Saved", size=11, color="white", weight=ft.FontWeight.BOLD)
    
    word_count_text = ft.Text(f"{generator.get_word_count()}", size=36, weight=ft.FontWeight.W_300, color="#3b82f6")
    recent_files_list = ft.Column(spacing=2)
    log_content = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=2)

    webhook_input = ft.TextField(
        label="Discord Webhook URL",
        value=generator.discord_webhook_url or "",
        password=True,
        can_reveal_password=True,
        text_size=11,
        content_padding=ft.Padding.symmetric(horizontal=10, vertical=0),
        height=30,
        expand=True
    )

    progress_bar = ft.ProgressBar(width=None, color="#3b82f6", bgcolor="transparent", visible=False, height=2)

    # 3. Actions
    # ==========================================

    def add_log(msg, is_error=False):
        color = ft.Colors.RED_400 if is_error else ft.Colors.BLUE_200
        timestamp = time.strftime("%H:%M:%S")
        log_content.controls.append(ft.Text(f"[{timestamp}] {msg}", color=color, size=12, font_family="Consolas"))
        page.update()

    def update_stats():
        word_count_text.value = f"{generator.get_word_count()}"
        recent_files_list.controls.clear()
        for f in generator.get_recent_files():
            recent_files_list.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, size=13, color="#858585"),
                        ft.Text(f, size=12, color="#cccccc", no_wrap=True, expand=True),
                    ], spacing=6),
                    padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                    ink=True,
                    on_click=lambda _: os.startfile(generator.output_dir)
                )
            )
        page.update()

    def on_generate_click(e):
        generate_btn.disabled = True
        progress_bar.visible = True
        add_log("Generating Deck...")
        page.update()
        
        if webhook_input.value != generator.discord_webhook_url:
            generator.update_webhook(webhook_input.value)

        success, msg = generator.generate(log_callback=lambda m: add_log(m))
        
        if success:
            add_log("Success!", is_error=False)
            gen_status.value = "✔️ Generated"
        else:
            add_log(msg, is_error=True)
            
        generate_btn.disabled = False
        progress_bar.visible = False
        update_stats()
        update_sidebar_icons()
        page.update()

    def on_json_change(e):
        save_status.value = "⚠️ Unsaved"
        save_btn.disabled = False
        update_sidebar_icons()
        page.update()

    def on_save_json(e):
        success, msg = generator.save_words_json(json_editor.value)
        if success:
            save_status.value = "✔️ Saved"
            save_btn.disabled = True
            gen_status.value = "⚠️ Ungenerated"
            update_stats()
            update_sidebar_icons()
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        update_ui_colors()
        update_sidebar_icons()

    def update_sidebar_icons():
        # Save Button: Blue if Unsaved
        if save_status.value == "⚠️ Unsaved":
            save_btn.icon_color = "#3b82f6"
        else:
            save_btn.icon_color = "#858585"
            
        # Generate Button: Blue if Saved but Ungenerated
        if save_status.value == "✔️ Saved" and gen_status.value == "⚠️ Ungenerated":
            generate_btn.icon_color = "#3b82f6"
        else:
            generate_btn.icon_color = "#858585"
        
        page.update()

    # CUSTOM ACCORDION BUILDER
    def make_section(title, content_control, default_open=True):
        content_container = ft.Container(content=content_control, visible=default_open, padding=ft.Padding.only(bottom=10))
        icon = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN if default_open else ft.Icons.KEYBOARD_ARROW_RIGHT, size=14)
        
        def toggle_section(e):
            content_container.visible = not content_container.visible
            icon.name = ft.Icons.KEYBOARD_ARROW_DOWN if content_container.visible else ft.Icons.KEYBOARD_ARROW_RIGHT
            page.update()

        header = ft.Container(
            content=ft.Row([icon, ft.Text(title, size=11, weight=ft.FontWeight.BOLD)], spacing=2),
            on_click=toggle_section,
            ink=True,
            padding=ft.Padding.symmetric(vertical=4, horizontal=2)
        )
        return ft.Column([header, content_container], spacing=0)


    # 4. Layout Parts
    # ==========================================

    # --- MAIN EDITOR ---
    json_editor = ft.TextField(
        multiline=True,
        expand=True,
        value=generator.read_words_json(),
        text_style=ft.TextStyle(font_family="Consolas, monospace", size=13),
        border=ft.InputBorder.NONE,
        on_change=on_json_change,
        bgcolor="transparent",
        content_padding=ft.Padding.only(left=20, top=10, right=10),
    )

    # Actions for Sidebar
    save_btn = ft.IconButton(
        icon=ft.Icons.SAVE_OUTLINED, 
        on_click=on_save_json, 
        tooltip="Save Settings", 
        disabled=True, 
        icon_size=24, 
        icon_color="#858585"
    )
    generate_btn = ft.IconButton(
        icon=ft.Icons.PLAY_ARROW, 
        on_click=on_generate_click, 
        tooltip="Generate Deck", 
        icon_color="#858585", 
        icon_size=24
    )


    # --- SIDEBAR CONTENT ---
    sidebar_content = ft.Column([
        ft.Container(
            content=ft.Text("DASHBOARD", size=11, color="#bbbbbb"),
            padding=ft.Padding.only(left=20, top=10, bottom=10)
        ),
        ft.Container(
            content=ft.Column([
                make_section("STATISTICS", ft.Container(
                    content=ft.Column([
                        ft.Text("Total Words", size=10, color="#858585"),
                        word_count_text,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.Alignment(0, 0),
                    padding=10
                )),
                make_section("RECENT OUTPUTS", ft.Container(
                    content=recent_files_list, padding=0
                )),
            ], spacing=10, scroll=ft.ScrollMode.ADAPTIVE, expand=True),
            padding=ft.Padding.only(left=5, right=5),
            expand=True
        )
    ], spacing=0)

    # --- ACTIVITY LOG AREA ---
    terminal_tabs = ft.Container(
        content=ft.Row([
            ft.Text("TERMINAL", size=11, color="white", weight=ft.FontWeight.W_500),
        ]),
        padding=ft.Padding.only(left=20, top=6, bottom=6),
    )

    log_area = ft.Container(
        content=ft.Column([
            terminal_tabs,
            ft.Container(content=log_content, padding=ft.Padding.symmetric(horizontal=20, vertical=5), expand=True)
        ], spacing=0),
        height=220,
    )

    # --- SETTINGS DIALOG ---
    def open_settings(e):
        settings_dialog.open = True
        page.update()

    def close_settings(e):
        settings_dialog.open = False
        page.update()

    settings_dialog = ft.AlertDialog(
        title=ft.Text("Settings", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Container(
            content=ft.Column([
                ft.Text("Webhook Configuration", size=12, color="#858585", weight=ft.FontWeight.BOLD),
                webhook_input,
                ft.Divider(height=20, color="transparent"),
                ft.Row([
                    ft.Text("Dark Theme", size=14, expand=True),
                    ft.Switch(
                        value=page.theme_mode == ft.ThemeMode.DARK,
                        on_change=toggle_theme,
                        active_color="#3b82f6"
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ], tight=True, spacing=5),
            width=400,
            padding=10
        ),
        actions=[
            ft.TextButton("Done", on_click=close_settings)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.overlay.append(settings_dialog)
    page.dialog = settings_dialog

    # --- CUSTOM ACTIVITY BAR ---
    activity_bar = ft.Container(
        width=48, # Standard VS Code width
        content=ft.Column([
            ft.Container(height=10), # Spacer
            save_btn,
            generate_btn,
            ft.Container(expand=True),
            ft.IconButton(icon=ft.Icons.SETTINGS_OUTLINED, icon_size=24, icon_color="#858585", on_click=open_settings, tooltip="Settings"),
            ft.Container(height=10)
        ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    # --- STATUS BAR ---
    status_bar = ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Container(width=5),
                ft.Icon(ft.Icons.CHECK, size=13, color="white"),
                ft.Text("Anki Sync: Active", size=11, color="white"),
                ft.Container(width=15),
                gen_status,
                ft.Container(width=15),
                save_status,
            ], spacing=5),
            ft.Text("UTF-8  |  JSON", size=11, color="white")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        height=22,
        padding=ft.Padding.only(right=15),
        bgcolor="#007acc"
    )

    # 5. UI Updates & Composition
    # ==========================================

    sidebar_container = ft.Container(content=sidebar_content, width=250)
    editor_container = ft.Container(content=json_editor, expand=True)

    def update_ui_colors():
        c = VS_COLORS[page.theme_mode]
        page.bgcolor = c["editor_bg"]
        activity_bar.bgcolor = c["activity_bg"]
        sidebar_container.bgcolor = c["sidebar_bg"]
        log_area.bgcolor = c["panel_bg"]
        log_area.border = ft.Border.only(top=ft.BorderSide(1, c["border"]))
        sidebar_container.border = ft.Border.only(right=ft.BorderSide(1, c["border"]))
        status_bar.bgcolor = c["status_bg"]
        page.update()

    update_ui_colors()

    main_view = ft.Row([
        activity_bar,
        sidebar_container,
        ft.Column([
            progress_bar,
            editor_container,
            log_area
        ], expand=True, spacing=0)
    ], expand=True, spacing=0)

    page.add(
        ft.Column([
            main_view,
            status_bar
        ], expand=True, spacing=0)
    )

    update_stats()
    update_sidebar_icons()

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
