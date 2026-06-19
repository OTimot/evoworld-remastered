from dataclasses import dataclass

@dataclass
class UITheme:
    background: tuple = (8, 12, 22)
    panel: tuple = (18, 24, 38)
    panel_light: tuple = (30, 42, 64)
    border: tuple = (86, 230, 160)
    text: tuple = (240, 245, 250)
    muted: tuple = (165, 180, 195)
    danger: tuple = (235, 80, 90)
    gold: tuple = (255, 210, 90)
    cyan: tuple = (95, 230, 255)

DEFAULT_THEME = UITheme()
