import pkgutil
import os

def load_theme(theme):
    for try_theme in [theme, "ocean"]:
        theme_file = f"themes/{try_theme}.theme"
        try:
            theme_data = pkgutil.get_data(__name__, theme_file)
            if theme_data:
                return theme_data.decode("utf-8")
        except FileNotFoundError:
            pass