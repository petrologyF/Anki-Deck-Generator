import flet as ft
import pydoc
with open("flet_help.txt", "w") as f:
    f.write(pydoc.text.document(ft.Tab))
    f.write("\n\n")
    f.write(pydoc.text.document(ft.Tabs))
